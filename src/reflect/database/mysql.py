import os
from typing import Tuple, Union, List, Dict, Optional
from pathlib import Path

from datetime import datetime
from mysql.connector.pooling import MySQLConnectionPool
import funcy as fn
from pydantic import SecretStr
from reflect.config import AppConfig
from pydantic import BaseModel, validator
from reflect.utils import logger


class Entry(BaseModel):
    id: str
    project_name: str
    text: str
    type: str
    created_at: datetime
    votes: Optional[int]


class Project(BaseModel):
    id: str
    name: str
    created_at: datetime


class Votes(BaseModel):
    amount: int = 0


class MySQLDB:
    def __init__(
            self,
            host: str,
            port: str,
            username: SecretStr,
            password: SecretStr,
            database: str,
            pool_name: str,
            migrations_file: str,
            pool_size: int = 3,
            run_migrations: bool = True,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.cnx = MySQLConnectionPool(
            user=self.username.get_secret_value(),
            password=self.password.get_secret_value(),
            host=self.host,
            database=self.database,
            pool_name=pool_name,
            pool_size=pool_size
        )
        self.run_migrations = run_migrations
        self.migrations_file = migrations_file
        self._do_migrations()

    def _read_migrations_file(self):
        migrations_file = os.path.join(Path(__file__).parent, self.migrations_file)
        with open(migrations_file, "r") as file:
            statements = file.read().split(";")
        return fn.lfilter(lambda x: x.strip() != "", statements)

    def _do_migrations(self):
        if self.run_migrations:
            statements = self._read_migrations_file()
            conn = self.cnx.get_connection()
            try:
                cursor = conn.cursor()
                for stmt in statements:
                    cursor.execute(stmt)
                conn.commit()
                logger.info(f"Migrations run successfully")
            except Exception as err:
                logger.error(err)
                raise
            finally:
                conn.close()

    def _query(self, query: str, params: tuple = None, dictionary: bool = True):
        conn = self.cnx.get_connection()
        try:
            cursor = conn.cursor(dictionary=dictionary)
            cursor.execute(query, params)
            for row in cursor:
                yield row
        except Exception as err:
            logger.error(err)
            raise
        finally:
            conn.close()

    def _write(
            self,
            stmt: str,
            params: Union[Tuple, List[Tuple], List[Dict], Dict, None],
            many: bool = False,
            batch_size: int = 1000
    ):
        conn = self.cnx.get_connection()
        try:
            cursor = conn.cursor()
            if many is True:
                batches = fn.chunks(batch_size, params)
                fn.lmap(lambda chunk: cursor.executemany(stmt, chunk), batches)
            else:
                cursor.execute(stmt, params)
            conn.commit()
        except Exception as err:
            logger.error(err)
            conn.rollback()
            raise
        finally:
            conn.close()


class ReflectMySQL(MySQLDB):
    def save_project(self, name: str):
        stmt = """
        INSERT INTO projects (id, name) VALUES (UUID(), %s)
        """
        self._write(stmt, (name, ))

    def check_project_name(self, project_name: str):
        stmt = """
        SELECT * FROM projects WHERE name = %s
        """
        try:
            return next(self._query(stmt, (project_name, )))
        except StopIteration:
            return None

    def add_entry(self, project_name: str, text: str, type: str):
        stmt = """
        INSERT INTO project_entries (id, project_name, text, type) VALUES (UUID(), %s, %s, %s)
        """
        self._write(
            stmt=stmt,
            params=(project_name, text, type)
        )

    def get_entries_for_project_with_type(self, project_id: str, _type: str) -> List[Entry]:
        stmt = """
        SELECT * FROM project_entries WHERE project_name = %s AND type = %s
        """
        return [Entry(**x) for x in self._query(stmt, (project_id, _type))]

    def get_all_entries_for_project(self, project_id: str) -> List[Entry]:
        stmt = """
        SELECT
        pe.*,
        pv.votes
        FROM project_entries AS pe
        LEFT JOIN (
            SELECT entry_id, COUNT(1) AS votes
            FROM project_entries_votes
            WHERE project_name = %s GROUP BY entry_id
        ) AS pv ON pe.id = pv.entry_id
        WHERE pe.project_name = %s
        ORDER BY pe.created_at DESC;
        """
        return [Entry(**x) for x in self._query(stmt, (project_id, project_id))]

    def get_all_projects(self) -> List[Project]:
        stmt = """
        SELECT * FROM projects ORDER BY created_at DESC
        """
        return [Project(**x) for x in self._query(stmt)]

    def save_vote(self, project_name: str, event_id: str):
        stmt = """
        INSERT INTO project_entries_votes (id, project_name, entry_id) VALUES (UUID(), %s, %s)
        """
        self._write(stmt, (project_name, event_id))

    def get_votes(self, entry_id: str) -> Votes:
        stmt = """
        SELECT COUNT(1) AS amount FROM project_entries_votes WHERE entry_id = %s;
        """
        return Votes(**next(self._query(stmt, (entry_id, ))))


reflectdb = ReflectMySQL(
    host=AppConfig.mysql.HOST,
    port=AppConfig.mysql.PORT,
    username=AppConfig.mysql.USERNAME,
    password=AppConfig.mysql.PASSWORD,
    database=AppConfig.mysql.DATABASE,
    pool_size=AppConfig.mysql.DB_POOL_SIZE,
    pool_name="reflect-project-pool",
    migrations_file=AppConfig.mysql.MIGRATIONS_FILE,
    run_migrations=AppConfig.mysql.RUN_MIGRATIONS
)
