# CampusFix — Campus Maintenance Complaint & Tracking System

[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite)](https://sqlite.org)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458.svg?logo=pandas)](https://pandas.pydata.org)
[![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-11557C.svg)](https://matplotlib.org)

An enterprise-grade campus facility maintenance and complaint tracking software designed for universities, colleges, and educational institutes.

Featuring **both** a modern **Streamlit Web Application** (for cloud deployment) and an official **Tkinter Desktop GUI** (meeting 100% of academic project guidelines).

---

## 🌟 Key Features & Modules

### 1. 🚀 Real-time Operations Dashboard
- **Live Campus Operations**: Visual status across 6 major campus zones (Block A, Block B, Block C, Computer Lab, Library, Hostel Block).
- **Executive KPI Cards**: Real-time counts of Total Tickets, Pending Work, In-Progress Jobs, and Resolved Issues.
- **Urgent Tickets Feed**: Instant alert banner displaying unresolved high-priority complaints.

### 2. 📝 Complaint Registration
- Structured form: Student Name, Department, Building, Room No, Problem Category, Priority, and Detailed Description.
- Auto-generated sequential Complaint IDs (`CMP001`, `CMP002`...).
- Automatic timestamping and initial status assignment (`Pending`).
- Comprehensive field validation to prevent empty submissions.

### 3. 🎫 Interactive Ticket Console & Search
- Multi-parameter live search: Search by Ticket ID, Student, Room, or Issue.
- Dynamic filtering by Status (`Pending`, `In Progress`, `Resolved`), Building, and Category.
- **Ticket Action Drawer**: Select any complaint to view full audit logs, update status, and log technician repairs.

### 4. 🔧 Maintenance & Repair Ledger
- Record technician/staff name, repair date, repair cost (₹), and parts replaced.
- Automatic or manual status transition to `Resolved`.
- Historical repair ledger tracking total maintenance expenditures and average repair costs.

### 5. 📊 Reports & Visual Analytics
- **8 KPI Metric Cards** matching institutional reporting standards:
  - Total Complaints
  - Pending Count
  - In-Progress Count
  - Resolved Count
  - Total Maintenance Cost (₹)
  - Average Repair Cost (₹)
  - Most Common Category
  - Most Reported Building
- **5 High-Fidelity Data Visualizations**:
  1. Complaints by Category (Horizontal Bar Chart)
  2. Status Distribution (Pie / Donut Chart)
  3. Complaints by Building (Vertical Bar Chart)
  4. Monthly Intake Trend (Line Chart)
  5. Repair Cost by Category (Bar Chart)
- **1-Click Export to CSV**: Download `complaints_report.csv` directly from the web interface.

---

## 📂 Project Directory Structure

```text
Campus_Maintenance_System/
├── app.py                      # Production Streamlit web application (Primary deployment)
├── streamlit_app.py            # Streamlit Cloud entry point
├── main.py                     # Official Tkinter desktop application
├── database.py                 # SQLite schema, CRUD operations, & sample seeding
├── analysis.py                 # Pandas KPI calculations & Matplotlib chart generator
├── verify_system.py            # Automated end-to-end testing suite
├── push_to_github.bat          # Automated 1-click batch script to commit & push to GitHub
├── requirements.txt            # Python dependencies (streamlit, pandas, matplotlib)
├── README.md                   # Complete documentation and setup guide
├── PROJECT_REPORT.md           # 23-section complete academic project report
├── PPT_PRESENTATION.md         # Slide-by-slide presentation structure
├── VIVA_QUESTIONS.md           # 15+ Viva questions with detailed model answers
├── .streamlit/
│   └── config.toml             # Custom theme tokens (Dark Navy palette)
├── data/
│   └── campus.db               # SQLite database with 48 realistic pre-seeded records
└── reports/
    └── complaints_report.csv   # Auto-generated CSV export
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Web App** | Streamlit | Cloud-accessible interactive responsive dashboard |
| **Desktop GUI** | Tkinter & TTK | Local desktop GUI fulfilling academic requirements |
| **Database** | SQLite 3 | Relational database (`complaints` and `maintenance` tables) |
| **Data Crunching** | Pandas | Grouping, aggregation, summary metrics, and CSV export |
| **Charts** | Matplotlib | High-contrast dark-themed analytical charts |

---

## 🚀 How to Run Locally

### 1. Clone or Open the Project
```bash
git clone https://github.com/yogavijaynandandasari/CampusFix.git
cd CampusFix
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Automated Verification Suite
```bash
python verify_system.py
```

### 4. Launch the Modern Browser Dashboard (Recommended)
Double-click `start_browser_dashboard.bat` or run:
```bash
python serve_web.py
```
*Your default web browser (Edge/Chrome/Firefox) will automatically open `http://localhost:8000` with the live interactive campus dashboard connected to SQLite.*

### 5. Launch the Streamlit Web Application
Double-click `start_streamlit_dashboard.bat` or run:
```bash
streamlit run app.py
```
*Your browser will open `http://localhost:8501`.*

### 6. Launch the Tkinter Desktop Application
Double-click `start_tkinter_desktop.bat` or run:
```bash
python main.py
```
*Opens the Tkinter desktop GUI fulfilling the academic project requirement.*

---

## ☁️ How to Deploy on Streamlit Community Cloud (Free)

Deploying takes under 2 minutes:

1. **Push your code to GitHub**:
   - Double-click `push_to_github.bat` or run:
     ```bash
     git add .
     git commit -m "Deploy CampusFix on Streamlit"
     git push -u origin main
     ```
2. **Go to Streamlit Community Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. **Create New App**:
   - Click **"Create app"** -> **"I already have an app"**.
   - Select your repository: `yogavijaynandandasari/CampusFix`
   - Branch: `main`
   - Main file path: `app.py`
4. **Deploy**:
   - Click **"Deploy!"**
   - Your application will go live with a public URL like `https://campusfix.streamlit.app`!

---

## 📋 Database Schema

```sql
-- Complaints Table
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id TEXT UNIQUE NOT NULL,
    student_name TEXT NOT NULL,
    department TEXT NOT NULL,
    building TEXT NOT NULL,
    room_no TEXT NOT NULL,
    category TEXT NOT NULL,
    problem TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL
);

-- Maintenance Table
CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id TEXT NOT NULL,
    staff_name TEXT NOT NULL,
    repair_date TEXT NOT NULL,
    cost REAL NOT NULL,
    remarks TEXT NOT NULL,
    FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
);
```

---

## 🎓 Academic Documents Included

- 📄 [`PROJECT_REPORT.md`](file:///C:/Users/vijay%20nandan/.gemini/antigravity/scratch/Campus_Maintenance_System/PROJECT_REPORT.md) — 23-section detailed major project report with certificate, acknowledgements, system architecture, and screenshots.
- 📊 [`PPT_PRESENTATION.md`](file:///C:/Users/vijay%20nandan/.gemini/antigravity/scratch/Campus_Maintenance_System/PPT_PRESENTATION.md) — Complete 13-slide presentation outline for defense and final evaluation.
- 💡 [`VIVA_QUESTIONS.md`](file:///C:/Users/vijay%20nandan/.gemini/antigravity/scratch/Campus_Maintenance_System/VIVA_QUESTIONS.md) — Comprehensive viva preparation with 15+ detailed technical questions and answers.

---

## 👤 Author & Credits
- **Developed by:** Student Major Project Team
- **Repository:** [https://github.com/yogavijaynandandasari/CampusFix](https://github.com/yogavijaynandandasari/CampusFix)
- **Guided by:** Faculty of Computer Applications & Technology
