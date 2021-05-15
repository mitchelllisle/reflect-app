CREATE TABLE IF NOT EXISTS projects (
    id BINARY(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY category_transactions_status_idx (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS project_entries (
    id BINARY(36) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    text VARCHAR(255) NOT NULL,
    type ENUM('GOOD', 'BAD', 'WONDERING'),
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY project_entries_type_idx (type) USING BTREE,
    CONSTRAINT project_entries_project_name_ FOREIGN KEY (project_name) REFERENCES projects (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS project_entries_votes (
  id binary(36) NOT NULL,
  project_name varchar(255) NOT NULL,
  entry_id binary(36) NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_updated timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY entry_id (entry_id),
  KEY project_entries_votes_project_name_idx (project_name) USING BTREE,
  CONSTRAINT project_entries_votes_ibfk_1_ FOREIGN KEY (entry_id) REFERENCES project_entries (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;