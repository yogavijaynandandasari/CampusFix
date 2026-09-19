# VIVA VOCE PREPARATION GUIDE
# Campus Maintenance Complaint & Tracking System ("CampusFix")

This guide provides comprehensive answers and technical explanations for the viva questions listed in **Section 28 of the Project Guide**.

---

### Q1: Why did you choose this project?
**Answer:**  
We chose this project because facility management is a real-world operational challenge faced by every educational institution. Manual paper registers often result in misplaced complaints, delays in technician dispatch, lack of status tracking for students, and zero visibility into recurring repair costs. Developing **CampusFix** allowed us to build a practical desktop solution incorporating complete database management (SQLite), responsive desktop UI design (Tkinter), automated data analysis (Pandas), and visualization (Matplotlib).

---

### Q2: Why did you use SQLite instead of MySQL or PostgreSQL?
**Answer:**  
1. **Serverless & Zero-Configuration:** SQLite does not require a standalone server process or administrative configuration like MySQL or PostgreSQL.
2. **Portability:** The entire database is stored in a single standalone file (`data/campus.db`), making it easy to deploy, backup, and run on any operating system without installing database services.
3. **Built-in Support:** Python comes with native SQLite support through the standard `sqlite3` module.
4. **ACID Compliant:** It offers full transactional support suitable for desktop and local institutional applications.

---

### Q3: What is Tkinter?
**Answer:**  
Tkinter is Python's standard, built-in Graphical User Interface (GUI) package. It provides Python wrappers for the Tcl/Tk GUI toolkit. It features widgets such as Frames, Labels, Buttons, Text entries, and the modern `ttk` (Themed Tkinter) module, which includes advanced widgets like `Treeview`, Comboboxes, and custom styling themes.

---

### Q4: What is CRUD? How is it implemented in this project?
**Answer:**  
CRUD stands for **Create, Read, Update, and Delete**—the four basic persistent storage functions:
- **Create:** Registering a new complaint (`INSERT INTO complaints...`) and logging maintenance records (`INSERT INTO maintenance...`).
- **Read:** Viewing all tickets in the Treeview table (`SELECT * FROM complaints...`) and searching by Ticket ID.
- **Update:** Changing ticket status (`UPDATE complaints SET status = ...`) and modifying repair records.
- **Delete:** Archiving or removing obsolete complaint records.

---

### Q5: What is an SQL SELECT query? Give an example from the project.
**Answer:**  
An SQL `SELECT` statement retrieves specific data from one or more database tables matching specified criteria.  
**Example from `database.py`:**
```sql
SELECT * FROM complaints 
WHERE (complaint_id LIKE ? OR student_name LIKE ? OR department LIKE ?)
  AND status = ?
ORDER BY id DESC;
```
This query fetches all matching complaints based on search keywords and status filters, ordered with newest tickets first.

---

### Q6: How do you insert data into SQLite from Python?
**Answer:**  
We connect to SQLite using `sqlite3.connect()`, create a `cursor` object, and execute parameterized SQL `INSERT` statements with placeholders (`?`) to prevent SQL injection:
```python
conn = sqlite3.connect("data/campus.db")
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date))
conn.commit()  # Commits the transaction
conn.close()
```

---

### Q7: How is the Complaint ID generated?
**Answer:**  
The Complaint ID is generated systematically using the `generate_complaint_id()` function in `database.py`. It inspects the highest existing `complaint_id` in the `complaints` table (e.g., `CMP048`), extracts the numeric portion using string parsing, increments it by 1, and formats it as a 3-digit zero-padded string (`CMP049`):
```python
cursor.execute("SELECT complaint_id FROM complaints ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()
if row and row["complaint_id"].startswith("CMP"):
    num = int(row["complaint_id"].replace("CMP", ""))
    return f"CMP{num + 1:03d}"
return "CMP001"
```

---

### Q8: Why is Pandas used in this project?
**Answer:**  
Pandas is a fast, flexible data manipulation library in Python. Instead of writing complex, repetitive SQL queries for every metric, Pandas reads the database directly using `pd.read_sql_query()` into DataFrames. It simplifies:
- Grouping data (`df.groupby('category')['cost'].sum()`)
- Counting occurrences (`df['status'].value_counts()`)
- Computing statistical metrics (mean, sum, mode)
- Merging tables via left joins (`pd.merge()`)
- Exporting data to CSV with `to_csv()`

---

### Q9: Why is Matplotlib used? How is it integrated into Tkinter?
**Answer:**  
Matplotlib is Python's premier 2D plotting library. We use it to visualize maintenance patterns (bar charts, pie charts, line charts).  
To embed Matplotlib directly inside a Tkinter window rather than opening external blocking windows, we use the backend adapter:
```python
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = Figure(figsize=(5.5, 3.2), dpi=100)
# plot logic...
canvas = FigureCanvasTkAgg(fig, master=parent_frame)
canvas.draw()
canvas.get_tk_widget().pack()
```

---

### Q10: How did you calculate total and average maintenance cost?
**Answer:**  
In `analysis.py`, we query the `maintenance` table into a Pandas DataFrame `df_maintenance`:
- **Total Cost:** Computed using `df_maintenance["cost"].sum()`
- **Average Cost:** Computed using `df_maintenance["cost"].mean()`
This gives the exact total repair expenditure and the average expenditure per serviced complaint.

---

### Q11: What is the difference between Pending, In Progress, and Resolved?
**Answer:**  
- **Pending:** The complaint has been registered by a student or staff member but has not yet been assigned to or inspected by a technician.
- **In Progress:** A technician or maintenance worker has been assigned, inspection has taken place, or replacement parts have been ordered.
- **Resolved:** The repair work has been completed, verified, maintenance costs recorded, and the ticket closed.

---

### Q12: What happens when an invalid or non-existent Complaint ID is entered?
**Answer:**  
The application implements defensive validation:
- In the search bar: The SQL query returns an empty result set, and the table displays `Showing 0 tickets` without crashing.
- In status update or maintenance forms: The method checks `if not complaint:`, alerting the user with a `messagebox.showerror("Error", "Ticket not found")` and terminating the operation gracefully without generating unhandled Python exceptions.

---

### Q13: Where is the project data stored?
**Answer:**  
The data is stored locally inside the project directory at:
`Campus_Maintenance_System/data/campus.db`  
Exported CSV files are saved to:
`Campus_Maintenance_System/reports/complaints_report.csv`

---

### Q14: Does this project use Machine Learning? Why not?
**Answer:**  
No, this project does not use Machine Learning. As highlighted in Section 2 of the Project Guide:
1. Facility maintenance logging and status tracking is a deterministic workflow requiring reliable relational data management (CRUD) rather than probabilistic predictions.
2. The core objective is software engineering: building an end-to-end operational system integrating a database, GUI, data aggregation, and visualizations.
3. Machine Learning could, however, be added in future work for predictive maintenance (e.g., forecasting when a transformer or AC unit is likely to fail).

---

### Q15: What improvements can be made in the future?
**Answer:**  
1. **Web / Mobile Interface:** Porting the application to a web framework (such as Flask or Django) with React to allow access from student mobile phones.
2. **Role-Based Access Control:** Separate login portals for Students, Maintenance Workers, and Campus Administrators.
3. **Multimedia Attachments:** Permitting students to upload photos or audio recordings of damaged infrastructure.
4. **Automated Alerts:** Integrating Twilio or SMTP to send SMS and email notifications on status transitions.
5. **QR Code Integration:** Scanning QR stickers in classrooms to automatically populate Building and Room numbers.
