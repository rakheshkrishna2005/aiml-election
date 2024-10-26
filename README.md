# 🗳️ Voting System App

This is a web-based voting application built with Flask. It enables users to vote for candidates in different positions, providing a simple and secure platform for managing online elections.

## ⚖️ Voting Weightage

- `Student Votes: 1 point`
- `Teacher Votes: 5 points`
  
## 📋 Features

- **Candidate Management**: Add and display candidates for each position.
- **User Authentication**: Secure login with password hashing.
- **Vote Casting**: Allows registered users to vote for different positions.
- **Database Integration**: Uses SQLite to store user data and voting information.

## 🛠️ Tech Stack

- **Backend**: Flask
- **Database**: SQLite
- **Security**: Password hashing with Werkzeug
- **Frontend**: HTML templates with Jinja2

# 📷 Screenshots

## Home
![home](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Home.png)

## Sign Up
![sign up](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Sign%20Up.png)

## Login
![login](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Login.png)

## Results Dashboard - Admin Access
![results](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Results%20Dashboard.png)

## Student Dashboard
![student dashboard](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Student%20Dashboard.png)

## Teacher Dashboard
![teacher dashboard](https://github.com/rakheshkrishna2005/aiml-election/blob/main/static/screenshots/Teacher%20Dashboard.png)

## 📥 Installation and Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rakheshkrishna2005/aiml-election.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd aiml-election
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   python app.py
   ```

5. Access the app at `http://localhost:5000`
   
## 📚 Additional Resources

- [Werkzeug Security](https://werkzeug.palletsprojects.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
