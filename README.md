# Contribution Tracker API

A lightweight, high-performance REST API built with **FastAPI** to manage **Users**, **Events**, and **Contributions**. The API bridges request routing to an underlying backend service backed by a **MySQL Database** and automatically generates interactive **Swagger UI** and **ReDoc** documentation.

---

## 🚀 Features

- **User Management (`/user`)**: Register new users, query user profiles, list all users, and delete user accounts persisted in MySQL.
- **Event Management (`/event`)**: Register events associated with user IDs, retrieve event details, list events, and delete events stored in MySQL.
- **Contribution Tracking (`/contribution`)**: Register financial or resource contributions tied to events, generate event contribution reports, update contribution details, list contributions by event, and delete entries stored in MySQL.
- **MySQL Database Backend**: Relational database storage for persistent data integrity across Users, Events, and Contributions.
- **Interactive Swagger UI**: Explore and test API endpoints directly from your browser at `/docs`.
- **No Authentication Required**: Simple, open REST API design for quick integration and local development.


---

## 📁 Project Structure

```
contribution-tracker-python-client/
├── actions/
│   ├── user_tracker.py          # User management endpoints & schemas
│   ├── event_tracker.py         # Event management endpoints & schemas
│   └── contribution_tracker.py  # Contribution tracking endpoints & schemas
├── config.py                    # Environment & configuration settings
├── main.py                      # FastAPI application entrypoint
└── requirements.txt             # Python dependencies
```

---

## 🛠️ Prerequisites & Installation

### 1. Requirements
Ensure Python 3.10+ is installed.

### 2. Install Dependencies
Install all required libraries:

```bash
pip install -r requirements.txt
```

*Required packages:*
- `fastapi`
- `uvicorn`
- `requests`
- `pydantic`

---

## ⚙️ Configuration

The application forwards requests to a core backend API. The base URL can be configured using an environment variable `API_BASE_URL` or a `.env` file.

### `.env` Setup
Copy [.env.example](file:///c:/Users/jai08/projects/contribution-tracker-python-client/.env.example) to `.env`:
```bash
cp .env.example .env
```

- **Default Base URL**: `http://127.0.0.1:8005`

To override the backend address on Windows (PowerShell):
```powershell
$env:API_BASE_URL="http://127.0.0.1:8005"
```

Or on Linux/macOS:
```bash
export API_BASE_URL="http://127.0.0.1:8005"
```


---

## 🗄️ Database Architecture & Credentials (MySQL)

### Database Connection Flow
1. **Backend Service (`http://127.0.0.1:8005`)**: The core backend API service connects directly to the **MySQL Database** where tables (`users`, `events`, `contributions`) are created and persisted.
2. **FastAPI Client App (This Project)**: Routes requests via `BASE_URL` in [config.py](file:///c:/Users/jai08/projects/contribution-tracker-python-client/config.py) to the backend service.

### Database Credentials Configuration
Database credentials (Host, Port, Username, Password, Database Name) are configured in the **core backend service** (port 8005). 

If you choose to connect directly to MySQL from this FastAPI app (e.g., using SQLAlchemy / PyMySQL), add the following environment variables to a `.env` file:

```env
# Optional: Direct MySQL Database Credentials
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=contribution_tracker_db
```



---

## 🏃 Running the Application

Start the API server using Python directly:

```bash
python main.py
```

Or run via Uvicorn with auto-reload enabled:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📖 API Documentation & Interactive Testing

Once the server is running on `http://127.0.0.1:8000`, open your browser to access:

- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 API Endpoints Overview

### 1. User Tracker (`/user`)

| Method | Endpoint | Description | Request Body / Parameters |
| :--- | :--- | :--- | :--- |
| `POST` | `/user/user_registration` | Register a new user | Body: `name`, `email`, `dob` *(opt)*, `address` *(opt)*, `mobile_number` *(opt)* |
| `GET` | `/user/{user_id}` | Fetch user details by ID | Path: `user_id` (int) |
| `DELETE` | `/user/{user_id}` | Delete a user by ID | Path: `user_id` (int) |
| `GET` | `/user/` | List all registered users | None |

#### User Registration Request Example:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "dob": "1995-05-15",
  "address": "123 Main Street",
  "mobile_number": "9876543210"
}
```

---

### 2. Event Tracker (`/event`)

| Method | Endpoint | Description | Request Body / Parameters |
| :--- | :--- | :--- | :--- |
| `POST` | `/event/event_registration` | Register a new event | Body: `name`, `date`, `location`, `user_id` |
| `GET` | `/event/{event_id}` | Fetch event details by ID | Path: `event_id` (int) |
| `DELETE` | `/event/{event_id}` | Delete an event by ID | Path: `event_id` (int) |
| `GET` | `/event/` | List all registered events | None |

#### Event Registration Request Example:
```json
{
  "name": "Annual Gathering",
  "date": "2026-12-01",
  "location": "Community Center",
  "user_id": 1
}
```

---

### 3. Contribution Tracker (`/contribution`)

| Method | Endpoint | Description | Request Body / Parameters |
| :--- | :--- | :--- | :--- |
| `POST` | `/contribution/contributions_registration` | Register a new contribution | Body: `event_id`, `amount`, `name` *(opt)*, `address` *(opt)*, `mobile_number` *(opt)* |
| `GET` | `/contribution/{contribution_id}` | Fetch contribution by ID | Path: `contribution_id` (int) |
| `PUT` | `/contribution/{contribution_id}` | Update contribution details | Body: `event_id`, `name`, `address`, `amount`, `mobile_number` |
| `DELETE` | `/contribution/{contribution_id}` | Delete contribution by ID | Path: `contribution_id` (int) |
| `GET` | `/contribution/read_all/{event_id}` | List all contributions for an event | Path: `event_id` (str/int) |


#### Contribution Registration Request Example:
```json
{
  "event_id": 1,
  "amount": 500,
  "name": "Jane Smith",
  "address": "456 Park Avenue",
  "mobile_number": "9123456789"
}
```

---

## 🛡️ Authentication Note

This API current operates without an authentication module (open access). All endpoints can be called directly without bearer tokens or API keys.
