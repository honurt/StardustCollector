from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Veritabanını başlatan fonksiyon
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Liderlik tablosu için SQLite tablosunu oluşturuyoruz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Frontend dosyamızı çağırıyoruz
    return render_template('index.html')

@app.route('/game')
def game():
    # Game page after welcome
    return render_template('index.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    username = data.get('username')
    score = data.get('score')

    if username and score is not None:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leaderboard (username, score) VALUES (?, ?)', (username, score))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # En yüksek 5 skoru getiriyoruz
    cursor.execute('SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 5')
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)