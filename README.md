# Vehicle Maintenance System

Web application built with Flask for logging and tracking vehicle maintenance.

## Features

- Register vehicles with technical details
- Track performed maintenance
- Log mileage
- Reminders for upcoming maintenance
- Mechanic management
- User authentication system
- AI integration (Gemini) for maintenance suggestions

## Requirements

- Python 3.7 or higher
- SQLite3
- Python libraries specified in requirements.txt

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mauricio222/vehicle-maintenance-app-english.git
   cd vehicle-maintenance-app-english
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_SECRET_KEY=your_secret_key
   GEMINI_API_KEY=your_gemini_api_key
   DB_PATH=mantenimiento.db
   ```

5. Initialize the database:
   ```
   python initialize_db.py
   ```

## Usage

1. Run the application:
   ```
   python flask_app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Register a new user and start using the application.

## Project Structure

- `flask_app.py`: Main Flask application
- `initialize_db.py`: Script to initialize the database
- `templates/`: HTML template files
- `requirements.txt`: Dependency list
- `mantenimiento.db`: SQLite database (automatically created)

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, please open an issue in this repository.