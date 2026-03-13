Markdown
# 🧮 Django Calculator Project

A full-stack Django web application that provides basic arithmetic operations with a built-in user authentication system. Built with portability in mind using Docker.

## 🚀 Features
* **User Authentication**: Secure Signup, Login, and Logout functionality using Django's built-in auth system.
* **Math Operations**: Addition, Subtraction, Multiplication, and Division.
* **Separated Logic**: Calculation logic is decoupled from views for better maintainability.
* **Dockerized**: Fully containerized environment for consistent deployment.

---

## 🛠️ Installation & Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/Sunil2409/Python_learnings.git](https://github.com/Sunil2409/Python_learnings.git)
cd calculator_app
2. Set up a Virtual Environment

Bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Database Migrations

Bash
python manage.py migrate
5. Run the Server

Bash
python manage.py runserver
Visit http://127.0.0.1:8000 to see the app!

🐳 Docker Setup
To run the application without installing Python locally, use Docker:

1. Download the code

2. Build the Image

Bash
docker build -t calculator-app .
3. Run the Container

Bash
docker run -p 8000:8000 calculator-app
The app will be accessible at http://localhost:8000.

📁 Project Structure
Plaintext
.
├── calculator_app/       # Main app logic (views, operations)
├── calculator_project/   # Project settings and root URLs
├── templates/            # HTML files (home, login, signup)
├── Dockerfile            # Container configuration
├── .dockerignore         # Files excluded from Docker build
├── .gitignore            # Files excluded from Git (env, db.sqlite3)
└── manage.py             # Django management script
🔒 Security Note
The .env file is excluded from this repository to protect the SECRET_KEY.

Ensure DEBUG=False is set in production environments.


---

### Why this README is effective:
1.  **Clear Icons**: Makes it scannable.
2.  **Step-by-Step**: It covers both the local "Python" way and the "Docker" way.
3.  **Structure**: It explains what the folders do, which is helpful for someone looking at your GitHub for the first time.
4.  **Security Awareness**: It shows you understand why certain files (like `.env`) are missing.

