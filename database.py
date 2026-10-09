import sqlite3

def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            views INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("DB is ready")

def seed_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    starter_authors = [
        ("Bob", "hello"),
        ("Ann", "world"),
        ("Jack", ""),
    ]
    cursor.executemany(
        "INSERT INTO authors (name, bio) VALUES (?, ?)",
        starter_authors
    )
    conn.commit()
    print(f"Добавили {len(starter_authors)} authors")

    starter_posts = [
        ("Moon", "hello", 1, 1),
        ("Dinosaurs", "hello", 2, 2),
        ("Earth", "hello", 3, 3),
        ("Food", "hello", 3, 3),
        ("Poop", "hello", 3, 3),
    ]
    cursor.executemany(
        "INSERT INTO posts (title, content, author_id, views) VALUES (?, ?, ?, ?)",
        starter_posts
    )
    conn.commit()
    conn.close()
    print(f"Добавили {len(starter_posts)} posts")

if __name__ == "__main__":
    init_db()
    seed_db()