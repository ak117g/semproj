"""
Personal Portfolio Web Application
Built for: First Semester Project (VITyarthi Guidelines)
Description: A modular Flask application demonstrating OOP principles, 
database integration (SQLite), and responsive frontend design.
"""

from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import datetime
from dataclasses import dataclass
import os
import webbrowser
import threading

# ==========================================
# MODULE 1: Data Models
# ==========================================
@dataclass
class ProfileInfo:
    """Data class representing personal information."""
    name: str
    tagline: str
    bio: str
    email: str
    github: str

@dataclass
class AcademicInfo:
    """Data class representing college and academic life."""
    university: str
    major: str
    current_cgpa: float
    key_courses: list
    academic_achievements: list

@dataclass
class NonAcademicInfo:
    """Data class representing extracurriculars and hobbies."""
    clubs: list
    hobbies: list
    technical_skills: list

# ==========================================
# MODULE 2: Database Management (Functional Requirement 2)
# ==========================================
class DatabaseManager:
    """Handles all SQLite database connections and queries."""
    
    def __init__(self, db_name="portfolio.db"):
        self.db_name = db_name
        self._initialize_db()

    def _get_connection(self):
        """Creates and returns a database connection."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    def _initialize_db(self):
        """Creates tables if they do not exist."""
        conn = self._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Table for storing contact messages
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS contact_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp TEXT NOT NULL
                    )
                ''')
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error initializing tables: {e}")
            finally:
                conn.close()

    def insert_message(self, name: str, email: str, message: str) -> bool:
        """Inserts a new contact message into the database (CRUD: Create)."""
        conn = self._get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO contact_messages (name, email, message, timestamp) VALUES (?, ?, ?, ?)",
                    (name, email, message, timestamp)
                )
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error inserting message: {e}")
                return False
            finally:
                conn.close()
        return False

    def get_all_messages(self):
        """Retrieves all messages for the admin view (CRUD: Read)."""
        conn = self._get_connection()
        messages = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM contact_messages ORDER BY id DESC")
                messages = cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error fetching messages: {e}")
            finally:
                conn.close()
        return messages


# ==========================================
# MODULE 3: Portfolio Data Controller
# ==========================================
class PortfolioManager:
    """Acts as a central controller for providing data to the views."""
    
    def __init__(self):
        # Mock data (Replace with your actual details)
        self.profile = ProfileInfo(
            name="Akhil Vajjhala",
            tagline="Mehnat karo jhaat bhar, bakchodi Karo raat bhar",
            bio="Hello! I am a passionate first-year student eager to learn and build impactful software. I love solving problems and turning ideas into code.",
            email="vajjhalaakhil34@gmail.com",
            github="github.com/luffy47"
        )
        
        self.academic = AcademicInfo(
            university="VIT Bhopal University",
            major="B.Tech in Electronics and communication Engineering",
            current_cgpa=9.2,
            key_courses=["Electric circuits and syystems (EEE1001)","Calculus (MAT1003)","Introduction to programming and problem solving (CSE1001)"],
            academic_achievements=["Got into Team vortex with a great price (13000 Rs)"]
        )
        
        self.non_academic = NonAcademicInfo(
            clubs=["None"],
            hobbies=["Boxing", "Playing Chess", "Breathing","playing Football","More breathing", "Eating", "Blinking"],
            technical_skills=["Python", "SQL"]
        )

    def get_context(self):
        """Returns a dictionary context for the template engine."""
        return {
            "profile": self.profile,
            "academic": self.academic,
            "non_academic": self.non_academic
        }


# ==========================================
# MODULE 4: Frontend HTML/Tailwind Template
# ==========================================
# We store the HTML as a string here to keep the project in a single file
# while maintaining a beautiful, responsive UI.
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ profile.name }} | Portfolio</title>
    <!-- Non-Functional Requirement: Usability & UI design via Tailwind -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">

    <!-- Navigation -->
    <nav class="bg-white shadow-md fixed w-full z-10 top-0">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="font-bold text-xl text-blue-600">{{ profile.name }}</div>
                <div class="hidden md:flex space-x-6">
                    <a href="#about" class="hover:text-blue-600 transition">About Me</a>
                    <a href="#academics" class="hover:text-blue-600 transition">Academic Life</a>
                    <a href="#extracurriculars" class="hover:text-blue-600 transition">Non-Academic</a>
                    <a href="#contact" class="hover:text-blue-600 transition">Contact</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="about" class="pt-32 pb-20 px-4 max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-12">
        <div class="flex-1 text-center md:text-left">
            <h1 class="text-5xl font-extrabold mb-4 text-gray-900">Hi, I'm <span class="text-blue-600">{{ profile.name }}</span></h1>
            <p class="text-2xl text-gray-600 mb-6">{{ profile.tagline }}</p>
            <p class="text-lg text-gray-500 mb-8">{{ profile.bio }}</p>
            <div class="flex justify-center md:justify-start space-x-4">
                <a href="#contact" class="bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-blue-700 transition">Get in Touch</a>
                <a href="https://{{ profile.github }}" target="_blank" class="bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-gray-900 transition"><i class="fab fa-github mr-2"></i>GitHub</a>
            </div>
        </div>
        <div class="flex-1 flex justify-center">
            <!-- Placeholder for profile picture -->
            <div class="w-64 h-64 bg-blue-100 rounded-full border-4 border-blue-500 shadow-xl flex items-center justify-center overflow-hidden">
                <i class="fas fa-user-graduate text-6xl text-blue-500"></i>
            </div>
        </div>
    </section>

    <!-- Academic Life Section -->
    <section id="academics" class="py-20 bg-white px-4">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-3xl font-bold mb-10 text-center border-b-4 border-blue-600 inline-block pb-2">Academic Life</h2>
            <div class="grid md:grid-cols-2 gap-10">
                <div class="bg-blue-50 p-8 rounded-xl shadow-sm border border-blue-100">
                    <h3 class="text-xl font-bold text-blue-800 mb-4"><i class="fas fa-university mr-2"></i>College Details</h3>
                    <p class="text-lg mb-2"><strong>University:</strong> {{ academic.university }}</p>
                    <p class="text-lg mb-2"><strong>Major:</strong> {{ academic.major }}</p>
                    <p class="text-lg mb-2"><strong>Current CGPA:</strong> <span class="bg-green-100 text-green-800 px-2 py-1 rounded font-bold">{{ academic.current_cgpa }}</span></p>
                </div>
                
                <div class="bg-gray-50 p-8 rounded-xl shadow-sm border border-gray-100">
                    <h3 class="text-xl font-bold text-gray-800 mb-4"><i class="fas fa-book-open mr-2"></i>Key Coursework</h3>
                    <ul class="list-disc pl-5 space-y-2 text-gray-700">
                        {% for course in academic.key_courses %}
                            <li>{{ course }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            
            <div class="mt-10 bg-yellow-50 p-8 rounded-xl shadow-sm border border-yellow-100">
                <h3 class="text-xl font-bold text-yellow-800 mb-4"><i class="fas fa-trophy mr-2"></i>Academic Achievements</h3>
                <ul class="list-disc pl-5 space-y-2 text-gray-700">
                    {% for achievement in academic.academic_achievements %}
                        <li>{{ achievement }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </section>

    <!-- Non-Academic Life Section -->
    <section id="extracurriculars" class="py-20 px-4 bg-gray-50">
        <div class="max-w-6xl mx-auto">
            <h2 class="text-3xl font-bold mb-10 text-center border-b-4 border-blue-600 inline-block pb-2">Non-Academic Life</h2>
            <div class="grid md:grid-cols-3 gap-8">
                
                <!-- Skills -->
                <div class="bg-white p-6 rounded-xl shadow-md border-t-4 border-blue-500">
                    <h3 class="text-xl font-bold mb-4"><i class="fas fa-laptop-code mr-2 text-blue-500"></i>Technical Skills</h3>
                    <div class="flex flex-wrap gap-2">
                        {% for skill in non_academic.technical_skills %}
                            <span class="bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm font-semibold">{{ skill }}</span>
                        {% endfor %}
                    </div>
                </div>

                <!-- Clubs -->
                <div class="bg-white p-6 rounded-xl shadow-md border-t-4 border-green-500">
                    <h3 class="text-xl font-bold mb-4"><i class="fas fa-users mr-2 text-green-500"></i>Clubs & Societies</h3>
                    <ul class="list-disc pl-5 text-gray-600 space-y-1">
                        {% for club in non_academic.clubs %}
                            <li>{{ club }}</li>
                        {% endfor %}
                    </ul>
                </div>

                <!-- Hobbies -->
                <div class="bg-white p-6 rounded-xl shadow-md border-t-4 border-purple-500">
                    <h3 class="text-xl font-bold mb-4"><i class="fas fa-palette mr-2 text-purple-500"></i>Hobbies</h3>
                    <ul class="list-disc pl-5 text-gray-600 space-y-1">
                        {% for hobby in non_academic.hobbies %}
                            <li>{{ hobby }}</li>
                        {% endfor %}
                    </ul>
                </div>

            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="py-20 bg-white px-4">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold mb-8 text-center border-b-4 border-blue-600 inline-block pb-2">Contact Me</h2>
            
            {% if status == 'success' %}
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-6" role="alert">
                <span class="block sm:inline">Thank you! Your message has been saved successfully.</span>
            </div>
            {% elif status == 'error' %}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
                <span class="block sm:inline">Error saving message. Please try again.</span>
            </div>
            {% endif %}

            <form action="/submit_contact" method="POST" class="bg-gray-50 shadow-lg rounded-xl p-8 border border-gray-100">
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="name">Your Name</label>
                    <input class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" id="name" name="name" type="text" placeholder="John Doe" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email Address</label>
                    <input class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" id="email" name="email" type="email" placeholder="john@example.com" required>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="message">Message</label>
                    <textarea class="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500" id="message" name="message" rows="5" placeholder="Let's connect!" required></textarea>
                </div>
                <div class="flex items-center justify-center">
                    <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg focus:outline-none focus:shadow-outline transition w-full shadow-md" type="submit">
                        Send Message
                    </button>
                </div>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-8 text-center">
        <p>&copy; 2026 {{ profile.name }}. Built with Python & Flask for the First Semester Project.</p>
        <div class="mt-4">
            <a href="/admin" class="text-gray-500 hover:text-white text-sm"><i class="fas fa-lock mr-1"></i>Admin Panel</a>
        </div>
    </footer>

</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-5xl mx-auto">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800"><i class="fas fa-database mr-2"></i>Contact Messages Database</h1>
            <a href="/" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">Back to Portfolio</a>
        </div>
        
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <table class="min-w-full leading-normal">
                <thead>
                    <tr>
                        <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">ID</th>
                        <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Date/Time</th>
                        <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Name</th>
                        <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Email</th>
                        <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Message</th>
                    </tr>
                </thead>
                <tbody>
                    {% for msg in messages %}
                    <tr>
                        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="text-gray-900 whitespace-no-wrap">{{ msg.id }}</p></td>
                        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="text-gray-900 whitespace-no-wrap">{{ msg.timestamp }}</p></td>
                        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="text-gray-900 whitespace-no-wrap font-bold">{{ msg.name }}</p></td>
                        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="text-gray-900 whitespace-no-wrap">{{ msg.email }}</p></td>
                        <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm"><p class="text-gray-700 whitespace-no-wrap">{{ msg.message }}</p></td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-center text-gray-500">No messages received yet.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# MODULE 5: Application Router & Controllers
# ==========================================
class PortfolioApp:
    """Wrapper class for the Flask application to maintain OOP structure."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.db_manager = DatabaseManager()
        self.portfolio_data = PortfolioManager()
        self._setup_routes()

    def _setup_routes(self):
        """Maps URLs to their respective handler functions."""
        
        @self.app.route("/")
        def home():
            # Get data context and URL parameters (for success/error messages)
            context = self.portfolio_data.get_context()
            context['status'] = request.args.get('status')
            # Render the template with the data context
            return render_template_string(MAIN_TEMPLATE, **context)

        @self.app.route("/submit_contact", methods=['POST'])
        def submit_contact():
            # Extract data from the HTTP POST request
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Non-Functional Requirement: Error Handling and Data Validation
            if not name or not email or not message:
                return redirect(url_for('home', status='error'))
                
            # Perform database insertion
            success = self.db_manager.insert_message(name, email, message)
            
            if success:
                return redirect(url_for('home', status='success', _anchor='contact'))
            else:
                return redirect(url_for('home', status='error', _anchor='contact'))

        @self.app.route("/admin")
        def admin_dashboard():
            # Retrieve all messages for the dashboard
            messages = self.db_manager.get_all_messages()
            return render_template_string(ADMIN_TEMPLATE, messages=messages)

    def run(self):
        """Starts the Flask development server and opens the browser."""
        # Run on localhost, port 5000. Debug enabled for development.
        print("Starting Portfolio Web Application...")
        
        # Open the web browser after a short 1-second delay
        # to ensure the server has time to start up first.
        url = "http://127.0.0.1:5000"
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        
        # Start the Flask app
        self.app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    # Create an instance of our application and run it
    my_portfolio = PortfolioApp()
    my_portfolio.run()