from flask import Blueprint, request, jsonify
from db import get_db_connection

authors_bp = Blueprint("authors", __name__)

@authors_bp.route("/authors", methods=['GET'])
def get_authors():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    conn.close()
    return jsonify([dict(author) for author in authors])

@authors_bp.route("/authors/<int:id>/posts", methods=['GET'])
def get_posts_from_author(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
    author = cursor.fetchone()
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    
    cursor.execute("""SELECT 
                posts.id AS post_id,
                posts.title,
                posts.content,
                posts.views FROM posts WHERE author_id = ?""", (id,))
    rows = cursor.fetchall()
    conn.close()
    
    posts = [dict(row) for row in rows]
    result = {
        "id": author["id"],
        "name": author["name"],
        "bio":author["bio"],
        "posts":posts
    }
    
    return jsonify(result)
