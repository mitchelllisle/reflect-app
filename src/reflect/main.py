from reflect.app import app
from reflect.config import AppConfig


if __name__ == '__main__':
    app.run_server(debug=AppConfig.dash.debug)
