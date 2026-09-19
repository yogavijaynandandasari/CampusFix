"""
analysis.py - Analytics and Visualization Layer for CampusFix
Performs data aggregation with Pandas and renders dark-themed Matplotlib charts.
"""

import os
import sqlite3
import pandas as pd
import matplotlib
# Use TkAgg backend when running in desktop GUI
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DB_PATH = os.path.join(DATA_DIR, "campus.db")

# Theme color constants matching the dark navy reference UI
BG_DARK = "#0B192C"
CARD_BG = "#15263F"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
GRID_COLOR = "#1E293B"
CYAN_ACCENT = "#38BDF8"
AMBER_ACCENT = "#F59E0B"
GREEN_ACCENT = "#10B981"
RED_ACCENT = "#EF4444"
PURPLE_ACCENT = "#A855F7"


def load_data(db_path=DB_PATH):
    """Loads complaints and maintenance tables into Pandas DataFrames."""
    if not os.path.exists(db_path):
        return pd.DataFrame(), pd.DataFrame()

    conn = sqlite3.connect(db_path)
    df_complaints = pd.read_sql_query("SELECT * FROM complaints", conn)
    df_maintenance = pd.read_sql_query("SELECT * FROM maintenance", conn)
    conn.close()

    return df_complaints, df_maintenance


def calculate_metrics(db_path=DB_PATH):
    """
    Computes all analytical KPIs required by Section 16 & 18 of the project guide:
    - Total complaints
    - Pending, In Progress, Resolved counts
    - Total maintenance cost & average repair cost
    - Most common category
    - Building with highest number of complaints
    """
    df_complaints, df_maintenance = load_data(db_path)

    metrics = {
        "total_complaints": 0,
        "pending": 0,
        "in_progress": 0,
        "resolved": 0,
        "total_cost": 0.0,
        "avg_cost": 0.0,
        "most_common_category": "N/A",
        "most_reported_building": "N/A",
    }

    if not df_complaints.empty:
        metrics["total_complaints"] = len(df_complaints)
        status_counts = df_complaints["status"].value_counts().to_dict()
        metrics["pending"] = status_counts.get("Pending", 0)
        metrics["in_progress"] = status_counts.get("In Progress", 0)
        metrics["resolved"] = status_counts.get("Resolved", 0)

        if "category" in df_complaints.columns and not df_complaints["category"].empty:
            metrics["most_common_category"] = df_complaints["category"].mode().iloc[0]

        if "building" in df_complaints.columns and not df_complaints["building"].empty:
            metrics["most_reported_building"] = df_complaints["building"].mode().iloc[0]

    if not df_maintenance.empty and "cost" in df_maintenance.columns:
        metrics["total_cost"] = float(df_maintenance["cost"].sum())
        metrics["avg_cost"] = float(df_maintenance["cost"].mean()) if len(df_maintenance) > 0 else 0.0

    return metrics


def apply_dark_theme(fig, ax):
    """Applies high-contrast dark styling matching CampusFix aesthetic."""
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=MUTED_TEXT, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#233554")
    ax.grid(color=GRID_COLOR, linestyle="--", linewidth=0.6, alpha=0.7)


# ----------------------------------------------------
# 5 Core Charts (Embedded in Tkinter GUI)
# ----------------------------------------------------

def generate_category_bar_chart(df_complaints):
    """Chart 1: Complaints by Category (Horizontal Bar Chart)"""
    fig = Figure(figsize=(5.5, 3.2), dpi=100)
    ax = fig.add_subplot(111)
    apply_dark_theme(fig, ax)

    if df_complaints.empty or "category" not in df_complaints.columns:
        ax.text(0.5, 0.5, "No Data Available", color=MUTED_TEXT, ha="center", va="center")
        return fig

    cat_counts = df_complaints["category"].value_counts().sort_values(ascending=True)
    palette = ["#38BDF8", "#F59E0B", "#10B981", "#EF4444", "#3B82F6", "#A855F7", "#FBBF24", "#64748B"]
    colors = [palette[i % len(palette)] for i in range(len(cat_counts))]

    bars = ax.barh(cat_counts.index, cat_counts.values, color=colors, height=0.6)
    ax.set_title("COMPLAINTS BY CATEGORY", fontsize=11, fontweight="bold", color=TEXT_COLOR, pad=12, loc="left")
    ax.set_xlabel("Number of Complaints", color=MUTED_TEXT, fontsize=9)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{int(w)}",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(4, 0), textcoords="offset points",
                    ha="left", va="center", color=TEXT_COLOR, fontsize=8, fontweight="bold")

    fig.tight_layout()
    return fig


def generate_status_pie_chart(df_complaints):
    """Chart 2: Status Distribution (Pie Chart)"""
    fig = Figure(figsize=(4.8, 3.2), dpi=100)
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)

    if df_complaints.empty or "status" not in df_complaints.columns:
        ax.text(0.5, 0.5, "No Data Available", color=MUTED_TEXT, ha="center", va="center")
        return fig

    status_counts = df_complaints["status"].value_counts()
    colors_map = {
        "Pending": "#EF4444",      # Red / Coral
        "In Progress": "#38BDF8",  # Sky Blue
        "Resolved": "#10B981"      # Emerald Green
    }
    colors = [colors_map.get(k, "#64748B") for k in status_counts.index]

    wedges, texts, autotexts = ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops={"color": TEXT_COLOR, "fontsize": 9, "fontweight": "bold"},
        wedgeprops={"edgecolor": CARD_BG, "linewidth": 2}
    )
    for at in autotexts:
        at.set_color("#FFFFFF")
        at.set_fontsize(8)

    ax.set_title("STATUS DISTRIBUTION", fontsize=11, fontweight="bold", color=TEXT_COLOR, pad=12, loc="left")
    fig.tight_layout()
    return fig


