# Modern Flask App

This is a modern Flask application designed with a stylish and responsive layout using Tailwind CSS. The application is structured to provide a clean separation of concerns, making it easy to maintain and extend.

## Features

- Responsive design using Tailwind CSS
- Modular structure with blueprints for routes
- Custom error pages (404 and 500)
- Dashboard for user-specific data
- Easy to customize and extend

## Project Structure

```
modern-flask-app
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── models
│   │   └── __init__.py
│   ├── routes
│   │   └── __init__.py
│   ├── static
│   │   ├── css
│   │   │   ├── main.css
│   │   │   └── tailwind.css
│   │   ├── js
│   │   │   └── main.js
│   │   └── img
│   │       └── logo.svg
│   ├── templates
│   │   ├── base.html
│   │   ├── components
│   │   │   ├── footer.html
│   │   │   ├── navbar.html
│   │   │   └── sidebar.html
│   │   ├── errors
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── pages
│   │       ├── index.html
│   │       └── dashboard.html
│   └── utils
│       └── __init__.py
├── tests
│   └── __init__.py
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/modern-flask-app.git
   cd modern-flask-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables in the `.env` file.

## Running the Application

To run the application, execute the following command:

```
python run.py
```

The application will be accessible at `http://127.0.0.1:5000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.