from app.app import create_app

HOST = None

if __name__ == '__main__':
    app = create_app()
    app.run(host=HOST)
