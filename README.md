# CampusFix — Campus Maintenance Complaint & Tracking System

An end-to-end desktop application designed for colleges and universities to report, track, resolve, and analyze campus facility maintenance complaints. Built with **Python**, **Tkinter**, **SQLite3**, **Pandas**, and **Matplotlib**.

---

## 📸 Overview & Features

- **Branding & UI**: Built with custom high-contrast dark theme styling inspired by **CampusFix — Maintenance Control System**.
- **Dashboard View**:
  - Live campus status indicator (`● LIVE ACROSS 6 CAMPUS BUILDINGS`).
  - Active campus hotspots map (Block A, Library, Computer Lab, Block C).
  - Quick action buttons to open console or log complaints.
- **Complaint Registration**:
  - Structured input form (Student Name, Department, Building, Room No, Category, Priority, Problem Description).
  - Automatic `CMPxxx` Ticket ID generation.
  - Automatic timestamping.
  - Comprehensive field validation.
- **Ticket Management (All Tickets)**:
  - Search by Ticket ID, Student Name, Department, or Issue description.
  - Filter by Status (`Pending`, `In Progress`, `Resolved`) and Campus Building.
  - Interactive Treeview table with color-coded status badges.
  - In-app modals to **Update Status**, **Add Maintenance Details**, and **View Ticket History**.
- **Maintenance & Repair Logging**:
  - Technician assignment, repair date, non-negative repair cost (₹), and repair remarks.
  - Auto-updates ticket status to `In Progress` or `Resolved`.
- **Reports & Data Visualizations**:
  - Live 8-card KPI summary: Total Tickets, Pending, In Progress, Resolved, Total Repair Spend, Average Cost, Most Common Category, Most Reported Building.
  - 5 embedded Matplotlib charts:
    1. **Complaints by Category** (Horizontal Bar Chart)
    2. **Status Distribution** (Pie Chart)
    3. **Complaints by Building** (Vertical Bar Chart)
    4. **Complaints Reported Per Month** (Trend Line Chart)
    5. **Repair Cost by Category** (Vertical Bar Chart)
  - One-click CSV Export to `reports/complaints_report.csv`.

---

## 📂 Project Structure

```text
Campus_Maintenance_System/
├── main.py                     # Main Tkinter desktop application
├── database.py                 # SQLite database schema, CRUD operations, & seeding
├── analysis.py                 # Pandas KPI calculations & Matplotlib chart generation
├── verify_system.py            # Automated test and verification suite
├── requirements.txt            # Python dependencies (pandas, matplotlib)
├── README.md                   # Project overview & running instructions
├── PROJECT_REPORT.md           # Full academic project report (Section 23 compliant)
├── PPT_PRESENTATION.md         # Slide-by-slide presentation structure (Section 24 compliant)
├── VIVA_QUESTIONS.md           # 15+ Viva questions with detailed answers (Section 28 compliant)
├── data/
│   └── campus.db               # SQLite database with 48 realistic pre-seeded records
└── reports/
    └── complaints_report.csv   # Exported CSV reports
```

---

## 🚀 Quickstart & How to Run

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Required Packages
Open your terminal or command prompt inside the project folder:
```bash
pip install -r requirements.txt
```
*(Or install manually: `pip install pandas matplotlib`)*

### 3. Run the Verification Script (Optional)
To verify that database queries, calculations, charts, and exports work:
```bash
python verify_system.py
```

### 4. Launch the Desktop Application
```bash
python main.py
```

---

## 📊 Pre-Seeded Sample Data

The application automatically seeds 48 realistic records upon first launch matching the teacher's reference statistics:
- **Total Complaints**: 48
- **Pending**: 18
- **In Progress**: 12
- **Resolved**: 18
- **Total Maintenance Cost**: ₹16,120
- **Average Repair Cost**: ₹806
- **Most Common Category**: Internet
- **Most Reported Building**: Library
- **Timeframe**: March 2026 to August 2026

---

## 🎓 Academic Documentation Included

- **[`PROJECT_REPORT.md`](PROJECT_REPORT.md)**: Full academic project report with Abstract, Introduction, System Architecture, DFD Diagrams, Database Design, Implementation, Testing Results, and References.
- **[`PPT_PRESENTATION.md`](PPT_PRESENTATION.md)**: Slide deck structure and script ready for project defense and presentation.
- **[`VIVA_QUESTIONS.md`](VIVA_QUESTIONS.md)**: In-depth answers to 15+ viva questions covering Python, Tkinter, SQLite, Pandas, and Matplotlib.
