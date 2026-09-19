"""
main.py - CampusFix: Campus Maintenance Complaint & Tracking System
A modern desktop GUI built with Python Tkinter, SQLite, Pandas, and Matplotlib.
Faithfully recreates the CampusFix theme, navigation, cards, tables, and live analytics.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Matplotlib embedded canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Internal modules
import database as db
import analysis

# Color palette matching CampusFix theme
CLR_BG = "#0B192C"           # Deep Navy background
CLR_NAVBAR = "#0F1E36"       # Slightly lighter navbar
CLR_CARD = "#15263F"         # Card background
CLR_CARD_BORDER = "#1E3A5F"  # Subtle border
CLR_TEXT = "#F8FAFC"         # Crisp white
CLR_MUTED = "#94A3B8"        # Slate muted
CLR_CYAN = "#38BDF8"         # Primary blue/cyan accent
CLR_AMBER = "#F59E0B"        # Warning / Action accent
CLR_GREEN = "#10B981"        # Success / Resolved
CLR_RED = "#EF4444"          # Pending / Urgent
CLR_FORM_BG = "#FDFBF7"      # Clean cream card for registration
CLR_FORM_TEXT = "#0F172A"    # Dark text for registration card


class CampusFixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CampusFix — Maintenance Control System")
        self.geometry("1180x820")
        self.minsize(1050, 720)
        self.configure(bg=CLR_BG)

        # Initialize SQLite database and sample records
        db.init_db()

        # Configure custom TTK styling
        self.setup_styles()

        # Root layout: Header Navbar (top) and Content Container (fill)
        self.create_navbar()

        self.content_frame = tk.Frame(self, bg=CLR_BG)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # View frames dictionary
        self.views = {}
        self.current_view_name = None

        # Build all application views
        self.build_dashboard_view()
        self.build_register_view()
        self.build_tickets_view()
        self.build_reports_view()

        # Show initial view: Dashboard
        self.switch_view("dashboard")

    # ----------------------------------------------------
    # Styles & Themes
    # ----------------------------------------------------
    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Custom.Treeview",
            background="#112240",
            foreground="#E2E8F0",
            fieldbackground="#112240",
            rowheight=30,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#2563EB")],
            foreground=[("selected", "#FFFFFF")]
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#1E3A5F",
            foreground="#F8FAFC",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=6
        )
        style.map("Custom.Treeview.Heading", background=[("active", "#2563EB")])

        # Scrollbar styling
        style.configure("Vertical.TScrollbar", background="#1E3A5F", troughcolor="#0B192C")
        style.configure("Horizontal.TScrollbar", background="#1E3A5F", troughcolor="#0B192C")

        # Combobox styling
        style.configure(
            "TCombobox",
            fieldbackground="#FFFFFF",
            background="#CBD5E1",
            foreground="#0F172A",
            font=("Segoe UI", 10)
        )

    # ----------------------------------------------------
    # Top Navigation Bar
    # ----------------------------------------------------
    def create_navbar(self):
        nav = tk.Frame(self, bg=CLR_NAVBAR, height=65, padx=25)
        nav.pack(side=tk.TOP, fill=tk.X)
        nav.pack_propagate(False)

        # Left branding
        brand_frame = tk.Frame(nav, bg=CLR_NAVBAR)
        brand_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10)

        logo_lbl = tk.Label(
            brand_frame, text="CF", font=("Segoe UI", 12, "bold"),
            bg=CLR_CYAN, fg="#0F172A", width=3, height=1, relief="flat"
        )
        logo_lbl.pack(side=tk.LEFT, padx=(0, 10))

        title_box = tk.Frame(brand_frame, bg=CLR_NAVBAR)
        title_box.pack(side=tk.LEFT)
        lbl_app = tk.Label(title_box, text="CampusFix", font=("Segoe UI", 15, "bold"), fg="#FFFFFF", bg=CLR_NAVBAR)
        lbl_app.pack(anchor="w")
        lbl_sub = tk.Label(title_box, text="MAINTENANCE CONTROL SYSTEM", font=("Segoe UI", 7, "bold"), fg=CLR_MUTED, bg=CLR_NAVBAR)
        lbl_sub.pack(anchor="w")

        # Right CTA Button: + Report an Issue
        cta_btn = tk.Button(
            nav, text="+ Report an Issue", font=("Segoe UI", 10, "bold"),
            bg=CLR_AMBER, fg="#0F172A", activebackground="#D97706", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", padx=16, pady=6,
            command=lambda: self.switch_view("register")
        )
        cta_btn.pack(side=tk.RIGHT, pady=14)

        # Center Navigation Pills
        pills_frame = tk.Frame(nav, bg="#0A1424", padx=5, pady=4)
        pills_frame.pack(side=tk.RIGHT, padx=25, pady=12)

        self.nav_buttons = {}
        items = [
            ("dashboard", "Dashboard"),
            ("register", "Register"),
            ("tickets", "All Tickets"),
            ("reports", "Reports")
        ]

        for key, title in items:
            btn = tk.Button(
                pills_frame, text=title, font=("Segoe UI", 10, "bold"),
                bg="#0A1424", fg=CLR_MUTED, activebackground=CLR_CYAN, activeforeground="#0F172A",
                relief="flat", cursor="hand2", padx=14, pady=4,
                command=lambda k=key: self.switch_view(k)
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.nav_buttons[key] = btn

    def switch_view(self, view_name):
        """Switches the active view in the content container."""
        if self.current_view_name == view_name:
            return

        # Hide current view
        if self.current_view_name and self.current_view_name in self.views:
            self.views[self.current_view_name].pack_forget()

        # Update pill styling
        for key, btn in self.nav_buttons.items():
            if key == view_name:
                btn.configure(bg=CLR_CYAN, fg="#0F172A")
            else:
                btn.configure(bg="#0A1424", fg=CLR_MUTED)

        # Show target view
        self.views[view_name].pack(fill=tk.BOTH, expand=True)
        self.current_view_name = view_name

        # Trigger data refresh for tickets or reports
        if view_name == "tickets":
            self.refresh_tickets_table()
        elif view_name == "reports":
            self.render_reports_view()
        elif view_name == "dashboard":
            self.update_dashboard_stats()

    # ----------------------------------------------------
    # VIEW 1: Dashboard (CampusFix Landing & Schematic Map)
    # ----------------------------------------------------
    def build_dashboard_view(self):
        view = tk.Frame(self.content_frame, bg=CLR_BG, padx=40, pady=25)
        self.views["dashboard"] = view

        # Hero Banner
        top_badge = tk.Label(
            view, text="  ● LIVE ACROSS 6 CAMPUS BUILDINGS  ",
            font=("Segoe UI", 9, "bold"), fg=CLR_GREEN, bg="#0E2A38",
            relief="flat", padx=8, pady=4
        )
        top_badge.pack(anchor="w", pady=(0, 10))

        hero_title = tk.Label(
            view,
            text="EVERY SQUEAK, LEAK, AND FLICKER —\nLOGGED, TRACKED, FIXED.",
            font=("Impact", 28), fg="#FFFFFF", bg=CLR_BG, justify=tk.LEFT
        )
        hero_title.pack(anchor="w")

        hero_sub = tk.Label(
            view,
            text="CampusFix turns scattered maintenance complaints into a single work-order board —\n"
                 "from the moment a student reports a broken fan to the day a technician closes the ticket.",
            font=("Segoe UI", 11), fg=CLR_MUTED, bg=CLR_BG, justify=tk.LEFT
        )
        hero_sub.pack(anchor="w", pady=(10, 20))

        # CTA buttons
        btn_bar = tk.Frame(view, bg=CLR_BG)
        btn_bar.pack(anchor="w", pady=(0, 25))

        btn_console = tk.Button(
            btn_bar, text="Open the Console", font=("Segoe UI", 11, "bold"),
            bg=CLR_CYAN, fg="#0F172A", relief="flat", cursor="hand2", padx=20, pady=9,
            command=lambda: self.switch_view("tickets")
        )
        btn_console.pack(side=tk.LEFT, padx=(0, 15))

        btn_report = tk.Button(
            btn_bar, text="Report an Issue →", font=("Segoe UI", 11, "bold"),
            bg=CLR_CARD, fg="#FFFFFF", relief="flat", highlightthickness=1,
            highlightbackground=CLR_CYAN, cursor="hand2", padx=20, pady=9,
            command=lambda: self.switch_view("register")
        )
        btn_report.pack(side=tk.LEFT)

        # Campus Schematic Map / Pins Card
        pins_container = tk.Frame(view, bg=CLR_CARD, bd=1, relief="solid", padx=25, pady=20)
        pins_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        map_lbl = tk.Label(
            pins_container, text="ACTIVE CAMPUS HOTSPOTS",
            font=("Segoe UI", 10, "bold"), fg=CLR_MUTED, bg=CLR_CARD
        )
        map_lbl.pack(anchor="w", pady=(0, 12))

        # 4 Hotspot Cards
        cards_row = tk.Frame(pins_container, bg=CLR_CARD)
        cards_row.pack(fill=tk.BOTH, expand=True)

        hotspots = [
            ("Block A · Rm 204", "Fan not working", "● Pending", CLR_RED),
            ("Library · 2nd Floor", "Wi-Fi down", "● In Progress", CLR_AMBER),
            ("Computer Lab · Lab 2", "Projector fault", "● Pending", CLR_RED),
            ("Block C · Rm 118", "Tap leakage", "● Resolved", CLR_GREEN),
        ]

        for i, (loc, issue, st_text, st_color) in enumerate(hotspots):
            c = tk.Frame(cards_row, bg="#0E1E34", padx=16, pady=14, relief="flat")
            c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)

            tk.Label(c, text=loc, font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#0E1E34").pack(anchor="w")
            tk.Label(c, text=issue, font=("Segoe UI", 10), fg=CLR_MUTED, bg="#0E1E34").pack(anchor="w", pady=4)
            tk.Label(c, text=st_text, font=("Segoe UI", 9, "bold"), fg=st_color, bg="#0E1E34").pack(anchor="w")

        # Bottom Quick Status Bar
        self.dash_status_lbl = tk.Label(
            view, text="Loading system metrics...",
            font=("Segoe UI", 10, "bold"), fg=CLR_CYAN, bg=CLR_BG
        )
        self.dash_status_lbl.pack(anchor="w", pady=(10, 0))

    def update_dashboard_stats(self):
        """Updates bottom metrics label on Dashboard."""
        m = analysis.calculate_metrics()
        txt = f"📊 System Overview:  {m['total_complaints']} Total Complaints  |  {m['pending']} Pending  |  {m['in_progress']} In Progress  |  {m['resolved']} Resolved  |  Total Spend: ₹{m['total_cost']:,.2f}"
        self.dash_status_lbl.config(text=txt)

    # ----------------------------------------------------
    # VIEW 2: Register Complaint (Cream Card matching Screenshot 3)
    # ----------------------------------------------------
    def build_register_view(self):
        view = tk.Frame(self.content_frame, bg=CLR_BG, padx=40, pady=25)
        self.views["register"] = view

        title_lbl = tk.Label(view, text="REGISTER A COMPLAINT", font=("Impact", 24), fg="#FFFFFF", bg=CLR_BG)
        title_lbl.pack(anchor="w")
        sub_lbl = tk.Label(
            view, text="Fill in the details below — a ticket ID is generated automatically.",
            font=("Segoe UI", 10), fg=CLR_MUTED, bg=CLR_BG
        )
        sub_lbl.pack(anchor="w", pady=(4, 18))

        # Main Card (Styled warm cream card matching Screenshot 3)
        card = tk.Frame(view, bg=CLR_FORM_BG, bd=1, relief="flat", padx=35, pady=25)
        card.pack(fill=tk.BOTH, expand=True)

        # "NEW TICKET" stamp badge in top-right
        stamp_frame = tk.Frame(card, bg=CLR_FORM_BG)
        stamp_frame.pack(fill=tk.X)
        badge = tk.Label(
            stamp_frame, text="NEW TICKET", font=("Impact", 11),
            fg="#B91C1C", bg="#FEE2E2", padx=10, pady=3, relief="solid", bd=1
        )
        badge.pack(side=tk.RIGHT)

        # Form grid
        form = tk.Frame(card, bg=CLR_FORM_BG)
        form.pack(fill=tk.BOTH, expand=True, pady=(10, 15))
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        # Row 1: Student Name & Department
        lbl_sname = tk.Label(form, text="STUDENT NAME *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_sname.grid(row=0, column=0, sticky="w", padx=(0, 15), pady=(5, 2))
        self.entry_name = tk.Entry(form, font=("Segoe UI", 10), bg="#FFFFFF", fg=CLR_FORM_TEXT, relief="solid", bd=1)
        self.entry_name.grid(row=1, column=0, sticky="ew", padx=(0, 15), pady=(0, 12), ipady=5)

        lbl_dept = tk.Label(form, text="DEPARTMENT *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_dept.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=(5, 2))
        self.combo_dept = ttk.Combobox(form, font=("Segoe UI", 10), state="readonly", values=[
            "BCA", "B.Tech CSE", "B.Tech ECE", "B.Tech ME", "B.Tech IT", "MCA", "MBA", "BBA", "Other"
        ])
        self.combo_dept.set("Select department")
        self.combo_dept.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=(0, 12), ipady=3)

        # Row 2: Building & Room No
        lbl_bld = tk.Label(form, text="BUILDING *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_bld.grid(row=2, column=0, sticky="w", padx=(0, 15), pady=(5, 2))
        self.combo_bld = ttk.Combobox(form, font=("Segoe UI", 10), state="readonly", values=[
            "Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"
        ])
        self.combo_bld.set("Select building")
        self.combo_bld.grid(row=3, column=0, sticky="ew", padx=(0, 15), pady=(0, 12), ipady=3)

        lbl_room = tk.Label(form, text="ROOM NO. *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_room.grid(row=2, column=1, sticky="w", padx=(15, 0), pady=(5, 2))
        self.entry_room = tk.Entry(form, font=("Segoe UI", 10), bg="#FFFFFF", fg=CLR_FORM_TEXT, relief="solid", bd=1)
        self.entry_room.grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=(0, 12), ipady=5)

        # Row 3: Category & Priority
        lbl_cat = tk.Label(form, text="CATEGORY *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_cat.grid(row=4, column=0, sticky="w", padx=(0, 15), pady=(5, 2))
        self.combo_cat = ttk.Combobox(form, font=("Segoe UI", 10), state="readonly", values=[
            "Electrical", "Furniture", "Plumbing", "IT", "Internet", "Cleaning", "AC/Cooling", "Other"
        ])
        self.combo_cat.set("Select category")
        self.combo_cat.grid(row=5, column=0, sticky="ew", padx=(0, 15), pady=(0, 12), ipady=3)

        lbl_prio = tk.Label(form, text="PRIORITY *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_prio.grid(row=4, column=1, sticky="w", padx=(15, 0), pady=(5, 2))
        self.combo_prio = ttk.Combobox(form, font=("Segoe UI", 10), state="readonly", values=["Low", "Medium", "High"])
        self.combo_prio.set("Select priority")
        self.combo_prio.grid(row=5, column=1, sticky="ew", padx=(15, 0), pady=(0, 12), ipady=3)

        # Row 4: Problem Description
        lbl_prob = tk.Label(form, text="PROBLEM DESCRIPTION *", font=("Segoe UI", 9, "bold"), fg="#475569", bg=CLR_FORM_BG)
        lbl_prob.grid(row=6, column=0, columnspan=2, sticky="w", pady=(5, 2))
        self.txt_prob = tk.Text(form, font=("Segoe UI", 10), height=4, bg="#FFFFFF", fg=CLR_FORM_TEXT, relief="solid", bd=1)
        self.txt_prob.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Bottom Action
        act_box = tk.Frame(card, bg=CLR_FORM_BG)
        act_box.pack(anchor="w")

        btn_submit = tk.Button(
            act_box, text="Register complaint", font=("Segoe UI", 11, "bold"),
            bg="#0F1E36", fg="#FFFFFF", activebackground="#2563EB", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", padx=24, pady=10,
            command=self.handle_register_complaint
        )
        btn_submit.pack(side=tk.LEFT)

        note_lbl = tk.Label(
            act_box, text="Date & ticket ID are assigned automatically on submit.",
            font=("Segoe UI", 9), fg="#64748B", bg=CLR_FORM_BG
        )
        note_lbl.pack(side=tk.LEFT, padx=15)

    def handle_register_complaint(self):
        """Validates form and inserts complaint into SQLite."""
        name = self.entry_name.get().strip()
        dept = self.combo_dept.get()
        bld = self.combo_bld.get()
        room = self.entry_room.get().strip()
        cat = self.combo_cat.get()
        prio = self.combo_prio.get()
        problem = self.txt_prob.get("1.0", tk.END).strip()

        # Validation per Section 20 of project guide
        if not name:
            messagebox.showerror("Validation Error", "Student Name cannot be empty.")
            self.entry_name.focus()
            return
        if dept in ["Select department", ""]:
            messagebox.showerror("Validation Error", "Please select a valid Department.")
            return
        if bld in ["Select building", ""]:
            messagebox.showerror("Validation Error", "Please select a valid Building.")
            return
        if not room:
            messagebox.showerror("Validation Error", "Room No. cannot be empty.")
            self.entry_room.focus()
            return
        if cat in ["Select category", ""]:
            messagebox.showerror("Validation Error", "Please select a Problem Category.")
            return
        if prio in ["Select priority", ""]:
            prio = "Medium"
        if not problem:
            messagebox.showerror("Validation Error", "Problem description cannot be empty.")
            self.txt_prob.focus()
            return

        try:
            cid = db.add_complaint(
                student_name=name,
                department=dept,
                building=bld,
                room_no=room,
                category=cat,
                problem=problem,
                priority=prio,
                status="Pending"
            )

            messagebox.showinfo(
                "Complaint Registered",
                f"Complaint Registered Successfully!\n\n"
                f"Ticket ID: {cid}\n"
                f"Status: Pending\n"
                f"Student: {name} ({dept})\n"
                f"Location: {bld} - Room {room}"
            )

            # Reset form inputs
            self.entry_name.delete(0, tk.END)
            self.entry_room.delete(0, tk.END)
            self.txt_prob.delete("1.0", tk.END)
            self.combo_dept.set("Select department")
            self.combo_bld.set("Select building")
            self.combo_cat.set("Select category")
            self.combo_prio.set("Select priority")

            # Switch to tickets view to show the newly added ticket
            self.switch_view("tickets")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while saving complaint:\n{str(e)}")

    # ----------------------------------------------------
    # VIEW 3: All Tickets (View, Search, Update Status, Add Maintenance)
    # ----------------------------------------------------
    def build_tickets_view(self):
        view = tk.Frame(self.content_frame, bg=CLR_BG, padx=30, pady=20)
        self.views["tickets"] = view

        # Header with Search & Filters
        top_bar = tk.Frame(view, bg=CLR_BG)
        top_bar.pack(fill=tk.X, pady=(0, 12))

        lbl_t = tk.Label(top_bar, text="ALL MAINTENANCE TICKETS", font=("Impact", 22), fg="#FFFFFF", bg=CLR_BG)
        lbl_t.pack(side=tk.LEFT)

        # Filters on the right
        filters_frame = tk.Frame(top_bar, bg=CLR_BG)
        filters_frame.pack(side=tk.RIGHT)

        tk.Label(filters_frame, text="Status:", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_BG).pack(side=tk.LEFT, padx=(5, 3))
        self.filter_status = ttk.Combobox(filters_frame, width=12, state="readonly", values=["All", "Pending", "In Progress", "Resolved"])
        self.filter_status.set("All")
        self.filter_status.pack(side=tk.LEFT, padx=3)
        self.filter_status.bind("<<ComboboxSelected>>", lambda e: self.refresh_tickets_table())

        tk.Label(filters_frame, text="Building:", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_BG).pack(side=tk.LEFT, padx=(8, 3))
        self.filter_bld = ttk.Combobox(filters_frame, width=13, state="readonly", values=["All", "Block A", "Block B", "Block C", "Computer Lab", "Library", "Hostel Block"])
        self.filter_bld.set("All")
        self.filter_bld.pack(side=tk.LEFT, padx=3)
        self.filter_bld.bind("<<ComboboxSelected>>", lambda e: self.refresh_tickets_table())

        # Search Bar Row
        search_bar = tk.Frame(view, bg=CLR_CARD, padx=12, pady=10)
        search_bar.pack(fill=tk.X, pady=(0, 12))

        tk.Label(search_bar, text="🔍 Search:", font=("Segoe UI", 10, "bold"), fg=CLR_CYAN, bg=CLR_CARD).pack(side=tk.LEFT, padx=(0, 8))
        self.search_entry = tk.Entry(search_bar, font=("Segoe UI", 10), bg="#0B192C", fg="#FFFFFF", relief="flat", insertbackground="#FFFFFF", width=35)
        self.search_entry.pack(side=tk.LEFT, ipady=4, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.refresh_tickets_table())

        btn_search = tk.Button(
            search_bar, text="Search", font=("Segoe UI", 9, "bold"),
            bg=CLR_CYAN, fg="#0F172A", relief="flat", cursor="hand2", padx=14, pady=3,
            command=self.refresh_tickets_table
        )
        btn_search.pack(side=tk.LEFT, padx=4)

        btn_clear = tk.Button(
            search_bar, text="Reset", font=("Segoe UI", 9),
            bg="#1E3A5F", fg="#FFFFFF", relief="flat", cursor="hand2", padx=12, pady=3,
            command=self.reset_search
        )
        btn_clear.pack(side=tk.LEFT, padx=4)

        self.lbl_result_count = tk.Label(search_bar, text="", font=("Segoe UI", 9), fg=CLR_MUTED, bg=CLR_CARD)
        self.lbl_result_count.pack(side=tk.RIGHT)

        # Treeview Table
        tree_frame = tk.Frame(view, bg=CLR_CARD)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("complaint_id", "student_name", "department", "building", "room_no", "category", "priority", "status", "date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview", selectmode="browse")

        col_defs = [
            ("complaint_id", "Ticket ID", 90, "center"),
            ("student_name", "Student Name", 140, "w"),
            ("department", "Department", 100, "center"),
            ("building", "Building", 120, "w"),
            ("room_no", "Room", 75, "center"),
            ("category", "Category", 110, "w"),
            ("priority", "Priority", 90, "center"),
            ("status", "Status", 110, "center"),
            ("date", "Reported Date", 105, "center"),
        ]

        for cid, heading, width, anchor in col_defs:
            self.tree.heading(cid, text=heading)
            self.tree.column(cid, width=width, anchor=anchor)

        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview, style="Horizontal.TScrollbar")
        self.tree.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Row color tags
        self.tree.tag_configure("Pending", foreground="#F87171")       # Coral Red
        self.tree.tag_configure("In Progress", foreground="#38BDF8")   # Cyan Blue
        self.tree.tag_configure("Resolved", foreground="#34D399")      # Emerald Green

        # Bottom Action Bar
        act_frame = tk.Frame(view, bg=CLR_BG, pady=12)
        act_frame.pack(fill=tk.X)

        btn_status = tk.Button(
            act_frame, text="✏ Update Status", font=("Segoe UI", 10, "bold"),
            bg="#2563EB", fg="#FFFFFF", relief="flat", cursor="hand2", padx=16, pady=6,
            command=self.open_update_status_modal
        )
        btn_status.pack(side=tk.LEFT, padx=(0, 10))

        btn_maint = tk.Button(
            act_frame, text="🔧 Add Maintenance Details", font=("Segoe UI", 10, "bold"),
            bg=CLR_AMBER, fg="#0F172A", relief="flat", cursor="hand2", padx=16, pady=6,
            command=self.open_add_maintenance_modal
        )
        btn_maint.pack(side=tk.LEFT, padx=(0, 10))

        btn_view_det = tk.Button(
            act_frame, text="📋 Ticket Details", font=("Segoe UI", 10),
            bg=CLR_CARD, fg="#FFFFFF", relief="flat", cursor="hand2", padx=14, pady=6,
            command=self.open_ticket_details_modal
        )
        btn_view_det.pack(side=tk.LEFT, padx=(0, 10))

        btn_refresh = tk.Button(
            act_frame, text="🔄 Refresh", font=("Segoe UI", 10),
            bg="#1E3A5F", fg="#FFFFFF", relief="flat", cursor="hand2", padx=14, pady=6,
            command=self.refresh_tickets_table
        )
        btn_refresh.pack(side=tk.RIGHT)

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.filter_status.set("All")
        self.filter_bld.set("All")
        self.refresh_tickets_table()

    def refresh_tickets_table(self):
        """Fetches complaints and repopulates the Treeview."""
        term = self.search_entry.get().strip()
        status_val = self.filter_status.get()
        bld_val = self.filter_bld.get()

        records = db.get_all_complaints(
            search_term=term if term else None,
            status_filter=status_val,
            building_filter=bld_val
        )

        # Clear existing items
        for row in self.tree.get_children():
            self.tree.delete(row)

        for rec in records:
            st = rec["status"]
            self.tree.insert("", tk.END, values=(
                rec["complaint_id"],
                rec["student_name"],
                rec["department"],
                rec["building"],
                rec["room_no"],
                rec["category"],
                rec["priority"],
                st,
                rec["date"]
            ), tags=(st,))

        self.lbl_result_count.config(text=f"Showing {len(records)} tickets")

    def get_selected_ticket_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a ticket from the table first.")
            return None
        values = self.tree.item(selected[0], "values")
        return values[0]

    # Modal: Update Status
    def open_update_status_modal(self):
        cid = self.get_selected_ticket_id()
        if not cid:
            return

        complaint = db.get_complaint_by_id(cid)
        if not complaint:
            messagebox.showerror("Error", f"Ticket {cid} not found.")
            return

        modal = tk.Toplevel(self)
        modal.title(f"Update Status — {cid}")
        modal.geometry("420x280")
        modal.configure(bg=CLR_CARD)
        modal.transient(self)
        modal.grab_set()

        tk.Label(modal, text=f"Update Status: {cid}", font=("Segoe UI", 13, "bold"), fg="#FFFFFF", bg=CLR_CARD).pack(pady=(20, 5))
        tk.Label(modal, text=f"{complaint['student_name']} • {complaint['building']} - Rm {complaint['room_no']}", font=("Segoe UI", 9), fg=CLR_MUTED, bg=CLR_CARD).pack(pady=(0, 15))

        f = tk.Frame(modal, bg=CLR_CARD)
        f.pack(pady=10)

        tk.Label(f, text="Current Status:", font=("Segoe UI", 10), fg=CLR_MUTED, bg=CLR_CARD).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(f, text=complaint["status"], font=("Segoe UI", 10, "bold"), fg=CLR_CYAN, bg=CLR_CARD).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        tk.Label(f, text="New Status:", font=("Segoe UI", 10, "bold"), fg="#FFFFFF", bg=CLR_CARD).grid(row=1, column=0, sticky="w", pady=10)
        status_combo = ttk.Combobox(f, font=("Segoe UI", 10), state="readonly", values=["Pending", "In Progress", "Resolved"])
        status_combo.set(complaint["status"])
        status_combo.grid(row=1, column=1, padx=10, pady=10)

        def save():
            new_st = status_combo.get()
            db.update_complaint_status(cid, new_st)
            messagebox.showinfo("Status Updated", f"Ticket {cid} status updated to: {new_st}")
            modal.destroy()
            self.refresh_tickets_table()

        btn_save = tk.Button(modal, text="Save Status", font=("Segoe UI", 10, "bold"), bg=CLR_CYAN, fg="#0F172A", relief="flat", padx=20, pady=6, command=save)
        btn_save.pack(pady=15)

    # Modal: Add Maintenance Details
    def open_add_maintenance_modal(self):
        cid = self.get_selected_ticket_id()
        if not cid:
            return

        complaint = db.get_complaint_by_id(cid)
        if not complaint:
            messagebox.showerror("Error", f"Ticket {cid} not found.")
            return

        modal = tk.Toplevel(self)
        modal.title(f"Add Maintenance Details — {cid}")
        modal.geometry("480x420")
        modal.configure(bg=CLR_CARD)
        modal.transient(self)
        modal.grab_set()

        tk.Label(modal, text=f"Maintenance Log — {cid}", font=("Segoe UI", 13, "bold"), fg="#FFFFFF", bg=CLR_CARD).pack(pady=(15, 2))
        tk.Label(modal, text=f"Issue: {complaint['problem']}", font=("Segoe UI", 9), fg=CLR_MUTED, bg=CLR_CARD).pack(pady=(0, 15))

        f = tk.Frame(modal, bg=CLR_CARD)
        f.pack(fill=tk.X, padx=30)
        f.columnconfigure(1, weight=1)

        tk.Label(f, text="Staff Name *", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_CARD).grid(row=0, column=0, sticky="w", pady=5)
        e_staff = tk.Entry(f, font=("Segoe UI", 10), bg="#0B192C", fg="#FFFFFF", relief="flat", insertbackground="#FFFFFF")
        e_staff.grid(row=0, column=1, sticky="ew", pady=5, ipady=3)

        tk.Label(f, text="Repair Date *", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_CARD).grid(row=1, column=0, sticky="w", pady=5)
        e_date = tk.Entry(f, font=("Segoe UI", 10), bg="#0B192C", fg="#FFFFFF", relief="flat", insertbackground="#FFFFFF")
        e_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        e_date.grid(row=1, column=1, sticky="ew", pady=5, ipady=3)

        tk.Label(f, text="Repair Cost (₹) *", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_CARD).grid(row=2, column=0, sticky="w", pady=5)
        e_cost = tk.Entry(f, font=("Segoe UI", 10), bg="#0B192C", fg="#FFFFFF", relief="flat", insertbackground="#FFFFFF")
        e_cost.insert(0, "500")
        e_cost.grid(row=2, column=1, sticky="ew", pady=5, ipady=3)

        tk.Label(f, text="Remarks *", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_CARD).grid(row=3, column=0, sticky="nw", pady=5)
        t_rem = tk.Text(f, font=("Segoe UI", 10), height=3, bg="#0B192C", fg="#FFFFFF", relief="flat", insertbackground="#FFFFFF")
        t_rem.grid(row=3, column=1, sticky="ew", pady=5)

        tk.Label(f, text="Update Status:", font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg=CLR_CARD).grid(row=4, column=0, sticky="w", pady=5)
        combo_st = ttk.Combobox(f, font=("Segoe UI", 9), state="readonly", values=["In Progress", "Resolved"])
        combo_st.set("Resolved")
        combo_st.grid(row=4, column=1, sticky="w", pady=5)

        def save_maint():
            staff = e_staff.get().strip()
            rdate = e_date.get().strip()
            cost_str = e_cost.get().strip()
            remarks = t_rem.get("1.0", tk.END).strip()
            new_st = combo_st.get()

            if not staff:
                messagebox.showerror("Error", "Staff Name is required.")
                return
            if not remarks:
                messagebox.showerror("Error", "Repair remarks are required.")
                return
            try:
                cost = float(cost_str)
                if cost < 0:
                    raise ValueError("Cost cannot be negative.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid non-negative repair cost.")
                return

            db.add_maintenance_record(cid, staff, rdate, cost, remarks)
            db.update_complaint_status(cid, new_st)
            messagebox.showinfo("Success", f"Maintenance details saved for {cid}!\nStatus set to: {new_st}")
            modal.destroy()
            self.refresh_tickets_table()

        btn_save = tk.Button(modal, text="Save Maintenance Record", font=("Segoe UI", 10, "bold"), bg=CLR_GREEN, fg="#0F172A", relief="flat", padx=20, pady=7, command=save_maint)
        btn_save.pack(pady=15)

    # Modal: Ticket Details
    def open_ticket_details_modal(self):
        cid = self.get_selected_ticket_id()
        if not cid:
            return

        complaint = db.get_complaint_by_id(cid)
        maint_list = db.get_maintenance_for_complaint(cid)

        modal = tk.Toplevel(self)
        modal.title(f"Ticket Details — {cid}")
        modal.geometry("540x520")
        modal.configure(bg=CLR_CARD)
        modal.transient(self)

        tk.Label(modal, text=f"TICKET DETAILS — {cid}", font=("Segoe UI", 13, "bold"), fg="#FFFFFF", bg=CLR_CARD).pack(pady=(15, 10))

        info_box = tk.Frame(modal, bg="#0E1E34", padx=20, pady=15)
        info_box.pack(fill=tk.X, padx=25, pady=5)

        fields = [
            ("Student:", f"{complaint['student_name']} ({complaint['department']})"),
            ("Location:", f"{complaint['building']} - Room {complaint['room_no']}"),
            ("Category:", f"{complaint['category']} | Priority: {complaint['priority']}"),
            ("Status:", complaint["status"]),
            ("Reported Date:", complaint["date"]),
            ("Problem:", complaint["problem"]),
        ]

        for r, (lbl, val) in enumerate(fields):
            tk.Label(info_box, text=lbl, font=("Segoe UI", 9, "bold"), fg=CLR_MUTED, bg="#0E1E34").grid(row=r, column=0, sticky="w", pady=2)
            tk.Label(info_box, text=val, font=("Segoe UI", 9), fg="#FFFFFF", bg="#0E1E34", wraplength=350, justify=tk.LEFT).grid(row=r, column=1, sticky="w", padx=10, pady=2)

        # Maintenance History section
        tk.Label(modal, text="MAINTENANCE REPAIR HISTORY", font=("Segoe UI", 11, "bold"), fg=CLR_CYAN, bg=CLR_CARD).pack(anchor="w", padx=25, pady=(15, 5))

        hist_box = tk.Frame(modal, bg="#0E1E34", padx=15, pady=10)
        hist_box.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 15))

        if maint_list:
            for item in maint_list:
                line = f"• {item['repair_date']} by {item['staff_name']} | ₹{item['cost']:,.2f}\n  Remarks: {item['remarks']}"
                tk.Label(hist_box, text=line, font=("Segoe UI", 9), fg="#FFFFFF", bg="#0E1E34", justify=tk.LEFT, wraplength=450).pack(anchor="w", pady=4)
        else:
            tk.Label(hist_box, text="No repair records yet. Ticket is pending technician assignment.", font=("Segoe UI", 9, "italic"), fg=CLR_MUTED, bg="#0E1E34").pack(pady=10)

    # ----------------------------------------------------
    # VIEW 4: Reports & Live Data Visualizations (Screenshots 1 & 2)
    # ----------------------------------------------------
    def build_reports_view(self):
        view = tk.Frame(self.content_frame, bg=CLR_BG)
        self.views["reports"] = view

        # Top banner with Title & CSV Export Button
        top_frame = tk.Frame(view, bg=CLR_BG, padx=30, pady=15)
        top_frame.pack(fill=tk.X)

        title_box = tk.Frame(top_frame, bg=CLR_BG)
        title_box.pack(side=tk.LEFT)
        tk.Label(title_box, text="REPORTS & ANALYSIS", font=("Impact", 22), fg="#FFFFFF", bg=CLR_BG).pack(anchor="w")
        tk.Label(title_box, text="Everything Pandas would have crunched — rendered live.", font=("Segoe UI", 10), fg=CLR_MUTED, bg=CLR_BG).pack(anchor="w")

        btn_export = tk.Button(
            top_frame, text="📄 Export tickets to CSV", font=("Segoe UI", 10, "bold"),
            bg=CLR_CARD, fg=CLR_CYAN, relief="solid", bd=1, cursor="hand2", padx=16, pady=6,
            command=self.handle_export_csv
        )
        btn_export.pack(side=tk.RIGHT, pady=5)

        # Scrollable container for KPI Cards + Matplotlib Charts
        container = tk.Frame(view, bg=CLR_BG)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=CLR_BG, highlightthickness=0)
        v_scroll = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        self.reports_scroll_frame = tk.Frame(canvas, bg=CLR_BG, padx=30)

        self.reports_scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.reports_scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scroll.set)

        # Mousewheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.reports_canvas = canvas

    def render_reports_view(self):
        """Computes metrics with Pandas and embeds 5 Matplotlib figures into the canvas."""
        # Clear existing widgets in scroll frame
        for widget in self.reports_scroll_frame.winfo_children():
            widget.destroy()

        metrics = analysis.calculate_metrics()
        df_complaints, df_maintenance = analysis.load_data()

        # Row of 8 KPI Cards (Matching Screenshot 2)
        kpi_frame = tk.Frame(self.reports_scroll_frame, bg=CLR_BG)
        kpi_frame.pack(fill=tk.X, pady=(0, 20))

        # Top 4 cards
        row1 = tk.Frame(kpi_frame, bg=CLR_BG)
        row1.pack(fill=tk.X, pady=4)
        for i in range(4):
            row1.columnconfigure(i, weight=1)

        kpis_r1 = [
            (str(metrics["total_complaints"]), "TOTAL COMPLAINTS", CLR_CYAN),
            (str(metrics["pending"]), "PENDING", CLR_RED),
            (str(metrics["in_progress"]), "IN PROGRESS", CLR_CYAN),
            (str(metrics["resolved"]), "RESOLVED", CLR_GREEN),
        ]
        for col, (val, title, clr) in enumerate(kpis_r1):
            c = tk.Frame(row1, bg=CLR_CARD, padx=16, pady=12, highlightbackground=CLR_CARD_BORDER, highlightthickness=1)
            c.grid(row=0, column=col, sticky="ew", padx=5)
            tk.Label(c, text=val, font=("Segoe UI", 20, "bold"), fg=clr, bg=CLR_CARD).pack(anchor="w")
            tk.Label(c, text=title, font=("Segoe UI", 8, "bold"), fg=CLR_MUTED, bg=CLR_CARD).pack(anchor="w")

        # Bottom 4 cards
        row2 = tk.Frame(kpi_frame, bg=CLR_BG)
        row2.pack(fill=tk.X, pady=4)
        for i in range(4):
            row2.columnconfigure(i, weight=1)

        kpis_r2 = [
            (f"₹{int(metrics['total_cost']):,}", "TOTAL MAINTENANCE COST", CLR_CYAN),
            (f"₹{int(metrics['avg_cost']):,}", "AVERAGE REPAIR COST", CLR_CYAN),
            (str(metrics["most_common_category"]), "MOST COMMON CATEGORY", CLR_CYAN),
            (str(metrics["most_reported_building"]), "MOST REPORTED BUILDING", CLR_CYAN),
        ]
        for col, (val, title, clr) in enumerate(kpis_r2):
            c = tk.Frame(row2, bg=CLR_CARD, padx=16, pady=12, highlightbackground=CLR_CARD_BORDER, highlightthickness=1)
            c.grid(row=0, column=col, sticky="ew", padx=5)
            tk.Label(c, text=val, font=("Segoe UI", 16, "bold"), fg=clr, bg=CLR_CARD).pack(anchor="w")
            tk.Label(c, text=title, font=("Segoe UI", 8, "bold"), fg=CLR_MUTED, bg=CLR_CARD).pack(anchor="w")

        # Charts Section
        # Chart Row 1: Complaints by Category & Status Distribution
        charts_row1 = tk.Frame(self.reports_scroll_frame, bg=CLR_BG)
        charts_row1.pack(fill=tk.X, pady=(5, 15))

        fig1 = analysis.generate_category_bar_chart(df_complaints)
        canv1 = FigureCanvasTkAgg(fig1, master=charts_row1)
        canv1.draw()
        canv1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        fig2 = analysis.generate_status_pie_chart(df_complaints)
        canv2 = FigureCanvasTkAgg(fig2, master=charts_row1)
        canv2.draw()
        canv2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chart Row 2: Complaints by Building & Monthly Trend (Matching Screenshot 1)
        charts_row2 = tk.Frame(self.reports_scroll_frame, bg=CLR_BG)
        charts_row2.pack(fill=tk.X, pady=(0, 15))

        fig3 = analysis.generate_building_bar_chart(df_complaints)
        canv3 = FigureCanvasTkAgg(fig3, master=charts_row2)
        canv3.draw()
        canv3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        fig4 = analysis.generate_monthly_trend_chart(df_complaints)
        canv4 = FigureCanvasTkAgg(fig4, master=charts_row2)
        canv4.draw()
        canv4.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chart Row 3: Repair Cost by Category (Matching Screenshot 1)
        charts_row3 = tk.Frame(self.reports_scroll_frame, bg=CLR_BG)
        charts_row3.pack(fill=tk.X, pady=(0, 25))

        fig5 = analysis.generate_repair_cost_chart(df_complaints, df_maintenance)
        canv5 = FigureCanvasTkAgg(fig5, master=charts_row3)
        canv5.draw()
        canv5.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def handle_export_csv(self):
        """Exports complaints and repair records to CSV file using Pandas."""
        success, res = analysis.export_to_csv()
        if success:
            messagebox.showinfo("Export Successful", f"Tickets exported successfully to:\n{res}")
        else:
            messagebox.showerror("Export Failed", f"Could not export tickets:\n{res}")


if __name__ == "__main__":
    app = CampusFixApp()
    app.mainloop()
