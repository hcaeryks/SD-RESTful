from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def build_where_clause(params):
    clauses = []
    values = []
    for column, value in params.items():
        if value:
            clauses.append(f"{column} LIKE ?")
            values.append(f"%{value}%")
    return ' AND '.join(clauses), values

@app.route('/folders', methods=['GET'])
def get_folders():
    params = {
        'number': request.args.get('number'),
        'title': request.args.get('title'),
        'theme': request.args.get('theme'),
        'slogan': request.args.get('slogan')
    }
    where_clause, values = build_where_clause(params)

    query = "SELECT * FROM folder"
    if where_clause:
        query += f" WHERE {where_clause}"

    conn = get_db()
    folders = conn.execute(query, values).fetchall()
    conn.close()

    return jsonify([dict(folder) for folder in folders])

@app.route('/artists', methods=['GET'])
def get_artists():
    params = {
        'id': request.args.get('id'),
        'name': request.args.get('name'),
        'pseudonym': request.args.get('pseudonym')
    }
    where_clause, values = build_where_clause(params)

    query = "SELECT * FROM artist"
    if where_clause:
        query += f" WHERE {where_clause}"

    conn = get_db()
    artists = conn.execute(query, values).fetchall()
    conn.close()

    return jsonify([dict(artist) for artist in artists])

@app.route('/songs', methods=['GET'])
def get_songs():
    params = {
        'id': request.args.get('id'),
        'title': request.args.get('title'),
        'bpm': request.args.get('bpm'),
        'length': request.args.get('length'),
        'genre': request.args.get('genre'),
        'artist': request.args.get('artist'),
        'folder': request.args.get('folder'),
        'ln': request.args.get('ln'),
        'diffN': request.args.get('diffN'),
        'diffH': request.args.get('diffH'),
        'diffA': request.args.get('diffA'),
        'diffL': request.args.get('diffL')
    }
    where_clause, values = build_where_clause(params)

    query = "SELECT * FROM song"
    if where_clause:
        query += f" WHERE {where_clause}"

    conn = get_db()
    songs = conn.execute(query, values).fetchall()
    conn.close()

    return jsonify([dict(song) for song in songs])

@app.route('/folders', methods=['POST'])
def create_folder():
    data = request.json
    query = """
    INSERT INTO folder (number, title, theme, slogan) 
    VALUES (?, ?, ?, ?)
    """
    values = (
        data['number'],
        data['title'],
        data.get('theme'),
        data.get('slogan')
    )
    conn = get_db()
    conn.execute(query, values)
    conn.commit()
    conn.close()
    return jsonify({"message": "Folder created successfully"}), 201

@app.route('/artists', methods=['POST'])
def create_artist():
    data = request.json
    query = """
    INSERT INTO artist (name, pseudonym) 
    VALUES (?, ?)
    """
    values = (
        data['name'],
        data.get('pseudonym')
    )
    conn = get_db()
    conn.execute(query, values)
    artist_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"message": "Artist created successfully", "id": artist_id}), 201

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    query = """
    INSERT INTO song (title, bpm, length, genre, artist, folder, ln, diffN, diffH, diffA, diffL) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        data['title'],
        data.get('bpm'),
        data.get('length'),
        data.get('genre'),
        data.get('artist'),
        data.get('folder'),
        data.get('ln', 0),
        data.get('diffN'),
        data.get('diffH'),
        data.get('diffA'),
        data.get('diffL')
    )
    conn = get_db()
    conn.execute(query, values)
    song_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"message": "Song created successfully", "id": song_id}), 201

@app.route('/folders/<int:number>', methods=['DELETE'])
def delete_folder(number):
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM song WHERE folder = ?", (number,))
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return jsonify({"error": "Folder cannot be deleted as it has associated songs"}), 400
    
    conn.execute("DELETE FROM folder WHERE number = ?", (number,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Folder deleted successfully"}), 200

@app.route('/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM song WHERE artist = ?", (id,))
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return jsonify({"error": "Artist cannot be deleted as they have associated songs"}), 400
    
    conn.execute("DELETE FROM artist WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Artist deleted successfully"}), 200

@app.route('/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM song WHERE id = ?", (id,))
    count = cursor.fetchone()[0]
    if count == 0:
        conn.close()
        return jsonify({"error": "Song not found"}), 404
    
    conn.execute("DELETE FROM song WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Song deleted successfully"}), 200

@app.route('/folders/<int:number>', methods=['PUT'])
def update_folder(number):
    data = request.json
    update_fields = []
    values = []
    
    if 'title' in data:
        update_fields.append("title = ?")
        values.append(data['title'])
    if 'theme' in data:
        update_fields.append("theme = ?")
        values.append(data['theme'])
    if 'slogan' in data:
        update_fields.append("slogan = ?")
        values.append(data['slogan'])

    if update_fields:
        query = f"UPDATE folder SET {', '.join(update_fields)} WHERE number = ?"
        values.append(number)
        conn = get_db()
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({"message": "Folder updated successfully"}), 200
    else:
        return jsonify({"error": "No valid fields to update"}), 400

@app.route('/artists/<int:id>', methods=['PUT'])
def update_artist(id):
    data = request.json
    update_fields = []
    values = []
    
    if 'name' in data:
        update_fields.append("name = ?")
        values.append(data['name'])
    if 'pseudonym' in data:
        update_fields.append("pseudonym = ?")
        values.append(data['pseudonym'])

    if update_fields:
        query = f"UPDATE artist SET {', '.join(update_fields)} WHERE id = ?"
        values.append(id)
        conn = get_db()
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({"message": "Artist updated successfully"}), 200
    else:
        return jsonify({"error": "No valid fields to update"}), 400

@app.route('/songs/<int:id>', methods=['PUT'])
def update_song(id):
    data = request.json
    update_fields = []
    values = []
    
    if 'title' in data:
        update_fields.append("title = ?")
        values.append(data['title'])
    if 'bpm' in data:
        update_fields.append("bpm = ?")
        values.append(data['bpm'])
    if 'length' in data:
        update_fields.append("length = ?")
        values.append(data['length'])
    if 'genre' in data:
        update_fields.append("genre = ?")
        values.append(data['genre'])
    if 'artist' in data:
        update_fields.append("artist = ?")
        values.append(data['artist'])
    if 'folder' in data:
        update_fields.append("folder = ?")
        values.append(data['folder'])
    if 'ln' in data:
        update_fields.append("ln = ?")
        values.append(data['ln'])
    if 'diffN' in data:
        update_fields.append("diffN = ?")
        values.append(data['diffN'])
    if 'diffH' in data:
        update_fields.append("diffH = ?")
        values.append(data['diffH'])
    if 'diffA' in data:
        update_fields.append("diffA = ?")
        values.append(data['diffA'])
    if 'diffL' in data:
        update_fields.append("diffL = ?")
        values.append(data['diffL'])

    if update_fields:
        query = f"UPDATE song SET {', '.join(update_fields)} WHERE id = ?"
        values.append(id)
        conn = get_db()
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({"message": "Song updated successfully"}), 200
    else:
        return jsonify({"error": "No valid fields to update"}), 400

if __name__ == '__main__':
    app.run(debug=True)
