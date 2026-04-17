# Flight Search Web Application
CS 6083 – Database Design | Spring 2026

A Flask web application that allows users to search for flights and view seat availability, backed by a PostgreSQL database.

## Features

- Search flights by origin airport, destination airport, and date range
- View all matching flights with flight number, date, route, departure time, and airline
- Click any flight to see real-time seat availability (capacity, booked seats, available seats)

## Project Structure

```
flights_app/
├── app.py               # Flask backend and database queries
├── templates/
│   └── index.html       # Frontend HTML, CSS, and JavaScript
├── .env                 # Database credentials (not committed to Git)
├── .gitignore
└── README.md
```

## Database Schema

The app uses a PostgreSQL database with the following tables:

- `Airport` — airport code, name, city, country
- `Aircraft` — plane type and capacity
- `FlightService` — scheduled route info (flight number, airline, origin, destination, departure time, duration)
- `Flight` — actual flight instances (flight number, departure date, plane type)
- `Passenger` — passenger ID and name
- `Booking` — maps passengers to flights with seat numbers

## Prerequisites

- Python 3.10+
- PostgreSQL 16+ (via Homebrew or official installer)
- pip

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/flights-app.git
cd flights-app
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask psycopg2-binary python-dotenv
```

### 4. Set up the database

Start PostgreSQL, then create the database and load the schema and data:

```bash
psql -U postgres
```

```sql
CREATE DATABASE flights_db;
\c flights_db
\i /path/to/flights.sql
\q
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```
DB_NAME=flights_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 6. Run the application

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

## Usage

1. Enter a source airport code (e.g. `JFK`) and destination airport code (e.g. `LAX`)
2. Select a date range
3. Click **Search Flights**
4. Click any flight row to expand and see seat availability

## Sample Test Cases

| Origin | Destination | Date Range | Expected Result |
|--------|-------------|------------|-----------------|
| JFK | LAX | 2025-12-29 to 2025-12-31 | 3 flights (AA101, AA101, AA205) |
| SFO | ORD | 2025-12-31 to 2025-12-31 | 1 flight, fully booked (UA302) |
| ATL | MIA | 2025-12-31 to 2025-12-31 | 1 flight, 1 seat available (DL410) |
| LAX | JFK | 2025-12-29 to 2025-12-31 | No flights found |

## Security

- Database credentials are stored in a `.env` file and excluded from version control via `.gitignore`
- All SQL queries use parameterized statements to prevent SQL injection
