# 🎯 Job Application Tracker (Python 3 & SQLite OOP)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-green.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Object--Oriented-orange.svg)](#object-oriented-programming-architecture)
[![Build Status](https://img.shields.io/badge/Tests-Passing%20(8%2F8)-brightgreen.svg)](#testing-and-validation)

> A production-grade, terminal-based **Job Application Tracker** built with **Python 3**, **SQLite**, and clean **Object-Oriented Programming (OOP)**. Designed for students, graduates, and job seekers to organize applications, track interview rounds, sort by priority, and analyze recruitment pipeline metrics.

---

## 📑 Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Database Architecture & Schema](#database-architecture--schema)
6. [Object-Oriented Programming (OOP) Design](#object-oriented-programming-oop-design)
7. [Installation & Setup](#installation--setup)
8. [How to Run the Application](#how-to-run-the-application)
9. [Sample CLI Output](#sample-cli-output)
10. [Priority Sorting Guide](#priority-sorting-guide)
11. [Testing & Validation](#testing-and-validation)
12. [Git Version Control Commands](#git-version-control-commands)
13. [Future Roadmap](#future-roadmap)

---

## 🌟 Project Overview

Searching for internships and full-time software engineering roles involves dozens of applications, varying deadlines, multiple interview rounds, and recruiter communications. Spreadsheets become messy and lack validation, while web platforms can be bloated.

This **Job Application Tracker** provides a lightweight, permanent, and resilient solution using Python's native SQLite database. It incorporates **application priority tagging (High, Medium, Low)** so users can focus on their dream companies first.

---

## ✨ Key Features

### 1. Application Management (CRUD)
- **Add Applications:** Capture company name, job role, location, application date, job type (Internship, Full-time, Part-time, Contract), status, priority, salary/stipend, job link, and notes.
- **View Applications:** Formatted Unicode tables with column auto-sizing and aligned status badges.
- **Priority Sorting:** Sort applications with 1 click based on **High ➔ Medium ➔ Low** priority order (or reverse).
- **Multi-Field Search:** Instant filtering by Company Name, Job Role, Status, Priority, or universal keyword search.
- **Safe Updates:** Update individual fields (status, priority, salary, notes) or full profiles with timestamps.
- **Destructive Operation Protection:** Requires explicit user confirmation (`[y/N]`) before deleting any record.

### 2. Interview Lifecycle Tracking
- Log scheduled interview dates.
- Track progression through rounds (Screening, Technical Coding, System Design, Behavioral).
- Store interview questions, recruiter notes, and interviewer feedback.

### 3. Pipeline Analytics Dashboard
- Total applications submitted and active pipeline count.
- **Selection (Offer) Success Rate** and **Interview Conversion Rate** calculations.
- Visual ASCII progress bars and funnel breakdowns.
- Priority distribution metrics (High vs Medium vs Low ratio).

### 4. Zero External Dependencies
- Runs natively on any computer with Python 3.8+ installed.
- No `pip install` required — built entirely with standard library tools (`sqlite3`, `unittest`, `abc`, `enum`).

---

## 🛠️ Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.8 - 3.12+ | Clean syntax, robust standard library, strong OOP support |
| **Database Engine** | SQLite 3 | Serverless, zero-configuration, ACID-compliant permanent file storage |
| **Architecture** | Object-Oriented (OOP) | Separation of data models, database management, and UI presentation |
| **Testing Framework** | `unittest` (Standard Library) | Automated test suite verifying CRUD, schema migrations, and sorting |

---

## 📁 Project Structure

```text
job-application-tracker/
│
├── main.py                  # CLI application entry point and interactive navigation
├── database.py              # SQLite DatabaseManager with parameterized queries & migrations
├── models.py                # Domain models (JobApplication, Priority, ApplicationStatus)
├── tracker.py               # Coordinator handling business logic and workflows
├── dashboard.py             # Analytics engine, KPI calculations, and ASCII visualizations
├── utils.py                 # ANSI colors, table formatting, and input validation
├── requirements.txt         # Minimalist dependency manifest (std-lib native)
├── README.md                # Comprehensive portfolio documentation
├── .gitignore               # Excludes bytecode, temporary files, and local databases
│
├── tests/
│   └── test_tracker.py      # Automated unit tests covering models, DB, and priority sorting
│
└── data/
    └── jobs.db              # Permanent SQLite database (created automatically on first launch)
```

---

## 🗄️ Database Architecture & Schema

The application uses an SQLite database stored in `data/jobs.db`. It features **automatic schema initialization and dynamic schema migration** (ensuring the `priority` column is automatically added even if an older database file exists).

### Entity-Relationship Schema (`applications` table)

```sql
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT DEFAULT 'Remote',
    application_date TEXT NOT NULL,
    job_type TEXT NOT NULL,
    status TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'Medium',        -- 'High', 'Medium', or 'Low'
    salary_or_stipend TEXT DEFAULT 'Not Disclosed',
    job_description TEXT DEFAULT '',
    link TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    interview_date TEXT DEFAULT 'None',
    interview_rounds INTEGER DEFAULT 0,
    interview_notes TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_company ON applications(company);
CREATE INDEX IF NOT EXISTS idx_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_priority ON applications(priority);
CREATE INDEX IF NOT EXISTS idx_app_date ON applications(application_date);
```

### SQL Injection Prevention
All database methods in `DatabaseManager` use **parameterized queries** (`?` placeholders). Raw user strings are never concatenated directly into SQL statements.

---

## 🧩 Object-Oriented Programming (OOP) Design

This project demonstrates core software engineering principles:

### 1. Encapsulation
- `JobApplication` keeps its raw fields private/protected (`_company`, `_role`, `_priority`, etc.).
- Access is controlled via `@property` getters and setters that enforce validation (e.g. non-empty company names, valid priority strings).

### 2. Inheritance
- `BaseRecord` is an abstract base class (`abc.ABC`) providing foundational identifier management (`id`, `created_at`).
- `JobApplication` inherits from `BaseRecord` and implements required abstract methods.

### 3. Polymorphism
- `BaseRecord.summary()` defines an abstract interface.
- Subclasses implement their own contextual string representation (e.g., `JobApplication.summary()`).

### 4. Separation of Concerns & Loose Coupling
- **Data Layer:** `DatabaseManager` handles connection management, transactions, and SQL queries.
- **Domain Layer:** `models.py` contains business entities and validation rules.
- **Service/Logic Layer:** `JobTracker` and `Dashboard` coordinate workflows and compute analytics.
- **Presentation Layer:** `main.py` and `utils.py` handle user interaction and formatting.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your machine.
- Git (optional, for cloning).

### 1. Clone or Download the Repository
```bash
git clone https://github.com/your-username/job-application-tracker.git
cd job-application-tracker
```

### 2. (Optional) Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Verify Python Version
```bash
python3 --version
```

---

## 💻 How to Run the Application

Execute the main script from the root directory:

```bash
python3 main.py
```

The database directory `data/` and `data/jobs.db` will be initialized automatically. If launched for the first time, realistic sample applications (Google, Stripe, Spotify, etc.) are pre-populated so you can immediately explore sorting and dashboard metrics!

---

## 🖥️ Sample CLI Output

### 1. Main Navigation Menu
```text
╔═══════════════════════════════════════════════════════════════════════╗
║                   JOB APPLICATION TRACKER (OOP)                       ║
║                 OOP Python & SQLite CLI Edition                       ║
╚═══════════════════════════════════════════════════════════════════════╝

Main Navigation Menu:
  1) Add Job Application
  2) View Applications (with Priority Sorting)
  3) Search Applications (Company, Role, Status, Priority)
  4) Update Application
  5) Delete Application (with confirmation)
  6) 📊 Dashboard & Analytics
  7) 🎙️ Interview Management
  8) 🔄 Seed Demo Applications
  9) 🚪 Exit Application
─────────────────────────────────────────────────────────────────────────
Select an option (1-9):
```

### 2. Priority-Sorted Applications Table (Option 2 ➔ 2)
```text
▶ ALL JOB APPLICATIONS (5 TOTAL) — SORTED BY: PRIORITY (ASC) [HIGH ➔ MEDIUM ➔ LOW]
───────────────────────────────────────────────────────────────────────────────
┌────┬──────────────┬──────────────────────────┬────────────┬──────────┬─────────────────────┬────────────┬────────────────────────┐
│ ID │ Company      │ Job Role                 │    Type    │ Priority │ Status              │    Date    │ Location               │
├────┼──────────────┼──────────────────────────┼────────────┼──────────┼─────────────────────┼────────────┼────────────────────────┤
│ 1  │ Google       │ Software Eng. Intern     │ Internship │   High   │ Interview Scheduled │ 2026-10-15 │ Mountain View, CA      │
│ 2  │ Stripe       │ Backend Software Eng.    │ Full-time  │   High   │ Applied             │ 2026-10-20 │ Remote (US)            │
│ 3  │ Spotify      │ Data Engineer Intern     │ Internship │   High   │ Selected            │ 2026-10-02 │ New York, NY           │
│ 4  │ Shopify      │ Junior Python Developer  │ Full-time  │  Medium  │ Pending             │ 2026-10-25 │ Remote                 │
│ 5  │ TechCorp     │ Full Stack Developer     │ Full-time  │   Low    │ Rejected            │ 2026-09-28 │ Austin, TX             │
└────┴──────────────┴──────────────────────────┴────────────┴──────────┴─────────────────────┴────────────┴────────────────────────┘
```

### 3. Analytics Dashboard (Option 6)
```text
╔═══════════════════════════════════════════════════════════════════════╗
║                    APPLICATIONS ANALYTICS DASHBOARD                   ║
╚═══════════════════════════════════════════════════════════════════════╝

── 📊 KEY PERFORMANCE INDICATORS ────────────────────────────────────────
  • Total Applications Submitted:  5
  • Active in Pipeline:            3
  • Interview Conversion Rate:     [██████████░░░░░░░░░░░░░░] 40.0%
  • Final Selection (Offer) Rate:  [█████░░░░░░░░░░░░░░░░░░░] 20.0%

── 📈 PIPELINE STATUS BREAKDOWN ────────────────────────────────────────
┌─────────────────────┬───────┬────────────┬────────────────────────┐
│ Status Stage        │ Count │ Percentage │ Funnel Visual          │
├─────────────────────┼───────┼────────────┼────────────────────────┤
│ Applied             │     1 │      20.0% │ [████░░░░░░░░░░░░░░░░] │
│ Interview Scheduled │     1 │      20.0% │ [████░░░░░░░░░░░░░░░░] │
│ Selected (Offer)    │     1 │      20.0% │ [████░░░░░░░░░░░░░░░░] │
│ Pending             │     1 │      20.0% │ [████░░░░░░░░░░░░░░░░] │
│ Rejected            │     1 │      20.0% │ [████░░░░░░░░░░░░░░░░] │
└─────────────────────┴───────┴────────────┴────────────────────────┘

── ⭐ PRIORITY DISTRIBUTION ─────────────────────────────────────────────
┌────────────────┬───────┬────────────────┬────────────────────────────────────────────────────────┐
│ Priority Level │ Count │ Share of Total │ Focus Recommendation                                   │
├────────────────┼───────┼────────────────┼────────────────────────────────────────────────────────┤
│ High           │     3 │          60.0% │ Top target! Follow up weekly and prepare stories.      │
│ Medium         │     1 │          20.0% │ Core applications. Maintain standard networking.       │
│ Low            │     1 │          20.0% │ Backup options. Re-evaluate if priority shifts.        │
└────────────────┴───────┴────────────────┴────────────────────────────────────────────────────────┘
```

---

## 🏷️ Priority Sorting Guide

The tracker implements a custom SQL weighted ordering mechanism:
- **High:** Weight 3 (Top dream companies, tight deadlines, or high compensation)
- **Medium:** Weight 2 (Standard applications)
- **Low:** Weight 1 (Backup or exploratory roles)

When querying via SQLite, the application translates priority values dynamically:
```sql
ORDER BY CASE priority
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    WHEN 'Low' THEN 3
    ELSE 4
END ASC
```
This ensures `High` applications are surfaced to the top immediately without relying on flawed alphabetical ordering (`High` vs `Low` vs `Medium`).

---

## 🧪 Testing and Validation

A comprehensive test suite is located in `tests/test_tracker.py`. It tests models, database isolation, priority sorting, search filters, and updates using temporary databases.

### Run All Unit Tests:
```bash
python3 -m unittest discover tests/
```

### Or Run Specifically:
```bash
python3 tests/test_tracker.py
```

### Expected Output:
```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.042s

OK
```

---

## 📦 Git Version Control Commands

To initialize and upload this project to your GitHub account:

```bash
# 1. Initialize Git repository
git init

# 2. Add files to staging
git add .

# 3. Commit changes
git commit -m "feat: complete Job Application Tracker with OOP, SQLite, and Priority sorting"

# 4. Create main branch and link to your GitHub repository
git branch -M main
git remote add origin https://github.com/<your-github-username>/job-application-tracker.git

# 5. Push to GitHub
git push -u origin main
```

---

## 🔮 Future Roadmap

- [ ] Export applications and interview notes to CSV and JSON formats.
- [ ] Calendar integration (.ics file export for scheduled interviews).
- [ ] Automated email reminder scripts for follow-ups.
- [ ] Salary comparison and cost-of-living adjustments.

---

## 📄 License
This project is open-source under the MIT License. Feel free to use and adapt for personal or educational portfolios!
