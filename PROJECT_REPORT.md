# PROJECT REPORT
# Campus Maintenance Complaint & Tracking System ("CampusFix")

**Academic Year:** 2026–2027  
**Degree:** Major Project Submission  
**Technology Stack:** Python 3, Tkinter GUI, SQLite3 Database, Pandas Data Analysis, Matplotlib Visualizations  

---

## 1. Title Page

**Project Title:** Campus Maintenance Complaint & Tracking System ("CampusFix")  
**Domain:** Desktop Application & Facility Management System  
**Developed By:** Student Project Team  
**Supervisor / Mentor:** Prof. Ankita Asthana (<ankita.asthana@samatrix.io>)  
**Institution:** Faculty of Computer Applications & Technology  

---

## 2. Certificate / Declaration

### Certificate of Original Work
This is to certify that the project entitled **"Campus Maintenance Complaint & Tracking System"** is a bonafide work carried out by the student team in partial fulfillment of the requirements for the award of the Degree. The work embodied in this project report has not been submitted elsewhere for any other degree or diploma.

**Project Guide / Mentor:**  
Prof. Ankita Asthana  
Faculty Coordinator  

### Student Declaration
We hereby declare that this project report titled **"Campus Maintenance Complaint & Tracking System"** is an authentic record of our own research and development work carried out under the supervision of our guide. All information, data schemas, code implementations, and analytical charts presented in this report are original, except where explicitly cited.

---

## 3. Acknowledgement
We express our deepest gratitude to our project guide, **Prof. Ankita Asthana**, for her continuous guidance, constructive feedback, and encouragement throughout the design and development phases of this project. Her clear specifications and milestone roadmaps enabled us to transform a real-world campus problem into an efficient software solution.

We also thank the Department Faculty, Lab Assistants, and our peers whose valuable suggestions helped refine the user interface and testing procedures.

---

## 4. Abstract
Educational campuses require efficient physical infrastructure management, including classrooms, laboratories, computer centers, washrooms, and hostels. Traditional manual registers and paper complaint logs are prone to lost records, lack of accountability, delay in repairs, and absence of statistical visibility.

The **Campus Maintenance Complaint & Tracking System ("CampusFix")** is an end-to-end desktop software solution built using **Python, Tkinter, SQLite, Pandas, and Matplotlib**. The system facilitates instant complaint registration with automated ticket ID generation (`CMP001`, `CMP002`...), dynamic status tracking (`Pending`, `In Progress`, `Resolved`), maintenance expense logging, and live visual analytics. By leveraging Pandas for real-time aggregation and Matplotlib for graphical charts, administration teams can identify recurring failure points, track repair budgets, and optimize facility upkeep across all campus buildings.

---

## 5. Introduction
Colleges operate extensive facilities spanning multiple departments and residential blocks. Facility breakdowns—ranging from electrical failures, plumbing issues, Wi-Fi downtime, to furniture breakages—directly impede academic workflows.

A software-driven maintenance management system centralizes maintenance requests into a unified digital dashboard. It bridges students and facility staff, ensuring tickets are timestamped, categorized, prioritized, and monitored until completion.

---

## 6. Problem Statement
Existing campus maintenance processes face critical operational drawbacks:
1. **Manual Paper Logs:** Physical registers kept at department desks or hostel gates are often misplaced or unread by maintenance staff.
2. **Lack of Tracking & Status Visibility:** Students cannot track whether an issue has been reviewed, assigned, or completed.
3. **Budget & Cost Opacity:** Campus administrators lack automated tracking of repair costs, spare parts expenditure, and labor expenses.
4. **No Analytical Insights:** Repetitive equipment failures cannot be detected early due to the absence of centralized data crunching.

---

## 7. Objectives
The primary objectives of the project are:
- To provide a user-friendly desktop GUI for quick complaint registration with auto-generated ticket IDs.
- To maintain an ACID-compliant local database storing complaint and maintenance details.
- To implement filtering and search mechanisms for administrative tracking.
- To calculate critical operational KPIs (Pending vs. Resolved tickets, total expenditure, average repair cost).
- To generate 5 core Matplotlib charts for visual reporting and trends analysis.
- To provide CSV export functionality for offline auditing and reporting.

---

## 8. Existing System vs. Proposed System

