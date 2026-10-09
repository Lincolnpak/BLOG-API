from flask import Blueprint, request, jsonify
from db import get_db_connection

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/posts", methods=['GET'])
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

@posts_bp.route("/posts/<int:id>", methods=['GET'])
def get_post(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            posts.id AS post_id,
            posts.title,
            posts.content,
            posts.views,
            authors.id AS author_id,
            authors.name,
            authors.bio
        FROM posts
        JOIN authors ON posts.author_id = authors.id
        WHERE post_id = ?
        """, (id,))
    row = cursor.fetchone()
    conn.close()

    row = dict(row)

    post = {
        "id": row["post_id"],
        "title": row["title"],
        "content": row["content"],
        "views": row["views"],
        "author": {
            "id": row["author_id"],
            "name": row["name"],
            "bio": row["bio"],
        }
    }

    if post is None:
        return jsonify({"error":"Post not found"}), 404
    return jsonify(post)

@posts_bp.route("/posts", methods=['POST'])
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
