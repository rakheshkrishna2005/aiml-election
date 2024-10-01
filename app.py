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
    ]},
    3: {"name": "Public Relation Officer", "candidates": [
        {"id": 7, "name": "Candidate G", "image": "candidate.png"},
        {"id": 8, "name": "Candidate H", "image": "candidate.png"},
        {"id": 9, "name": "Candidate I", "image": "candidate.png"}
    ]},
    4: {"name": "Treasurer", "candidates": [
        {"id": 10, "name": "Candidate J", "image": "candidate.png"},
        {"id": 11, "name": "Candidate K", "image": "candidate.png"},
        {"id": 12, "name": "Candidate L", "image": "candidate.png"}
    ]},
    5: {"name": "Sponsorship Head", "candidates": [
        {"id": 13, "name": "Candidate M", "image": "candidate.png"},
        {"id": 14, "name": "Candidate N", "image": "candidate.png"},
        {"id": 15, "name": "Candidate O", "image": "candidate.png"}
    ]},
    6: {"name": "Head of Operations", "candidates": [
        {"id": 16, "name": "Candidate P", "image": "candidate.png"},
        {"id": 17, "name": "Candidate Q", "image": "candidate.png"},
        {"id": 18, "name": "Candidate R", "image": "candidate.png"}
    ]},
    7: {"name": "Technical Event Head", "candidates": [
        {"id": 19, "name": "Candidate S", "image": "candidate.png"},
        {"id": 20, "name": "Candidate T", "image": "candidate.png"},
        {"id": 21, "name": "Candidate U", "image": "candidate.png"}
    ]},
    8: {"name": "Non-Technical Event Head", "candidates": [
        {"id": 22, "name": "Candidate V", "image": "candidate.png"},
        {"id": 23, "name": "Candidate W", "image": "candidate.png"},
        {"id": 24, "name": "Candidate X", "image": "candidate.png"}
    ]},
    9: {"name": "Innovation Director", "candidates": [
        {"id": 25, "name": "Candidate Y", "image": "candidate.png"},
        {"id": 26, "name": "Candidate Z", "image": "candidate.png"},
        {"id": 27, "name": "Candidate AA", "image": "candidate.png"}
    ]},
    10: {"name": "Editorial Head", "candidates": [
        {"id": 28, "name": "Candidate BB", "image": "candidate.png"},
        {"id": 29, "name": "Candidate CC", "image": "candidate.png"},
        {"id": 30, "name": "Candidate DD", "image": "candidate.png"}
    ]},
    11: {"name": "Marketing Head", "candidates": [
        {"id": 31, "name": "Candidate EE", "image": "candidate.png"},
        {"id": 32, "name": "Candidate FF", "image": "candidate.png"},
        {"id": 33, "name": "Candidate GG", "image": "candidate.png"}
    ]},
    12: {"name": "Digital Head", "candidates": [
        {"id": 34, "name": "Candidate HH", "image": "candidate.png"},
        {"id": 35, "name": "Candidate II", "image": "candidate.png"},
        {"id": 36, "name": "Candidate JJ", "image": "candidate.png"}
    ]},
    13: {"name": "Head of Industry Interaction", "candidates": [
        {"id": 37, "name": "Candidate KK", "image": "candidate.png"},
        {"id": 38, "name": "Candidate LL", "image": "candidate.png"},
        {"id": 39, "name": "Candidate MM", "image": "candidate.png"}
    ]},
    14: {"name": "P.R.I.D.E Activities Director", "candidates": [
        {"id": 40, "name": "Candidate NN", "image": "candidate.png"},
        {"id": 41, "name": "Candidate OO", "image": "candidate.png"},
        {"id": 42, "name": "Candidate PP", "image": "candidate.png"}
    ]},
    15: {"name": "DSR Head", "candidates": [
        {"id": 43, "name": "Candidate QQ", "image": "candidate.png"},
        {"id": 44, "name": "Candidate RR", "image": "candidate.png"},
        {"id": 45, "name": "Candidate SS", "image": "candidate.png"}
    ]},
    16: {"name": "Student Coordinator Head", "candidates": [
        {"id": 46, "name": "Candidate TT", "image": "candidate.png"},
        {"id": 47, "name": "Candidate UU", "image": "candidate.png"},
        {"id": 48, "name": "Candidate VV", "image": "candidate.png"}
    ]},
    17: {"name": "Student Welfare Head", "candidates": [
        {"id": 49, "name": "Candidate WW", "image": "candidate.png"},
        {"id": 50, "name": "Candidate XX", "image": "candidate.png"},
        {"id": 51, "name": "Candidate YY", "image": "candidate.png"}
    ]},
    18: {"name": "Vice President", "candidates": [
        {"id": 52, "name": "Candidate ZZ", "image": "candidate.png"},
        {"id": 53, "name": "Candidate AAA", "image": "candidate.png"},
        {"id": 54, "name": "Candidate BBB", "image": "candidate.png"}
    ]},
    19: {"name": "Joint Secretary", "candidates": [
        {"id": 55, "name": "Candidate CCC", "image": "candidate.png"},
        {"id": 56, "name": "Candidate DDD", "image": "candidate.png"},
        {"id": 57, "name": "Candidate EEE", "image": "candidate.png"}
    ]},
    20: {"name": "Joint Public Relation Officer", "candidates": [
        {"id": 58, "name": "Candidate FFF", "image": "candidate.png"},
        {"id": 59, "name": "Candidate GGG", "image": "candidate.png"},
        {"id": 60, "name": "Candidate HHH", "image": "candidate.png"}
    ]},
    21: {"name": "Joint Treasurer", "candidates": [
        {"id": 61, "name": "Candidate III", "image": "candidate.png"},
        {"id": 62, "name": "Candidate JJJ", "image": "candidate.png"},
        {"id": 63, "name": "Candidate KKK", "image": "candidate.png"}
    ]},
    22: {"name": "Joint Sponsorship Head", "candidates": [
        {"id": 64, "name": "Candidate LLL", "image": "candidate.png"},
        {"id": 65, "name": "Candidate MMM", "image": "candidate.png"},
        {"id": 66, "name": "Candidate NNN", "image": "candidate.png"}
    ]},
    23: {"name": "Joint Technical Event Head", "candidates": [
        {"id": 67, "name": "Candidate OOO", "image": "candidate.png"},
        {"id": 68, "name": "Candidate PPP", "image": "candidate.png"},
        {"id": 69, "name": "Candidate QQQ", "image": "candidate.png"}
    ]},
    24: {"name": "Joint Non-Technical Event Head", "candidates": [
        {"id": 70, "name": "Candidate RRR", "image": "candidate.png"},
        {"id": 71, "name": "Candidate SSS", "image": "candidate.png"},
        {"id": 72, "name": "Candidate TTT", "image": "candidate.png"}
    ]},
    25: {"name": "Joint Innovation Director", "candidates": [
        {"id": 73, "name": "Candidate UUU", "image": "candidate.png"},
        {"id": 74, "name": "Candidate VVV", "image": "candidate.png"},
        {"id": 75, "name": "Candidate WWW", "image": "candidate.png"}
    ]},
    26: {"name": "Joint Editorial Head", "candidates": [
        {"id": 76, "name": "Candidate XXX", "image": "candidate.png"},
        {"id": 77, "name": "Candidate YYY", "image": "candidate.png"},
        {"id": 78, "name": "Candidate ZZZ", "image": "candidate.png"}
    ]},
    27: {"name": "Joint Marketing Head", "candidates": [
        {"id": 79, "name": "Candidate AAAA", "image": "candidate.png"},
        {"id": 80, "name": "Candidate BBBB", "image": "candidate.png"},
        {"id": 81, "name": "Candidate CCCC", "image": "candidate.png"}
    ]},
    28: {"name": "Joint Digital Head", "candidates": [
        {"id": 82, "name": "Candidate DDDD", "image": "candidate.png"},
        {"id": 83, "name": "Candidate EEEE", "image": "candidate.png"},
        {"id": 84, "name": "Candidate FFFF", "image": "candidate.png"}
    ]},
    29: {"name": "Joint Head of Industry Interaction", "candidates": [
        {"id": 85, "name": "Candidate GGGG", "image": "candidate.png"},
        {"id": 86, "name": "Candidate HHHH", "image": "candidate.png"},
        {"id": 87, "name": "Candidate IIII", "image": "candidate.png"}
    ]},
    30: {"name": "Joint P.R.I.D.E Activities Director", "candidates": [
        {"id": 88, "name": "Candidate JJJJ", "image": "candidate.png"},
        {"id": 89, "name": "Candidate KKKK", "image": "candidate.png"},
        {"id": 90, "name": "Candidate LLLL", "image": "candidate.png"}
    ]},
    31: {"name": "Joint DSR Head", "candidates": [
        {"id": 91, "name": "Candidate MMMM", "image": "candidate.png"},
        {"id": 92, "name": "Candidate NNNN", "image": "candidate.png"},
        {"id": 93, "name": "Candidate OOOO", "image": "candidate.png"}
    ]},
    32: {"name": "Joint Student Coordinator Head", "candidates": [
        {"id": 94, "name": "Candidate PPPP", "image": "candidate.png"},
        {"id": 95, "name": "Candidate QQQQ", "image": "candidate.png"},
        {"id": 96, "name": "Candidate RRRR", "image": "candidate.png"}
    ]},
    33: {"name": "Joint Student Welfare Head", "candidates": [
        {"id": 97, "name": "Candidate SSSS", "image": "candidate.png"},
        {"id": 98, "name": "Candidate TTTT", "image": "candidate.png"},
        {"id": 99, "name": "Candidate UUUU", "image": "candidate.png"}
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
    else:
        cur.execute("INSERT INTO votes (user_id, candidate_id, position_id) VALUES (?, ?, ?)", (user_id, candidate_id, position_id))
        conn.commit()
        cur.close()
        conn.close()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(f'{user_role}_dashboard.html', positions=get_positions(user_id))
    else:
        return redirect(url_for(f"{user_role}_dashboard"))

def get_positions(user_id):
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
    return positions

if __name__ == '__main__':
    app.run(debug=True)