def generate_building_bar_chart(df_complaints):
    """Chart 3: Complaints by Building (Amber Vertical Bar Chart)"""
    fig = Figure(figsize=(5.5, 3.2), dpi=100)
    ax = fig.add_subplot(111)
    apply_dark_theme(fig, ax)

    if df_complaints.empty or "building" not in df_complaints.columns:
        ax.text(0.5, 0.5, "No Data Available", color=MUTED_TEXT, ha="center", va="center")
        return fig

    building_counts = df_complaints["building"].value_counts()
    bars = ax.bar(building_counts.index, building_counts.values, color=AMBER_ACCENT, width=0.55, edgecolor="#B45309", linewidth=0.5)
    ax.set_title("COMPLAINTS BY BUILDING", fontsize=11, fontweight="bold", color=TEXT_COLOR, pad=12, loc="left")
    ax.set_ylabel("Count", color=MUTED_TEXT, fontsize=9)
    ax.tick_params(axis="x", rotation=20, labelsize=8)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{int(h)}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", color=TEXT_COLOR, fontsize=8, fontweight="bold")

    fig.tight_layout()
    return fig


def generate_monthly_trend_chart(df_complaints):
    """Chart 4: Complaints Reported Per Month (Cyan Line Chart)"""
    fig = Figure(figsize=(5.5, 3.2), dpi=100)
    ax = fig.add_subplot(111)
    apply_dark_theme(fig, ax)

    if df_complaints.empty or "date" not in df_complaints.columns:
        ax.text(0.5, 0.5, "No Data Available", color=MUTED_TEXT, ha="center", va="center")
        return fig

    # Extract Year-Month
    df_temp = df_complaints.copy()
    df_temp["month"] = pd.to_datetime(df_temp["date"], errors="coerce").dt.strftime("%Y-%m")
    month_counts = df_temp["month"].value_counts().sort_index()

    ax.plot(month_counts.index, month_counts.values, color=CYAN_ACCENT, marker="o", markersize=6,
            linewidth=2.5, markerfacecolor="#0284C7", markeredgecolor="#BAE6FD")
    ax.set_title("COMPLAINTS REPORTED PER MONTH", fontsize=11, fontweight="bold", color=TEXT_COLOR, pad=12, loc="left")
    ax.set_ylabel("Tickets Reported", color=MUTED_TEXT, fontsize=9)
    ax.tick_params(axis="x", rotation=25, labelsize=8)

    for x, y in zip(month_counts.index, month_counts.values):
        ax.annotate(f"{y}", xy=(x, y), xytext=(0, 5), textcoords="offset points",
                    ha="center", color=TEXT_COLOR, fontsize=8, fontweight="bold")

    fig.tight_layout()
    return fig


def generate_repair_cost_chart(df_complaints, df_maintenance):
    """Chart 5: Repair Cost by Category (Emerald Green Bar Chart)"""
    fig = Figure(figsize=(10.8, 3.2), dpi=100)
    ax = fig.add_subplot(111)
    apply_dark_theme(fig, ax)

    if df_complaints.empty or df_maintenance.empty:
        ax.text(0.5, 0.5, "No Repair Cost Data Available", color=MUTED_TEXT, ha="center", va="center")
        return fig

    merged = pd.merge(df_maintenance, df_complaints[["complaint_id", "category"]], on="complaint_id", how="left")
    category_cost = merged.groupby("category")["cost"].sum().sort_values(ascending=False)

    bars = ax.bar(category_cost.index, category_cost.values, color=GREEN_ACCENT, width=0.5, edgecolor="#047857")
    ax.set_title("REPAIR COST BY CATEGORY", fontsize=11, fontweight="bold", color=TEXT_COLOR, pad=12, loc="left")
    ax.set_ylabel("Total Cost (₹)", color=MUTED_TEXT, fontsize=9)
    ax.tick_params(axis="x", rotation=15, labelsize=8)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"₹{int(h):,}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", color=TEXT_COLOR, fontsize=8, fontweight="bold")

    fig.tight_layout()
    return fig


def export_to_csv(db_path=DB_PATH, output_file=None):
    """
    Exports merged complaints and maintenance details to CSV using Pandas.
    Saves to reports/complaints_report.csv.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    if not output_file:
        output_file = os.path.join(REPORTS_DIR, "complaints_report.csv")

    df_complaints, df_maintenance = load_data(db_path)

    if df_complaints.empty:
        return False, "No complaint records found to export."

    # Perform left join with maintenance details
    if not df_maintenance.empty:
        merged_df = pd.merge(
            df_complaints,
            df_maintenance[["complaint_id", "staff_name", "repair_date", "cost", "remarks"]],
            on="complaint_id",
            how="left"
        )
    else:
        merged_df = df_complaints.copy()
        merged_df["staff_name"] = ""
        merged_df["repair_date"] = ""
        merged_df["cost"] = 0.0
        merged_df["remarks"] = ""

    merged_df.to_csv(output_file, index=False)
    return True, output_file


if __name__ == "__main__":
    m = calculate_metrics()
    print("Metrics calculated:", m)
    status, path = export_to_csv()
    print("CSV Export status:", status, "Path:", path)
