# Airport Ground Management System

A Flask-based web application for managing airport ground operations through a centralized dashboard, with MySQL database integration.

**Live Demo:** [Open the deployed application](https://airport-ground-management-system.onrender.com)  
**Source Code:** [GitHub Repository](https://github.com/harshitabalpande/Airport-Ground-Management-System)

---

## Project Overview

The Airport Ground Management System is an academic software engineering project designed to organize key airport ground operations in one web application. It provides a centralized interface for managing flight information, gate allocations, ground staff, baggage handling, and aircraft fueling records.

The application demonstrates full-stack web development using Python and Flask, relational database integration with MySQL, and a responsive user interface built with HTML and CSS.

## Key Features

- **User Authentication:** User registration and login functionality.
- **Centralized Dashboard:** Navigation to the main ground-operation modules.
- **Flight Management:** View and manage flight details, schedules, and status.
- **Gate Allocation:** Maintain gate assignments for flights.
- **Ground Staff Management:** Manage staff details, departments, roles, and availability.
- **Baggage Management:** Maintain baggage handling records and processing status.
- **Fuel Operations:** Manage aircraft fueling records, quantities, and status.
- **Login History:** Record successful and unsuccessful login activity and track logout timestamps.
- **Responsive Interface:** Clean, light-themed interface designed for usability across screen sizes.

## Technology Stack

| Technology | Role |
|---|---|
| Python | Application logic |
| Flask | Backend web framework |
| MySQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layout |
| Git | Version control |
| GitHub | Source code hosting |
| Render | Web application hosting |
| Railway | Hosted MySQL database |

## Application Modules

| Module | Description |
|---|---|
| Authentication | User registration and login |
| Dashboard | Central navigation for operational tasks |
| Flight Management | Flight information and status |
| Gate Allocation | Flight-to-gate assignments |
| Ground Staff | Staff records and availability |
| Baggage Management | Baggage handling records |
| Fuel Management | Aircraft fueling records |
| Reports | Operational summaries and grouped status information |
| Login History | Login and logout activity tracking |

## Project Structure

```text
Airport-Ground-Management-System/
├── 01_Dataset/
│   └── airline_ground_management_system_dataset.csv
├── 02_Documentation/
│   ├── Objectives.md
│   ├── Problem_Statement.md
│   ├── Project_Proposal.md
│   └── SRS.md
├── 04_Database/
│   └── Database_Design.md
├── 07_Testing/
│   └── Test_Cases.md
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── flights.html
│   ├── edit_flight.html
│   ├── gate_allocation.html
│   ├── ground_staff.html
│   ├── edit_ground_staff.html
│   ├── baggage.html
│   ├── edit_baggage.html
│   ├── fuel_management.html
│   ├── edit_fuel.html
│   └── reports.html
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

Install the following software before running the project locally:

- Python 3
- MySQL Server
- MySQL Workbench (recommended)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/harshitabalpande/Airport-Ground-Management-System.git
cd Airport-Ground-Management-System
```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Database

Create a MySQL database named `airport_ground_management` and create the required tables using the project's database design.

Set the following environment variables for your local environment:

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL server hostname |
| `DB_PORT` | MySQL server port |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_NAME` | Database name |
| `SECRET_KEY` | Secret key used by Flask sessions |

Use your own database credentials. Never publish database passwords, secret keys, or connection URLs containing credentials in the repository.

### 5. Run the Application

```powershell
python app.py
```

Open the application in your browser:

`http://127.0.0.1:5000`

## Deployment

The project source code is hosted on GitHub. The deployment setup uses Render for the Flask web application and Railway for the MySQL database.

For the deployed application to work correctly, ensure that:

- The web service uses the correct production start command.
- All required environment variables are configured in the hosting platform.
- The hosted MySQL database contains the required tables.
- The application can connect securely to the database.

**Live application:** Replace the placeholder URL at the top of this README with the actual public URL shown on the Render service dashboard.

## Dataset

The repository includes a sample dataset for demonstration and academic purposes. The data is illustrative and has not been verified as real-world airport operational data.

It should not be used to make actual airport operational or safety-critical decisions.

## Learning Outcomes

This project provides practical exposure to:

- Developing a web application with Flask.
- Connecting a Python application to a MySQL database.
- Implementing database operations for multiple management modules.
- Building HTML templates and styling a web interface with CSS.
- Using Git and GitHub for version control.
- Configuring environment variables and deploying a web application.

## Future Improvements

Potential enhancements include:

- Stronger authorization and role-based access controls.
- Improved form validation and consistent error handling.
- More detailed operational analytics and visual reports.
- Automated testing and deployment checks.
- Additional security and reliability hardening.

## Disclaimer

This application was developed for academic learning and portfolio demonstration. It is not intended for production use at a real airport without further security assessment, comprehensive testing, reliability improvements, and operational validation.

## Author

**Harshita Balpande**

GitHub: [@harshitabalpande](https://github.com/harshitabalpande)
