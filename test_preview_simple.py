#!/usr/bin/env python3
"""
Simple test for PreviewWindow to debug display issues
"""

import tkinter as tk
from preview_window import PreviewWindow, FilePreviewData

def test_preview():
    """Test preview window with minimal data"""
    root = tk.Tk()
    root.title("Test Main Window")
    root.geometry("400x300")
    
    # Test data
    test_data = [
        FilePreviewData(
            file_path="C:/test/teamlease.com (india).txt",
            file_name="teamlease.com (india).txt",
            category="Database",
            date="2024-10-16",
            domain="teamlease.com",
            topic="Test Topic",
            link="https://t.me/test/123",
            password="",
            destination_path="E:/WORK/db/Database/2024-10-16/teamlease.com",
            analysis_info="Auto: Database with domain 'teamlease.com' (conf: high)"
        ),
        FilePreviewData(
            file_path="C:/test/VALID_MEGA_COMBO.txt",
            file_name="VALID_MEGA_COMBO.txt",
            category="Combo",
            date="2024-10-16",
            domain="VALID_MEGA_COMBO",
            topic="Test Topic",
            link="https://t.me/test/124",
            password="",
            destination_path="E:/WORK/db/Combo/2024-10-16/VALID_MEGA_COMBO",
            analysis_info="Auto: Multiple combo indicators (3)"
        ),
    ]
    
    def on_confirm(data):
        print("Confirmed processing:")
        for item in data:
            print(f"  - {item.file_name} -> {item.category} / {item.date}")
        root.quit()
    
    def calc_path(data):
        return f"E:/WORK/db/{data.category}/{data.date}/{data.domain}"
    
    def show_preview():
        print("Creating preview window...")
        try:
            window = PreviewWindow(root, test_data, ["Combo", "Database", "Logs", "Mixed"], 
                                  on_confirm, calc_path)
            print("Preview window created, waiting...")
            window.wait_window()
            print("Preview window closed")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Button to show preview
    btn = tk.Button(root, text="Show Preview", command=show_preview, font=('Arial', 14))
    btn.pack(pady=50)
    
    # Instructions
    label = tk.Label(root, text="Click 'Show Preview' to test the preview window", 
                    font=('Arial', 12))
    label.pack(pady=20)
    
    print("Test window created. Click 'Show Preview' button.")
    root.mainloop()

if __name__ == "__main__":
    test_preview()

