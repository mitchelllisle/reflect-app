from reflect.app import app
from reflect.config import AppConfig


def main():
    app.run_server(debug=AppConfig.dash.debug)


if __name__ == '__main__':
    main()
