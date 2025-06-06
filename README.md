# FlashCard Hub

**Team Members:**
*   Maddy - Frontend Development & UI/UX Design
*   Sean - Technical Architecture, CI/CD & DevOps
*   James - Project Lead, LLM Integration & API Utilities

FlashCard Hub is a web application designed to help users create and manage flashcards for effective learning. It successfully integrates AI and direct data extraction to offer a powerful and efficient solution for creating and managing study materials. The application offers two primary methods for flashcard generation: direct content extraction from Wikipedia articles and AI-powered generation using Google's Gemini model for more customized and nuanced flashcards. This application is built with Flask, featuring a stylish and responsive layout using Tailwind CSS, and is structured for clean separation of concerns, making it easy to maintain and extend. We've addressed the challenge of transforming information into effective study aids quickly and intelligently, making learning more accessible and productive.

## Features
- **Automated Flashcard Creation**: Drastically reduces manual effort in generating study materials.
- **Intelligent Content Generation**: Leverages Google's Gemini LLM for high-quality, context-aware flashcards.
- **User-Friendly Deck Management**: Provides an organized and intuitive platform for creating, viewing, and managing flashcard decks.
- **Versatile Generation Methods**: Supports both direct content extraction from Wikipedia and LLM-enhanced generation for tailored study aids.
- Responsive design using Tailwind CSS
- Modular structure with blueprints for routes
- Custom error pages (404 and 500)
- Dashboard for user-specific data
- Flashcard deck creation and management
- Flashcard generation via Wikipedia extraction
- Flashcard generation via LLM (Google Gemini)
- Easy to customize and extend

## Key Components
*   **Frontend**: Built with Flask (serving HTML templates), Tailwind CSS, and JavaScript, providing a responsive user interface for creating, viewing, and managing flashcards and decks.
*   **Backend**: A Flask-based server handling user authentication (Flask-Login), data persistence (SQLite with Flask-SQLAlchemy), form handling (Flask-WTF), and overall business logic.
*   **Flashcard Generation Modules**:
    *   `app/utils/wikipedia_agent.py`: Implements functionality to search Wikipedia and extract content suitable for flashcards.
    *   `app/utils/llm_flashcard_generator.py`: Utilizes Google's Gemini model (via `app/utils/llm_agent.py`) to generate flashcards based on user-provided topics or text.
*   **Database**: Employs SQLAlchemy ORM with a SQLite database (`instance/site.db`) to store user accounts, flashcard decks, and individual flashcards. Database migrations are managed by Flask-Migrate.
*   **Environment Configuration**: Uses a `.env` file for managing sensitive information and application settings (API keys, secret keys, debug modes).
*   **Dockerization**: Includes a `Dockerfile` and `docker-compose.yaml` for building and running the application in a containerized environment, ensuring consistency and ease of deployment.

## Local Development Setup
(This heading replaces "## Installation". Content for points 1-4 remains the same, point 5 is updated.)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FlashCard-Hub.git
   cd FlashCard-Hub
   ```
   *(Note: Update with the actual repository URL if available, otherwise keep as placeholder)*
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   Create a `.env` file in the project root directory by copying the example `.env.example` (if provided) or creating it from scratch. Populate it with necessary variables:
   ```env
   FLASK_APP=run.py
   FLASK_DEBUG=True # Set to False in production
   SECRET_KEY='your_super_secret_key_here_please_change_me'
   GOOGLE_API_KEY='your_google_gemini_api_key_here'
   # SQLALCHEMY_DATABASE_URI='sqlite:///instance/site.db' # Default, or specify another path
   ```
   Ensure `GOOGLE_API_KEY` is correctly set to use the LLM-based flashcard generation feature.

## Running Locally (without Docker)
(This heading replaces "## Running the Application". Content is slightly modified for clarity.)
To run the application directly using Python after completing the local development setup:
```bash
flask run
# Alternatively, if your run.py is set up for it:
# python run.py
```
The application will typically be accessible at `http://127.0.0.1:5000`.

## Running with Docker
The application can be easily built and run using Docker, which encapsulates the application and its dependencies.

**1. Ensure Docker is installed and running on your system.**

**2. Build the Docker image:**
   From the project root directory (where `Dockerfile` is located):
   ```bash
   docker build -t flashcard-hub .
   ```

**3. Run the Docker container:**
   You'll need to pass your environment variables to the container. The recommended way is using an `.env` file.
   ```bash
   docker run -p 5000:5000 --env-file .env flashcard-hub
   ```
   This command maps port 5000 of the container to port 5000 on your host and loads environment variables from the `.env` file located in your project root.
   The application will be accessible at `http://localhost:5000`.

**Using Docker Compose (Recommended for development and multi-container setups):**
This project includes a `docker-compose.yaml` file for streamlined Docker management.
1.  Ensure your `.env` file is correctly set up in the project root.
2.  Build and start the services (including the web application):
    ```bash
    docker-compose up --build
    ```
    (The `--build` flag is needed the first time or when `Dockerfile` or application dependencies change.)
3.  To run in detached mode (in the background):
    ```bash
    docker-compose up -d
    ```
4.  To stop the services:
    ```bash
    docker-compose down
    ```
The `docker-compose.yaml` is configured to use the `.env` file for environment variables.

## Docker Hub Image
A pre-built Docker image is available on Docker Hub:
`jamestcss506/flashcard-hub:latest`

You can pull it using:
```bash
docker pull jamestcss506/flashcard-hub:latest
```

To run the pulled image (remember to provide necessary environment variables, e.g., via an `.env` file or `-e` flags):
```bash
# Example using --env-file (recommended if you have an .env file in the directory where you run this command)
# Ensure your .env file has FLASK_DEBUG=False for production images if applicable.
docker run -p 5000:5000 --env-file .env jamestcss506/flashcard-hub:latest

# Example using -e flags (replace with your actual values):
# docker run -p 5000:5000 \
#   -e FLASK_APP="run.py" \
#   -e FLASK_DEBUG="False" \
#   -e SECRET_KEY="your_production_secret_key" \
#   -e GOOGLE_API_KEY="your_google_api_key" \
#   jamestcss506/flashcard-hub:latest
```
Link: [https://hub.docker.com/r/jamestcss506/flashcard-hub](https://hub.docker.com/r/jamestcss506/flashcard-hub)

## Individual Contributions
*   **Maddy:** Led the frontend development, including the design and implementation of user interface elements, animations for the flashcard decks, and overall user experience.
*   **Sean:** Responsible for the technical architecture of the project. Set up the CI/CD pipeline using GitHub Actions, and configured Nginx with the PostgreSQL database for robust deployment.
*   **James:** Conceived the project idea. Developed the core utilities for integrating with the Google Gemini LLM for AI-powered flashcard generation and the Wikipedia API for content extraction.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
