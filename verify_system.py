"""
verify_system.py - Headless Verification Script for Campus Maintenance System
Verifies database initialization, CRUD operations, Pandas analytics, and Matplotlib chart figures.
"""

import os
import sys

# Ensure current directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set stdout encoding to utf-8 for Windows console support
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import database as db
import analysis


def test_database():
    print("Testing Database initialization...")
    db.init_db()

    complaints = db.get_all_complaints()
    maintenance = db.get_all_maintenance_records()
    print(f"[PASS] Complaints in DB: {len(complaints)}")
    print(f"[PASS] Maintenance records in DB: {len(maintenance)}")
    assert len(complaints) >= 48, f"Expected at least 48 complaints, got {len(complaints)}"
    assert len(maintenance) >= 20, f"Expected at least 20 maintenance records, got {len(maintenance)}"

    # Test adding a complaint
    new_id = db.add_complaint(
        student_name="Test Student",
        department="BCA",
        building="Block A",
        room_no="105",
        category="Electrical",
        problem="Test issue verification",
        priority="High",
        status="Pending"
    )
    print(f"[PASS] Added test complaint with ID: {new_id}")

    # Test search
    fetched = db.get_complaint_by_id(new_id)
    assert fetched is not None
    assert fetched["student_name"] == "Test Student"
    print(f"[PASS] Fetched complaint: {fetched['complaint_id']} - {fetched['student_name']}")

    # Test update status
    db.update_complaint_status(new_id, "In Progress")
    updated = db.get_complaint_by_id(new_id)
    assert updated["status"] == "In Progress"
    print(f"[PASS] Updated status to: {updated['status']}")

    # Test add maintenance
    db.add_maintenance_record(new_id, "Test Tech", "2026-09-18", 350.0, "Test fix completed")
    m_list = db.get_maintenance_for_complaint(new_id)
    assert len(m_list) >= 1
    print(f"[PASS] Added maintenance record: Cost ₹{m_list[0]['cost']}, Remarks: {m_list[0]['remarks']}")


def test_analysis():
    print("\nTesting Analysis & Metrics calculations...")
    metrics = analysis.calculate_metrics()
    print(f"[PASS] Metrics calculated:")
    for k, v in metrics.items():
        print(f"    - {k}: {v}")

    assert metrics["total_complaints"] >= 48
    assert metrics["total_cost"] > 0
    assert metrics["avg_cost"] > 0

    print("\nTesting Matplotlib charts generation...")
    df_c, df_m = analysis.load_data()
    fig1 = analysis.generate_category_bar_chart(df_c)
    fig2 = analysis.generate_status_pie_chart(df_c)
    fig3 = analysis.generate_building_bar_chart(df_c)
    fig4 = analysis.generate_monthly_trend_chart(df_c)
    fig5 = analysis.generate_repair_cost_chart(df_c, df_m)
    print("[PASS] All 5 Matplotlib figures created successfully without errors.")

    print("\nTesting CSV Export...")
    success, filepath = analysis.export_to_csv()
    assert success is True
    assert os.path.exists(filepath)
    print(f"[PASS] CSV Report exported successfully to: {filepath} ({os.path.getsize(filepath)} bytes)")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING CAMPUS MAINTENANCE SYSTEM VERIFICATION")
    print("=" * 60)
    test_database()
    test_analysis()
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! SYSTEM READY.")
    print("=" * 60)
