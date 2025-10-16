"""
Test script for PreviewWindow
Run this to test the preview window functionality independently
"""

import tkinter as tk
from preview_window import PreviewWindow, FilePreviewData


def test_preview_window():
    """Test the preview window with sample data"""
    root = tk.Tk()
    root.withdraw()
    
    # Create test data
    test_data = [
        FilePreviewData(
            file_path="C:/test/combo_file1.txt",
            file_name="combo_file1.txt",
            category="Combo",
            date="2024-01-15",
            domain="combo_file1",
            topic="Test Channel",
            link="https://t.me/testchannel/123",
            password="",
            destination_path="E:/_WORK/db/Combo/2024-01-15/combo_file1"
        ),
        FilePreviewData(
            file_path="C:/test/database.sql",
            file_name="database.sql",
            category="Database",
            date="2024-01-16",
            domain="testdatabase",
            topic="DB Topic",
            link="https://t.me/testchannel/124",
            password="pass123",
            destination_path="E:/_WORK/db/Database/2024-01-16/testdatabase"
        ),
        FilePreviewData(
            file_path="C:/test/logs_archive.zip",
            file_name="logs_archive.zip",
            category="Logs",
            date="2024-01-17",
            domain="logs_archive",
            topic="Logs Topic",
            link="https://t.me/testchannel/125",
            password="",
            destination_path="E:/_WORK/db/Logs/2024-01-17/logs_archive"
        ),
    ]
    
    def on_confirm(data):
        """Callback when user confirms"""
        print("\n" + "="*60)
        print("CONFIRMED PROCESSING:")
        print("="*60)
        for item in data:
            print(f"\nFile: {item.file_name}")
            print(f"  Category: {item.category}")
            print(f"  Date: {item.date}")
            print(f"  Domain: {item.domain}")
            print(f"  Destination: {item.destination_path}")
        print("\n" + "="*60)
    
    def calc_path(data):
        """Recalculate path function"""
        return f"E:/_WORK/db/{data.category}/{data.date}/{data.domain}"
    
    # Create and show preview window
    categories = ["Combo", "Database", "Logs", "Mixed"]
    window = PreviewWindow(root, test_data, categories, on_confirm, calc_path)
    window.wait_window()
    
    root.destroy()
    print("Test completed!")


if __name__ == "__main__":
    print("Starting PreviewWindow test...")
    print("This will open a preview window with sample data.")
    print("Try editing the fields and clicking 'Process All Files'")
    print("-" * 60)
    test_preview_window()