| Feature | Existing Manual System | Proposed CampusFix System |
| :--- | :--- | :--- |
| **Medium** | Paper register / Verbal complaints | Desktop application with GUI |
| **Ticket ID** | None / Manual serial number | Unique auto-generated ID (`CMPxxx`) |
| **Status Updates** | Unknown until physical inquiry | Real-time (`Pending`, `In Progress`, `Resolved`) |
| **Maintenance Details** | Receipts filed manually in folders | Linked directly to complaint in SQLite DB |
| **Repair Cost Tracking**| Manual calculations in spreadsheets | Live automatic cost computation via Pandas |
| **Analytics & Trends** | Absent | 5 interactive Matplotlib charts |
| **Data Export** | Manual typing | One-click CSV export |

---

## 9. Technology Used

- **Python 3.10+**: Core programming language providing high readability and rich standard library.
- **Tkinter & `ttk`**: Standard Python GUI toolkit customized with a modern dark theme (`#0B192C` / `#15263F`).
- **SQLite3**: Lightweight, zero-configuration relational database engine embedded directly into the application.
- **Pandas**: High-performance data manipulation library for KPI aggregation, grouping, and CSV generation.
- **Matplotlib**: Visualization library utilized with `FigureCanvasTkAgg` for rendering interactive charts within Tkinter.

---

## 10. System Design & Architecture

### System Architecture Diagram
```text
┌─────────────────────────────────────────────────────────────┐
│                    Tkinter Desktop GUI                      │
│   (Dashboard  •  Register  •  All Tickets  •  Reports)       │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
    ┌──────────────────────┐        ┌──────────────────────┐
    │   CRUD Operations    │        │  Pandas & Matplotlib │
    │   (database.py)      │        │  (analysis.py)       │
    └──────────┬───────────┘        └──────────┬───────────┘
               │                               │
               ▼                               ▼
    ┌──────────────────────┐        ┌──────────────────────┐
    │   SQLite Database    │        │ Exported CSV Reports │
    │   (data/campus.db)   │        │ (reports/*.csv)      │
    └──────────────────────┘        └──────────────────────┘
```

### Data Flow Diagram (DFD Level 0 - Context Level)
```text
   [Student / User] ──── Register Complaint ───► [ CampusFix ] ──── Visual Reports ────► [ Administrator ]
                    ◄─── Ticket Confirmation ─── [   System  ] ◄─── Status & Repair ─── [ Technician ]
```

### Data Flow Diagram (DFD Level 1)
1. User enters complaint details into Registration Form.
2. System validates non-empty inputs and executes `add_complaint()`.
3. Database assigns next sequence ID (`CMPxxx`) and persists record into `complaints` table.
4. Administrative staff filters tickets and clicks "Add Maintenance Details".
5. Maintenance technician details and repair costs are recorded into `maintenance` table.
6. Status updates to `Resolved`.
7. Analytics engine queries database with Pandas and refreshes Matplotlib visual charts.

---

## 11. Database Design

### Entity-Relationship (ER) Schema
The relational database `campus.db` contains two normalized tables:

#### Table 1: `complaints`
| Field | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal record identifier |
| `complaint_id` | TEXT | UNIQUE, NOT NULL | External ticket ID (e.g. `CMP001`) |
| `student_name` | TEXT | NOT NULL | Name of student reporting |
| `department` | TEXT | NOT NULL | Academic branch (BCA, B.Tech, etc.) |
| `building` | TEXT | NOT NULL | Campus facility / building name |
| `room_no` | TEXT | NOT NULL | Specific classroom / lab / room number |
| `category` | TEXT | NOT NULL | Problem category (Electrical, IT, etc.) |
| `problem` | TEXT | NOT NULL | Detailed problem description |
| `priority` | TEXT | NOT NULL | Low / Medium / High |
| `status` | TEXT | NOT NULL | Pending / In Progress / Resolved |
| `date` | TEXT | NOT NULL | Date reported (YYYY-MM-DD) |

#### Table 2: `maintenance`
| Field | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal maintenance ID |
| `complaint_id` | TEXT | NOT NULL, FOREIGN KEY | References `complaints(complaint_id)` |
| `staff_name` | TEXT | NOT NULL | Maintenance staff / technician name |
| `repair_date` | TEXT | NOT NULL | Date of repair work |
| `cost` | REAL | NOT NULL, >= 0 | Repair expense in INR (₹) |
| `remarks` | TEXT | NOT NULL | Description of repair or replaced parts |

---

## 12. Implementation Details

