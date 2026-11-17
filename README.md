
# Job Application Tracker

## Project Description

The Job Application Tracker is a web application that helps users organize and manage their job search.

Users can manage companies, job listings, applications, and professional contacts. The application also includes a Job Match feature that compares user-entered skills against job requirements and ranks jobs by match percentage.

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- Bootstrap
- JavaScript

## Features

- Dashboard displaying database statistics
- Create, view, edit, and delete companies
- Create, view, edit, and delete job listings
- Create, view, edit, and delete applications
- Create, view, edit, and delete contacts
- Job Match feature that ranks jobs based on matching skills

## Database

The application uses a MySQL database named `job_tracker`.

The database contains four tables:

- companies
- jobs
- applications
- contacts

The database structure can be created by executing `schema.sql` in MySQL Workbench.

## Installation Instructions

### 1. Install Requirements

Install Python 3 and MySQL Server.

### 2. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd job_tracker
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

1. Open MySQL Workbench.
2. Connect to your MySQL server.
3. Open `schema.sql`.
4. Execute the script to create the database and tables.

### 5. Configure Database Connection

Open `database.py` and enter your own MySQL username and password.

### 6. Run the Application

```bash
python app.py
```

### 7. Open the Application

Visit:

http://127.0.0.1:5000

## Project Structure

```text
job_tracker/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── AI_USAGE.md
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── company_form.html
│   ├── jobs.html
│   ├── job_form.html
│   ├── applications.html
│   ├── application_form.html
│   ├── contacts.html
│   ├── contact_form.html
│   └── job_match.html
│
└── static/
    └── style.css
```

## Author

Job Application Tracker Course Project
