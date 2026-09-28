import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

def get_db_connection():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/authors", methods=['GET'])
def get_authors():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    conn.close()
    return jsonify([dict(author) for author in authors])

@app.route("/posts", methods=['GET'])
def get_posts():
    author_id = request.args.get("author_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    if author_id:
        cursor.execute("SELECT * FROM posts WHERE author_id = ?", (author_id,))
    else:
        cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return jsonify([dict(post) for post in posts])

@app.route("/posts/<int:id>", methods=['GET'])
def get_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (id,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return jsonify({"error":"Post not found"}), 404
    return jsonify(dict(post))

@app.route("/posts", methods=['POST'])
def add_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    title = data.get("title")
    content = data.get("content")
    author_id = data.get("author_id")
    views = data.get("views")

    if not title or not content or author_id is None:
        return jsonify({"error": "Fields title, content, and author_id are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
    author = cursor.fetchone()
    if author is None:
        return jsonify({"error":"Author was not found"}), 400
    
    cursor.execute(
        "INSERT INTO posts (title, content, author_id, views) VALUES (?, ?, ?, ?)",
        (title, content, author_id, views if views else 0)
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "title": title,
        "content": content,
        "author_id": author_id,
        "views": views if views else 0
    }), 201

@app.route("/authors/<int:id>/posts", methods=['GET'])
def get_posts_from_author(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
    author = cursor.fetchone()
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    
    cursor.execute("SELECT * FROM posts WHERE author_id = ?", (id,))
    posts = cursor.fetchall()
    conn.close()

    return jsonify([dict(post) for post in posts])

if __name__ == "__main__":
    app.run(debug=True)