### Core Modules:
1. **`main.py`**:
   - Manages the Tkinter `Tk` root window and modern navigation bar.
   - Houses the 4 primary views: Dashboard, Register Form, All Tickets Treeview, and Live Reports.
   - Hosts modal dialogs for updating status and entering maintenance logs.
2. **`database.py`**:
   - Manages SQLite connection pooling and transactions.
   - Provides methods: `init_db()`, `add_complaint()`, `get_all_complaints()`, `update_complaint_status()`, `add_maintenance_record()`.
   - Contains automatic database seeder with 48 realistic historical records.
3. **`analysis.py`**:
   - Interfaces between SQLite and Pandas DataFrame.
   - Computes KPI dictionaries: total tickets, status counts, total maintenance expenditure, average cost, most common category, and most reported building.
   - Renders 5 custom dark-themed Matplotlib figures.
   - Handles CSV report exports into `reports/complaints_report.csv`.

---

## 13. Testing & Quality Assurance

### Test Cases Execution Matrix

| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC01** | Submit complete complaint | Valid name, dept, room, issue | Ticket saved, `CMPxxx` generated | `CMP049` generated and saved | **PASS** |
| **TC02** | Submit blank complaint form | Empty Student Name or Problem | Validation error dialog | Dialog displayed; focus retained | **PASS** |
| **TC03** | Search valid Ticket ID | `CMP001` | Displays matching complaint row | Record rendered in Treeview | **PASS** |
| **TC04** | Search non-existent ID | `CMP999` | Shows empty result / message | 0 records shown | **PASS** |
| **TC05** | Update status | Change `Pending` to `In Progress` | Status in database updated | Database & Treeview updated | **PASS** |
| **TC06** | Add maintenance record | Staff: Amit, Cost: ₹500, remarks | Record inserted into maintenance table | Stored and linked to complaint | **PASS** |
| **TC07** | Negative repair cost | Cost: -200 | Error dialog "Cost cannot be negative" | Error shown; input rejected | **PASS** |
| **TC08** | Compute analytics | 48 pre-seeded records | Total: 48, Pending: 18, Resolved: 18 | Exact metrics verified | **PASS** |
| **TC09** | CSV Export | Click "Export tickets to CSV" | CSV written to `reports/` folder | File verified at destination | **PASS** |

---

## 14. Results & Findings
- **Resolution Distribution:** From 48 campus complaints analyzed, 18 (37.5%) are Resolved, 12 (25.0%) are In Progress, and 18 (37.5%) are Pending.
- **Top Breakdown Categories:** The most reported category is **Internet** (Wi-Fi connectivity and switch port issues in digital libraries and hostel wings).
- **Highest Maintenance Load:** The **Library** building generated the highest complaints count (12 tickets).
- **Financial Expenditure:** Total repair cost amounted to **₹16,120** with an average repair cost of **₹806** per completed maintenance ticket.

---

## 15. Limitations
- Single-user desktop deployment (no concurrent web access across different student smartphones).
- SQLite database is stored locally rather than in a cloud-hosted relational server.
- Notification dispatch (email/SMS) is not supported in the basic desktop version.

---

## 16. Future Scope
As outlined in Section 29 of the project guide, potential future enhancements include:
1. Converting the desktop application into a web application using Flask or FastAPI.
2. Implementing role-based user authentication (Student, Technician, Admin roles).
3. Allowing students to upload photos of broken equipment.
4. Automated SMS/Email alerts to students when tickets are resolved.
5. QR-code complaint registration stickers on classroom doors and equipment.

---

## 17. Conclusion
The **Campus Maintenance Complaint & Tracking System ("CampusFix")** successfully fulfills all academic and functional requirements. It replaces cumbersome paper registers with an intuitive, resilient, and visually engaging facility management platform. With built-in Pandas analytics and Matplotlib visualizations, it empowers institutional administrators to maintain campus assets efficiently.

---

## 18. References
1. Python Documentation: *Tkinter GUI Package* - https://docs.python.org/3/library/tkinter.html
2. SQLite Documentation: *SQLite SQL Syntax and Database Engine* - https://www.sqlite.org/docs.html
3. McKinney, Wes. *Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython*. O'Reilly Media.
4. Hunter, J. D. *Matplotlib: A 2D Graphics Environment*. Computing in Science & Engineering, 9(3), 90-95.
5. Campus Maintenance Project Guide (`Campus_Maintenance_Project.pdf`), Faculty of Computer Applications.
