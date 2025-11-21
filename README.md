# Vehicle Maintenance System with AI Intelligence 🚗🤖

An advanced web application for vehicle maintenance tracking powered by **Google Gemini AI**, featuring intelligent maintenance suggestions, automated categorization, and predictive analytics. Built with Flask and modern web technologies.

## 🌟 Key Features

### Core Functionality
- **Multi-Vehicle Management**: Register and track multiple vehicles with detailed specifications
- **Comprehensive Maintenance Tracking**: Log all maintenance activities with costs and notes
- **Mileage Monitoring**: Track vehicle usage and maintenance intervals
- **Mechanic Directory**: Manage preferred mechanics and workshops
- **User Authentication**: Secure multi-user support with individual dashboards
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### 🤖 AI-Powered Features (Google Gemini Integration)

#### 1. **Intelligent Maintenance Suggestions**
- **Context-Aware Recommendations**: AI analyzes vehicle mileage, age, type, and engine specifications to suggest appropriate maintenance tasks
- **Predictive Maintenance**: Anticipates upcoming maintenance needs based on:
  - Current mileage vs. manufacturer recommendations
  - Time since last service
  - Vehicle age and condition
  - Driving patterns and usage
- **Smart Scheduling**: Recommends optimal maintenance intervals customized for each vehicle type
- **Priority-Based Suggestions**: Ranks maintenance tasks by urgency and importance

#### 2. **Automated Category Classification**
- **Intelligent Categorization**: AI automatically categorizes maintenance into:
  - Oil System (Aceite)
  - Brakes (Frenos)
  - Engine (Motor)
  - Transmission (Transmisión)
  - Suspension (Suspensión)
  - Electrical (Eléctrico)
  - Tires (Llantas)
  - Body (Carrocería)
- **Description Analysis**: Natural language processing to understand maintenance descriptions
- **Learning Capability**: Improves suggestions based on user confirmations

#### 3. **Maintenance Delay Impact Analysis**
- **Risk Assessment**: Evaluates safety and mechanical consequences of delaying maintenance
- **Cost Analysis**: Compares prevention costs vs. potential repair expenses
- **Component Wear Prediction**: Estimates impact on related vehicle systems
- **Safety Prioritization**: Highlights critical safety-related maintenance

#### 4. **Multi-Language Support**
- **Bilingual Operation**: Seamlessly works in English and Spanish
- **Technical Translation**: Maintains accuracy for automotive terminology
- **Regional Adaptation**: Adjusts for regional maintenance practices

## 🛠️ Technology Stack

- **Backend**: Python Flask Framework
- **AI Engine**: Google Gemini AI (gemini-2.0-flash-exp model)
- **Database**: SQLite with optimized schema
- **Frontend**: Bootstrap 5, JavaScript, jQuery
- **Authentication**: Werkzeug Security with password hashing
- **Testing**: Playwright E2E Testing Suite (10/10 tests passing)
- **API Integration**: RESTful endpoints for AI services

## 📋 Requirements

- Python 3.8 or higher
- SQLite3
- Google Gemini API Key (Free tier: 1,500 requests/day)
- Python libraries specified in requirements.txt

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mauricio222/vehicle-maintenance-app.git
   cd vehicle-maintenance-app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
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

This project is licensed under the [MIT License](LICENSE).

## 🧪 Testing

The application includes a comprehensive E2E test suite using Playwright:

```bash
# Install test dependencies
pip install pytest pytest-playwright

# Install Playwright browsers
playwright install chromium

# Run E2E tests
pytest tests/e2e/test_vehicle_maintenance_e2e_final.py -v
```

Test coverage includes:
- User authentication (login/logout)
- Vehicle CRUD operations
- Maintenance record management
- Complete user journey flows
- Responsive design verification
- AI feature integration tests

## 🤖 AI Features Deep Dive

### How Google Gemini AI Enhances Your Maintenance Experience

1. **Smart Maintenance Predictions**
   - Analyzes vehicle specifications (make, model, year, engine type)
   - Considers current mileage and time since last service
   - Provides personalized maintenance schedules
   - Adapts recommendations based on driving conditions

2. **Intelligent Cost Analysis**
   - Estimates maintenance costs based on vehicle type
   - Compares preventive vs. reactive maintenance expenses
   - Helps budget for upcoming services
   - Tracks cost trends over time

3. **Natural Language Processing**
   - Understands maintenance descriptions in plain language
   - Works seamlessly in English and Spanish
   - Automatically extracts key information from notes
   - Suggests related maintenance tasks

4. **Predictive Analytics**
   - Forecasts component wear based on usage patterns
   - Identifies potential issues before they become critical
   - Recommends preventive actions
   - Learns from historical maintenance data

### API Integration

The application integrates with Google Gemini AI through:
- **Model**: gemini-2.0-flash-exp
- **Rate Limit**: 1,500 requests/day (free tier)
- **Response Time**: < 2 seconds average
- **Fallback**: Graceful degradation if API unavailable

## 📊 Database Schema

- **Usuario** (Users): Authentication and user management
- **Vehiculo** (Vehicles): Vehicle specifications and ownership
- **Mantenimiento** (Maintenance): Service history and records
- **Mecánico** (Mechanics): Service provider directory
- **Tipo_Mantenimiento** (Maintenance Types): Category definitions

## 🔒 Security Features

- Password hashing with Werkzeug security
- Session-based authentication
- SQL injection prevention
- XSS protection
- CSRF tokens for forms
- Secure API key management

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop (1920x1080 and above)
- Tablet (768x1024)
- Mobile (320x568 and above)

## 🎯 Demo Access

A clean demo environment is available:

```
URL: http://localhost:5000
Username: admin
Password: admin
```

The demo database includes:
- Admin user account
- Empty vehicle registry (ready for testing)
- Clean maintenance history
- No test data artifacts

## 🚧 Roadmap

Future enhancements planned:
- [ ] Mobile app development
- [ ] Cloud synchronization
- [ ] Advanced reporting dashboard
- [ ] Integration with OBD-II devices
- [ ] Maintenance reminder notifications
- [ ] Multi-language support expansion
- [ ] Fleet management features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or suggestions, please open an issue in this repository.
