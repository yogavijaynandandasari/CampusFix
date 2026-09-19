"""
streamlit_app.py - Streamlit Cloud Entry Point for CampusFix.
Ensures seamless deployment whether Streamlit targets app.py or streamlit_app.py.
"""
import os
import runpy

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    runpy.run_path(app_path, run_name="__main__")
