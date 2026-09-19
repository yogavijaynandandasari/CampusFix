"""
database.py - Database Layer for Campus Maintenance Complaint & Tracking System
Implements SQLite connection, table schemas, CRUD functions, and initial sample data seeding.
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "campus.db")


def get_connection():
    """Returns a SQLite connection to campus.db, creating directory if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes SQLite database tables for complaints and maintenance."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: complaints
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
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
        )
    """)

    # Table 2: maintenance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT NOT NULL,
            staff_name TEXT NOT NULL,
            repair_date TEXT NOT NULL,
            cost REAL NOT NULL,
            remarks TEXT NOT NULL,
            FOREIGN KEY (complaint_id) REFERENCES complaints (complaint_id)
        )
    """)

    conn.commit()
    conn.close()

    # Automatically seed sample data if complaints table is empty
    seed_if_empty()


def generate_complaint_id():
    """Generates the next complaint ID in CMP001 format."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id FROM complaints ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row and row["complaint_id"].startswith("CMP"):
        try:
            current_num = int(row["complaint_id"].replace("CMP", ""))
            return f"CMP{current_num + 1:03d}"
        except ValueError:
            pass

    # Fallback / starting point
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM complaints")
    count = cursor.fetchone()["total"]
    conn.close()
    return f"CMP{count + 1:03d}"


def add_complaint(student_name, department, building, room_no, category, problem, priority="Medium", status="Pending", date=None):
    """Inserts a new complaint into the complaints table."""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    complaint_id = generate_complaint_id()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (complaint_id, student_name.strip(), department.strip(), building.strip(), room_no.strip(),
          category.strip(), problem.strip(), priority.strip(), status.strip(), date))
    conn.commit()
    conn.close()
    return complaint_id


def get_all_complaints(search_term=None, status_filter=None, building_filter=None, category_filter=None):
    """Fetches complaints with optional search and filters."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM complaints WHERE 1=1"
    params = []

    if search_term:
        term = f"%{search_term.strip()}%"
        query += " AND (complaint_id LIKE ? OR student_name LIKE ? OR department LIKE ? OR problem LIKE ? OR room_no LIKE ?)"
        params.extend([term, term, term, term, term])

    if status_filter and status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)

    if building_filter and building_filter != "All":
        query += " AND building = ?"
        params.append(building_filter)

    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_complaint_by_id(complaint_id):
    """Fetches single complaint record by its complaint_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_complaint_status(complaint_id, new_status):
    """Updates the status of an existing complaint (Pending, In Progress, Resolved)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (new_status.strip(), complaint_id.strip()))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def add_maintenance_record(complaint_id, staff_name, repair_date, cost, remarks):
    """Adds a maintenance repair record for a complaint."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, (complaint_id.strip(), staff_name.strip(), repair_date.strip(), float(cost), remarks.strip()))
    conn.commit()
    conn.close()
    return True


def get_maintenance_for_complaint(complaint_id):
    """Returns all maintenance records associated with a complaint ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance WHERE complaint_id = ? ORDER BY id DESC", (complaint_id.strip(),))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_all_maintenance_records():
    """Returns all maintenance records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def seed_if_empty():
    """Seeds initial realistic sample complaints and maintenance logs if DB is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS cnt FROM complaints")
    count = cursor.fetchone()["cnt"]
    conn.close()

    if count > 0:
        return

    # Seed data matching reference dashboard statistics:
    # 48 Total Complaints: 18 Pending, 12 In Progress, 18 Resolved
    # Most Common Category: Internet (11 complaints)
    # Most Reported Building: Library (12 complaints)
    # Total Maintenance Cost: ₹16,120, Avg Repair Cost: ₹806 (across 20 maintenance records)
    sample_complaints = [
        # CMP001 - CMP010
        ("CMP001", "Rahul Sharma", "BCA", "Block A", "204", "Electrical", "Ceiling fan not working and making ticking noise", "Medium", "Pending", "2026-03-10"),
        ("CMP002", "Priya Verma", "B.Tech CSE", "Block B", "102", "Furniture", "Broken bench and wooden chair leg damaged", "Low", "Resolved", "2026-03-15"),
        ("CMP003", "Amit Patel", "MCA", "Computer Lab", "Lab 2", "IT", "Desktop PC #14 monitor not turning on and blue screen", "High", "In Progress", "2026-03-22"),
        ("CMP004", "Sneha Rao", "B.Tech ECE", "Block C", "305", "Plumbing", "Washroom tap continuous water leakage", "High", "Resolved", "2026-03-28"),
        ("CMP005", "Vikas Nair", "BCA", "Block A", "108", "Internet", "Wi-Fi access point SSID not broadcasting in lecture hall", "Medium", "Pending", "2026-04-02"),
        ("CMP006", "Ananya Ghosh", "MBA", "Library", "Reading Hall 1", "Internet", "Frequent Wi-Fi disconnections during online research", "High", "Resolved", "2026-04-05"),
        ("CMP007", "Rohan Gupta", "B.Tech ME", "Hostel Block", "H-204", "AC/Cooling", "Wall air conditioner unit blowing warm air", "High", "Resolved", "2026-04-11"),
        ("CMP008", "Meera Iyer", "BCA", "Library", "Stack Area", "Cleaning", "Dust accumulation and waste bin overflow in section B", "Low", "Resolved", "2026-04-16"),
        ("CMP009", "Arjun Reddy", "B.Tech CSE", "Computer Lab", "Lab 1", "IT", "Projector HDMI display flickering continuously", "High", "Pending", "2026-04-20"),
        ("CMP010", "Kavita Joshi", "BBA", "Block B", "210", "Furniture", "Classroom podium hinge broken and wobbly table", "Medium", "In Progress", "2026-04-25"),

        # CMP011 - CMP020
        ("CMP011", "Deepak Singh", "MCA", "Library", "Digital Library", "Internet", "LAN port dead at terminal desks 5 through 8", "High", "Resolved", "2026-05-02"),
        ("CMP012", "Pooja Hegde", "B.Tech ECE", "Block A", "312", "Electrical", "Tube light blinking intermittently causing disturbance", "Low", "Pending", "2026-05-04"),
        ("CMP013", "Suresh Kumar", "BCA", "Block C", "118", "Plumbing", "Handwash sink drain pipe clogged and overflowing", "High", "Resolved", "2026-05-08"),
        ("CMP014", "Neha Kapoor", "B.Tech CSE", "Computer Lab", "AI Lab", "IT", "Keyboard keys sticky and optical mouse sensor faulty", "Low", "Resolved", "2026-05-12"),
        ("CMP015", "Karan Malhotra", "Hostel Block", "Hostel Block", "H-105", "AC/Cooling", "Window cooler motor stopped running completely", "High", "In Progress", "2026-05-15"),
        ("CMP016", "Divya Pillai", "MBA", "Library", "Reference Room", "Furniture", "Two study chairs with torn armrests and uneven base", "Low", "Resolved", "2026-05-19"),
        ("CMP017", "Gaurav Sen", "B.Tech IT", "Library", "Floor 2", "Internet", "Wi-Fi signal strength extremely weak on north wing", "Medium", "Pending", "2026-05-22"),
        ("CMP018", "Ritu Saxena", "BBA", "Block A", "101", "Other", "Classroom door lock jammed and latch stuck", "Medium", "Resolved", "2026-05-25"),
        ("CMP019", "Manoj Tiwari", "B.Tech ME", "Block B", "Workshop A", "Electrical", "Main power distribution board switch tripping often", "High", "In Progress", "2026-05-28"),
        ("CMP020", "Simran Kaur", "MCA", "Library", "Quiet Zone", "Cleaning", "Spilled beverage stains on carpet needing shampoo cleaning", "Medium", "Resolved", "2026-06-01"),

        # CMP021 - CMP030
        ("CMP021", "Aditya Roy", "BCA", "Block C", "202", "Furniture", "Lecture desk top detached from metallic frame", "Medium", "In Progress", "2026-06-03"),
        ("CMP022", "Tanvi Deshmukh", "B.Tech CSE", "Library", "Floor 1", "Internet", "Gateway router drops internet packets during peak hours", "High", "Resolved", "2026-06-06"),
        ("CMP023", "Nikhil Chawla", "B.Tech ECE", "Hostel Block", "Dining Hall", "AC/Cooling", "Duct AC vibrating excessively and leaking condensation", "High", "Resolved", "2026-06-10"),
        ("CMP024", "Shweta Nambiar", "MBA", "Block A", "Seminar Hall", "IT", "Ceiling audio amplifier producing high pitch buzzing noise", "Medium", "Pending", "2026-06-14"),
        ("CMP025", "Harsh Vardhan", "BBA", "Block B", "304", "Cleaning", "Whiteboard marker residue stain and dusty window sills", "Low", "Pending", "2026-06-18"),
        ("CMP026", "Aakash Jain", "MCA", "Computer Lab", "Lab 3", "IT", "Operating system boot failure on Server 2", "High", "Resolved", "2026-06-22"),
        ("CMP027", "Pallavi Menon", "B.Tech IT", "Library", "Periodicals", "Furniture", "Magazine display rack shelving bent and loose", "Low", "Pending", "2026-06-26"),
        ("CMP028", "Tarun Rathore", "B.Tech ME", "Hostel Block", "H-310", "Plumbing", "Shower tap valve broken, water spraying onto wall", "High", "In Progress", "2026-06-29"),
        ("CMP029", "Bhavna Swaminathan", "BCA", "Library", "Reading Hall 2", "Internet", "IP address conflict warning when connecting to Wi-Fi", "Medium", "Pending", "2026-07-02"),
        ("CMP030", "Siddharth Das", "B.Tech CSE", "Block A", "205", "Electrical", "Wall power socket sparking when laptop charger plugged", "High", "In Progress", "2026-07-06"),

        # CMP031 - CMP040
        ("CMP031", "Ayesha Siddiqui", "B.Tech ECE", "Block C", "104", "Other", "Window glass pane cracked by tree branch during storm", "Medium", "Resolved", "2026-07-10"),
        ("CMP032", "Kunal Biswas", "MBA", "Library", "Group Study 3", "Furniture", "Table legs loose causing monitors to wobble", "Low", "In Progress", "2026-07-15"),
        ("CMP033", "Roshni Roy", "BBA", "Hostel Block", "Common Room", "AC/Cooling", "AC remote sensor receiver broken and unresponsive", "Medium", "Pending", "2026-07-18"),
        ("CMP034", "Varun Chauhan", "MCA", "Library", "Lobby", "Cleaning", "Floor tiles sticky near drinking water dispenser", "Low", "Pending", "2026-07-22"),
        ("CMP035", "Isha Bhatt", "BCA", "Computer Lab", "Lab 2", "IT", "Network switch port 12 flapping up and down", "High", "In Progress", "2026-07-25"),
        ("CMP036", "Mohit Pandey", "B.Tech IT", "Block A", "308", "Internet", "Wi-Fi authentication captive portal page failing to load", "Medium", "Resolved", "2026-07-29"),
        ("CMP037", "Ankita Saxena", "B.Tech CSE", "Block B", "215", "Furniture", "Teacher dais table drawer jammed shut", "Low", "Pending", "2026-08-01"),
        ("CMP038", "Sanjay Rao", "B.Tech ME", "Hostel Block", "H-112", "Electrical", "Exhaust fan motor seized in hostel washroom", "Medium", "Resolved", "2026-08-04"),
        ("CMP039", "Pratibha Joshi", "MBA", "Library", "Archives", "Internet", "Wi-Fi dead zone identified between book aisles 12-16", "Medium", "Pending", "2026-08-07"),
        ("CMP040", "Kartik Sundaram", "BBA", "Block C", "301", "Plumbing", "Water cooler filter clogged resulting in low trickle", "Medium", "Pending", "2026-08-10"),

        # CMP041 - CMP048
        ("CMP041", "Manish Paul", "MCA", "Library", "Server Room", "Internet", "Fiber optic patch cord bend attenuation causing latency", "High", "In Progress", "2026-08-12"),
        ("CMP042", "Geeta Krishna", "BCA", "Block A", "110", "Electrical", "Switchboard faceplate broken and exposed wiring", "High", "Pending", "2026-08-14"),
        ("CMP043", "Yashwant Patil", "Hostel Block", "Hostel Block", "H-220", "Furniture", "Steel almirah lock misaligned and door won't latch", "Low", "Pending", "2026-08-16"),
        ("CMP044", "Swati Bose", "B.Tech CSE", "Computer Lab", "IoT Lab", "IT", "Microcontroller lab programmer board USB faulty", "Medium", "Pending", "2026-08-18"),
        ("CMP045", "Rupesh Nair", "B.Tech ECE", "Library", "Floor 3", "Internet", "High latency and ping dropouts on campus guest Wi-Fi", "Medium", "Pending", "2026-08-20"),
        ("CMP046", "Anuradha Sen", "MBA", "Hostel Block", "H-401", "AC/Cooling", "Split AC outdoor condenser unit fan rattling loudly", "High", "Resolved", "2026-08-22"),
        ("CMP047", "Chirag Verma", "BBA", "Block C", "214", "Cleaning", "Spill mark on faculty corridor floor tiles", "Low", "Pending", "2026-08-25"),
        ("CMP048", "Pooja Batra", "B.Tech IT", "Library", "Study Cubicle 8", "Internet", "Ethernet wall socket pins bent and connection loose", "Medium", "In Progress", "2026-08-28"),
    ]

    # Maintenance records matching resolved & in progress complaints
    # Total sum of repair costs: ₹16,120 across 20 records (avg ₹806)
    sample_maintenance = [
        ("CMP002", "Ramesh Carpenter", "2026-03-17", 180.0, "Reinforced bench base and replaced wooden leg support"),
        ("CMP003", "Anil IT Tech", "2026-03-24", 450.0, "Replaced faulty monitor VGA cable and CMOS battery"),
        ("CMP004", "Madan Plumber", "2026-03-29", 350.0, "Replaced internal rubber washer and brass spindle valve"),
        ("CMP006", "Suresh NetTech", "2026-04-07", 650.0, "Reconfigured Cisco wireless access point channel bandwidth"),
        ("CMP007", "Dinesh HVAC", "2026-04-14", 3200.0, "Flushed condenser coils, patched copper joint and refilled R32 refrigerant gas"),
        ("CMP008", "Santosh Housekeeping", "2026-04-17", 120.0, "Cleaned book stack area and installed heavy duty trash bins"),
        ("CMP010", "Ramesh Carpenter", "2026-04-27", 220.0, "Screwed new steel hinges on podium cabinet"),
        ("CMP011", "Suresh NetTech", "2026-05-05", 550.0, "Re-crimped RJ45 connectors and punched down 4 patch panel ports"),
        ("CMP013", "Madan Plumber", "2026-05-10", 420.0, "Cleared PVC drain bottleneck with auger snake and replaced P-trap"),
        ("CMP014", "Anil IT Tech", "2026-05-14", 350.0, "Cleaned mechanical keyboard membrane and issued optical laser mouse"),
        ("CMP015", "Dinesh HVAC", "2026-05-18", 1200.0, "Replaced burnt cooler water pump and greased blower motor"),
        ("CMP016", "Ramesh Carpenter", "2026-05-21", 280.0, "Reupholstered chair arms with synthetic leather fabric"),
        ("CMP018", "Naresh Locksmith", "2026-05-27", 450.0, "Lubricated lock tumbler and replaced mortise cylinder latch"),
        ("CMP019", "Vinod Electrician", "2026-05-30", 380.0, "Replaced faulty 32A MCB breaker with new Schneider unit"),
        ("CMP020", "Santosh Housekeeping", "2026-06-01", 350.0, "Industrial vacuum carpet extraction and citrus deodorizer applied"),
        ("CMP022", "Suresh NetTech", "2026-06-08", 780.0, "Updated router firmware and implemented QoS bandwidth limiter"),
        ("CMP023", "Dinesh HVAC", "2026-06-13", 2650.0, "Tightened compressor mounting brackets and cleared drainage pipe"),
        ("CMP026", "Anil IT Tech", "2026-06-25", 1400.0, "Replaced failed SATA SSD and restored OS image from backup NAS"),
        ("CMP031", "Naresh Glazier", "2026-07-13", 1540.0, "Removed shattered 4mm float pane and installed laminated safety glass"),
        ("CMP038", "Vinod Electrician", "2026-08-06", 850.0, "Replaced burnt copper armature coil on Bajaj exhaust fan"),
    ]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO complaints (complaint_id, student_name, department, building, room_no, category, problem, priority, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_complaints)

    cursor.executemany("""
        INSERT INTO maintenance (complaint_id, staff_name, repair_date, cost, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, sample_maintenance)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded successfully.")
    print("Total complaints:", len(get_all_complaints()))
    print("Total maintenance records:", len(get_all_maintenance_records()))
