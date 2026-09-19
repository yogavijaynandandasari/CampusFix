# PPT PRESENTATION OUTLINE
# Campus Maintenance Complaint & Tracking System ("CampusFix")

This document provides the complete slide-by-slide script, bullet points, talking points, and presentation structure required by **Section 24 of the Project Guide**.

---

## Slide 1: Project Title
- **Headline:** Campus Maintenance Complaint & Tracking System
- **Subtitle:** Streamlining Campus Infrastructure Upkeep with Python, Tkinter, SQLite, Pandas & Matplotlib
- **Project Brand:** CampusFix — Maintenance Control System
- **Presented By:** [Your Name / Team Members]
- **Under the Guidance of:** Prof. Ankita Asthana
- **Date:** September 2026

---

## Slide 2: Problem Statement
- **Manual Registers:** Maintenance complaints are logged on paper logs that get lost, damaged, or unread.
- **Lack of Tracking:** Students and staff have no visibility into whether complaints are pending, in progress, or fixed.
- **No Financial Visibility:** Repair costs, spare parts expenses, and labor charges are not tracked systematically.
- **No Data Insights:** Recurring equipment failures (e.g. repeated fan breakdowns) go unnoticed without analytics.

---

## Slide 3: Objectives
- Provide a clean desktop application for rapid complaint registration with auto-assigned Ticket IDs (`CMP001`...).
- Implement centralized relational storage with SQLite for complaints and maintenance logs.
- Deliver real-time ticket tracking, search, and status workflow management (`Pending` → `In Progress` → `Resolved`).
- Automatically calculate crucial facility metrics using Pandas.
- Generate 5 core Matplotlib charts directly inside the GUI to guide facility budgeting.
- Enable one-click CSV export for administrative records and audits.

---

## Slide 4: Proposed Solution: CampusFix
- **Unified Work-Order Hub:** Converts scattered complaints into structured digital work tickets.
- **Interactive Console:** Search, filter by status or building, and update ticket lifecycle in seconds.
- **Maintenance Logger:** Links repair workers, dates, part replacement remarks, and costs to complaints.
- **Live Analytical Dashboard:** Embedded charts and KPI cards crunched live using Pandas.

---

## Slide 5: Technology Stack
- **Programming Language:** Python 3 (Object-Oriented, Modular)
- **GUI Toolkit:** Tkinter & `ttk` (Custom modern dark theme: `#0B192C` / `#15263F`)
- **Database Engine:** SQLite3 (Serverless, zero-config relational storage)
- **Data Wrangling:** Pandas (Aggregations, group-bys, statistics)
- **Data Visualization:** Matplotlib (`FigureCanvasTkAgg` embedded into Tkinter)

---

## Slide 6: System Workflow
```text
[Student/Staff] ──► Register Complaint Form ──► Auto-generate CMP001 ──► SQLite (complaints)
                                                                               │
[Technician]    ──► Inspect & Add Repair Record ◄── Status: In Progress ◄──────┘
        │
        └──► Log Cost & Remarks ──► Status: Resolved ──► SQLite (maintenance)
                                                               │
                                                               ▼
[Admin/Faculty] ◄── Live Dashboard & Charts ◄── Pandas Aggregation & Matplotlib
```

---

## Slide 7: Database Design
- **Complaints Table:**
  - `id`: Primary Key
  - `complaint_id`: Unique ticket identifier (e.g., `CMP001`)
  - `student_name`, `department`, `building`, `room_no`, `category`, `problem`, `priority`, `status`, `date`
- **Maintenance Table:**
  - `id`: Primary Key
  - `complaint_id`: Foreign Key referencing `complaints`
  - `staff_name`, `repair_date`, `cost`, `remarks`

---

## Slide 8: Application Screens
- **Dashboard Screen:** Live building coverage badge, campus schematic map cards, quick call-to-actions.
- **Register Complaint Form:** Warm card layout, required field validation, automatic date & sequence ID.
- **All Tickets Console:** Search bar, status filters, building filters, color-coded rows in `ttk.Treeview`.
- **Modals:** One-click modals to update status, record repair worker name, repair cost, and remarks.

---

## Slide 9: Data Analysis & Visualizations (Pandas & Matplotlib)
- **KPI Metrics Calculated:**
  - Total Complaints: **48**
  - Status: **18 Pending**, **12 In Progress**, **18 Resolved**
  - Total Maintenance Cost: **₹16,120**
  - Average Repair Cost: **₹806**
  - Most Common Category: **Internet**
  - Most Reported Building: **Library**
- **5 Embedded Charts:**
  1. *Horizontal Bar Chart:* Complaints by Category
  2. *Pie Chart:* Status Distribution
  3. *Vertical Bar Chart:* Complaints by Campus Building
  4. *Line Chart:* Monthly Complaints Trend (March – August 2026)
  5. *Vertical Bar Chart:* Repair Cost by Category

---

## Slide 10: Testing & Validation
- **Unit & Integration Tests Conducted:**
  - Empty form submission: Blocked with user-friendly validation error dialog.
  - Negative repair cost: Blocked with error alert.
  - Ticket ID lookup: Accurate filtering in Treeview.
  - Status transitions: Validated in database and immediately reflected across GUI.
  - CSV Export: Merged dataset exported safely to `reports/complaints_report.csv`.

---

## Slide 11: Results & Key Findings
- **37.5%** of complaints have been successfully resolved; **25%** are currently in progress.
- **Internet and Wi-Fi** connectivity represent the most frequent complaints across campus.
- **Library and Hostel Blocks** experience the highest maintenance requests.
- Air Conditioning / Cooling repairs account for the highest total expenditure (over ₹7,000).

---

## Slide 12: Future Scope
- Transition from desktop Tkinter to a Web Application (Flask / FastAPI / React).
- User authentication with Role-Based Access Control (Student, Maintenance Head, Admin).
- Photo attachments for broken equipment.
- SMS and WhatsApp ticket status notification webhooks.
- QR-code based room reporting stickers.

---

## Slide 13: Conclusion
- **CampusFix** delivers a complete, robust, and modern maintenance tracking workflow.
- Bridges the gap between students, maintenance workers, and administrative decision-makers.
- Meets and exceeds all course requirements, demonstrating proficiency in Python, database engineering, GUI development, data analysis, and visualization.

---

## Slide 14: Questions & Answers (Thank You)
- *Open floor for Viva and Evaluator Questions.*
- Thank you!
