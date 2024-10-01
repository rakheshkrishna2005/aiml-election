import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Manually define positions and candidates
POSITIONS = {
    1: {"name": "President", "candidates": [
        {"id": 1, "name": "Candidate A", "image": "candidate.png"},
        {"id": 2, "name": "Candidate B", "image": "candidate.png"},
        {"id": 3, "name": "Candidate C", "image": "candidate.png"}
    ]},
    2: {"name": "Secretary", "candidates": [
        {"id": 4, "name": "Candidate D", "image": "candidate.png"},
        {"id": 5, "name": "Candidate E", "image": "candidate.png"},
        {"id": 6, "name": "Candidate F", "image": "candidate.png"}
    ]}
}

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Use an SQLite database file
    conn.row_factory = sqlite3.Row  # This allows us to treat rows as dictionaries
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support in SQLite
    return conn

# Database initialization
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS votes
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    candidate_id INTEGER NOT NULL,
                    position_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    cur.close()
    conn.close()

# Ensure the database is initialized when the app starts
with app.app_context():
    init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            conn.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.', 'error')
        finally:
            cur.close()
            conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    results = {}
    
    for position_id, position_data in POSITIONS.items():
        results[position_data['name']] = []
        for candidate in position_data['candidates']:
            cur.execute('''
                SELECT 
                    COUNT(CASE WHEN users.role = 'student' THEN 1 ELSE NULL END) as student_votes,
                    COUNT(CASE WHEN users.role = 'teacher' THEN 1 ELSE NULL END) as teacher_votes
                FROM votes
                JOIN users ON votes.user_id = users.id
                WHERE votes.candidate_id = ? AND votes.position_id = ?
            ''', (candidate['id'], position_id))
            vote_counts = cur.fetchone()
            results[position_data['name']].append({
                'name': candidate['name'],
                'student_votes': vote_counts['student_votes'],
                'teacher_votes': vote_counts['teacher_votes'],
                'total_points': vote_counts['student_votes'] + vote_counts['teacher_votes'] * 5
            })
    
    cur.close()
    conn.close()
    
    return render_template('admin_dashboard.html', results=results)

@app.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT position_id FROM votes WHERE user_id = ?", (user_id,))
    voted_positions = {row['position_id'] for row in cur.fetchall()}
    cur.close()
    conn.close()
    
    positions = {
        position_id: {
            'name': position_data['name'],
            'candidates': position_data['candidates'],
            'voted': position_id in voted_positions
        }
        for position_id, position_data in POSITIONS.items()
    }
    
    return render_template('teacher_dashboard.html', positions=positions)

@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT position_id FROM votes WHERE user_id = ?", (user_id,))
    voted_positions = {row['position_id'] for row in cur.fetchall()}
    cur.close()
    conn.close()
    
    positions = {
        position_id: {
            'name': position_data['name'],
            'candidates': position_data['candidates'],
            'voted': position_id in voted_positions
        }
        for position_id, position_data in POSITIONS.items()
    }
    
    return render_template('student_dashboard.html', positions=positions)

@app.route('/vote', methods=['POST'])
def vote():
    if session.get('role') not in ['student', 'teacher']:
        return redirect(url_for('login'))
    
    position_id = int(request.form['position_id'])
    candidate_id = int(request.form['candidate_id'])
    user_id = session['user_id']
    user_role = session['role']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM votes WHERE user_id = ? AND position_id = ?", (user_id, position_id))
    if cur.fetchone():
        cur.close()
        conn.close()
        flash('You have already voted for this position', 'error')
        return redirect(url_for(f"{user_role}_dashboard"))
    
    cur.execute("INSERT INTO votes (user_id, candidate_id, position_id) VALUES (?, ?, ?)", (user_id, candidate_id, position_id))
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Vote casted successfully', 'success')
    return redirect(url_for(f"{user_role}_dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
