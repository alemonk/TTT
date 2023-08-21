import os
from website import create_app
from dotenv import load_dotenv


def configure():
    load_dotenv()


def main():
    configure()
    app = create_app()

    if __name__ == '__main__':
        app.run(debug=True)


main()
