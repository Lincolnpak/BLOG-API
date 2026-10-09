from flask import Flask
from routes.authors import authors_bp
from routes.posts import posts_bp

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False

    app.register_blueprint(authors_bp)
    app.register_blueprint(posts_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)