<!-- STREAMING_CHUNK: Initializing the README structure... -->
# Python Dynamic Portfolio Web App

## Overview
This project is an Interactive Personal Portfolio Web Application developed as a first-semester project. It is built using Python (Flask) and SQLite for the backend, and HTML/Tailwind CSS for the frontend. It serves as a comprehensive digital resume detailing my personal details, academic journey, and non-academic life.

This project was built adhering to the structural and technical guidelines provided in the `BuildYourOwnProjectVITyarthi.pdf` document.

<!-- STREAMING_CHUNK: Detailing features and technologies... -->
## Features
*   **Responsive UI:** Beautiful, modern design that works on all devices.
*   **Modular Architecture:** Python backend built with OOP principles (Data Models, Database Managers, View Controllers).
*   **SQLite Database Integration:** Features a fully functional contact form that saves messages to a local database.
*   **Admin Dashboard:** A hidden route (`/admin`) to view all incoming messages, demonstrating CRUD operations.
*   **Error Handling:** Robust backend validation and exception handling for database operations.

## Technologies Used
*   **Backend:** Python 3, Flask
*   **Database:** SQLite (via standard `sqlite3` library)
*   **Frontend:** HTML5, Tailwind CSS (via CDN), FontAwesome

<!-- STREAMING_CHUNK: Providing installation and testing instructions... -->
## Steps to Install & Run the Project

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.
2.  **Install Dependencies:** Open your terminal and install Flask.
    ```bash
    pip install Flask
    ```
3.  **Run the Application:** Execute the main Python file.
    ```bash
    python app.py
    ```
4.  **Access the Website:** Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000
    ```

## Instructions for Testing
1.  **UI Testing:** Navigate through the "About Me", "Academics", and "Non-Academics" sections to ensure responsiveness on different screen sizes.
2.  **Functional Testing (Contact Form):** 
    * Scroll to the Contact section.
    * Enter a test name, email, and message, then submit.
    * Verify the success message appears.
3.  **Database Validation:**
    * Navigate to `http://127.0.0.1:5000/admin` in your browser.
    * Verify that the message you just submitted appears in the database records table.