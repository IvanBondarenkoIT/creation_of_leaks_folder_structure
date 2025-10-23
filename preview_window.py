"""
Preview Window Module
Provides a preview interface for batch file processing with edit capabilities
"""

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import List, Callable, Optional


@dataclass
class FilePreviewData:
    """Data class for file preview information"""
    file_path: str
    file_name: str
    category: str  # Combo/Database/Logs/Mixed
    date: str
    domain: str
    topic: str
    link: str
    password: str
    destination_path: str
    analysis_info: str = None  # Optional: info about auto-analysis
    
    def get_destination_summary(self) -> str:
        """Get short summary of destination"""
        parts = self.destination_path.split('\\')
        if len(parts) >= 3:
            return f"...\\{parts[-3]}\\{parts[-2]}\\{parts[-1]}"
        return self.destination_path


class FilePreviewItem(tk.Frame):
    """Single file preview item in the list"""
    
    def __init__(self, parent, data: FilePreviewData, categories: List[str], on_change: Optional[Callable] = None):
        super().__init__(parent, relief=tk.RIDGE, borderwidth=1)
        self.data = data
        self.categories = categories
        self.on_change = on_change
        
        # Variables for editable fields
        self.category_var = tk.StringVar(value=data.category)
        self.domain_var = tk.StringVar(value=data.domain)
        self.date_var = tk.StringVar(value=data.date)
        
        # Trace changes
        self.category_var.trace_add("write", self._on_data_changed)
        self.domain_var.trace_add("write", self._on_data_changed)
        self.date_var.trace_add("write", self._on_data_changed)
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create widgets for preview item"""
        # File name (read-only)
        file_frame = tk.Frame(self)
        file_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(file_frame, text="[F]", font=('Arial', 10, 'bold'), fg='#3498db').pack(side=tk.LEFT, padx=2)
        tk.Label(file_frame, text=self.data.file_name, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Show analysis info if available
        if hasattr(self.data, 'analysis_info') and self.data.analysis_info:
            tk.Label(file_frame, text=f"[AI: {self.data.analysis_info}]", 
                    font=('Arial', 8), fg='#27ae60').pack(side=tk.LEFT, padx=5)
        
        # Editable fields frame
        edit_frame = tk.Frame(self)
        edit_frame.pack(fill=tk.X, padx=10, pady=2)
        
        # Category combobox
        tk.Label(edit_frame, text="Type:", width=10, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, padx=2)
        category_combo = ttk.Combobox(edit_frame, textvariable=self.category_var, 
                                      values=self.categories, state="readonly", width=12)
        category_combo.grid(row=0, column=1, sticky=tk.W, padx=2)
        
        # Date entry
        tk.Label(edit_frame, text="Date:", width=10, anchor=tk.W).grid(row=0, column=2, sticky=tk.W, padx=2)
        date_entry = tk.Entry(edit_frame, textvariable=self.date_var, width=12)
        date_entry.grid(row=0, column=3, sticky=tk.W, padx=2)
        
        # Domain entry
        tk.Label(edit_frame, text="Domain/Name:", width=10, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, padx=2)
        domain_entry = tk.Entry(edit_frame, textvariable=self.domain_var, width=30)
        domain_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W+tk.E, padx=2)
        
        # Destination path (read-only, updates on change)
        self.dest_label = tk.Label(edit_frame, text=f"→ {self.data.get_destination_summary()}", 
                                   font=('Arial', 9), fg='blue', anchor=tk.W)
        self.dest_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, padx=2, pady=2)
        
    def _on_data_changed(self, *args):
        """Called when any editable field changes"""
        # Update data object
        self.data.category = self.category_var.get()
        self.data.domain = self.domain_var.get()
        self.data.date = self.date_var.get()
        
        # Notify parent about change
        if self.on_change:
            self.on_change(self.data)
    
    def get_data(self) -> FilePreviewData:
        """Get current data with all edits"""
        return self.data


class PreviewWindow:
    """Modal window for previewing and editing batch file processing"""
    
    def __init__(self, parent, preview_data: List[FilePreviewData], 
                 categories: List[str], on_confirm: Callable[[List[FilePreviewData]], None],
                 path_calculator: Callable[[FilePreviewData], str]):
        """
        Initialize preview window
        
        Args:
            parent: Parent tkinter window
            preview_data: List of FilePreviewData objects
            categories: List of available categories
            on_confirm: Callback function when user confirms
            path_calculator: Function to recalculate destination path
        """
        self.parent = parent
        self.preview_data = preview_data
        self.categories = categories
        self.on_confirm = on_confirm
        self.path_calculator = path_calculator
        self.confirmed = False
        
        # Create modal window
        self.window = tk.Toplevel(parent)
        self.window.title("Chain Submit Preview - Review and Edit")
        self.window.geometry("700x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Ensure window is visible
        self.window.lift()
        self.window.focus_force()
        
        # Store preview items
        self.preview_items: List[FilePreviewItem] = []
        
        self._create_widgets()
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
        
        # Force window to be visible
        self.window.deiconify()
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))
        
    def _create_widgets(self):
        """Create all widgets for preview window"""
        # Header
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"📋 Preview: {len(self.preview_data)} files to process",
                font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
        
        # Info label
        info_frame = tk.Frame(self.window, bg='#ecf0f1')
        info_frame.pack(fill=tk.X, pady=5)
        tk.Label(info_frame, text="Review and edit file destinations before processing. You can change Type, Date, and Domain/Name.",
                font=('Arial', 9), bg='#ecf0f1', fg='#34495e').pack(pady=5, padx=10)
        
        # Scrollable frame for file list
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create preview items
        for data in self.preview_data:
            item = FilePreviewItem(scrollable_frame, data, self.categories, 
                                  on_change=self._on_item_changed)
            item.pack(fill=tk.X, pady=3, padx=5)
            self.preview_items.append(item)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom buttons frame
        button_frame = tk.Frame(self.window, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, pady=10)
        
        # Statistics
        stats_text = f"Total files: {len(self.preview_data)}"
        tk.Label(button_frame, text=stats_text, font=('Arial', 10), 
                bg='#ecf0f1').pack(side=tk.LEFT, padx=20)
        
        # Buttons
        tk.Button(button_frame, text="❌ Cancel", command=self._on_cancel,
                 font=('Arial', 11), bg='#e74c3c', fg='white', 
                 padx=20, pady=5).pack(side=tk.RIGHT, padx=10)
        
        tk.Button(button_frame, text="✅ Process All Files", command=self._on_process,
                 font=('Arial', 11, 'bold'), bg='#27ae60', fg='white',
                 padx=20, pady=5).pack(side=tk.RIGHT, padx=10)
        
        # Bind escape key
        self.window.bind('<Escape>', lambda e: self._on_cancel())
        
    def _on_item_changed(self, data: FilePreviewData):
        """Called when any item's data changes"""
        # Recalculate destination path
        new_path = self.path_calculator(data)
        data.destination_path = new_path
        
        # Update all items to refresh display
        for item in self.preview_items:
            if item.data == data:
                item.dest_label.config(text=f"→ {data.get_destination_summary()}")
                break
    
    def _on_process(self):
        """Handle process button click"""
        # Collect all data
        final_data = [item.get_data() for item in self.preview_items]
        
        # Confirm with user
        result = messagebox.askyesno(
            "Confirm Processing",
            f"Process {len(final_data)} files?\n\nThis will move files to their destinations.",
            parent=self.window
        )
        
        if result:
            self.confirmed = True
            self.preview_data = final_data
            self.window.destroy()
            self.on_confirm(final_data)
    
    def _on_cancel(self):
        """Handle cancel button click"""
        result = messagebox.askyesno(
            "Cancel Processing",
            "Cancel batch processing?\n\nNo files will be moved.",
            parent=self.window
        )
        
        if result:
            self.confirmed = False
            self.window.destroy()
    
    def wait_window(self):
        """Wait for window to close"""
        self.window.wait_window()


# Test code
if __name__ == "__main__":
    def test_preview():
        root = tk.Tk()
        root.withdraw()
        
        # Test data
        test_data = [
            FilePreviewData(
                file_path="C:/test/file1.txt",
                file_name="file1.txt",
                category="Combo",
                date="2024-01-15",
                domain="example.com",
                topic="Test Topic",
                link="https://t.me/test/123",
                password="",
                destination_path="E:/WORK/db/Combo/2024-01-15/example.com"
            ),
            FilePreviewData(
                file_path="C:/test/file2.sql",
                file_name="file2.sql",
                category="Database",
                date="2024-01-15",
                domain="database_name",
                topic="DB Topic",
                link="https://t.me/test/124",
                password="pass123",
                destination_path="E:/WORK/db/Database/2024-01-15/database_name"
            ),
        ]
        
        def on_confirm(data):
            print("Confirmed processing:")
            for item in data:
                print(f"  - {item.file_name} -> {item.category} / {item.date}")
        
        def calc_path(data):
            return f"E:/WORK/db/{data.category}/{data.date}/{data.domain}"
        
        window = PreviewWindow(root, test_data, ["Combo", "Database", "Logs", "Mixed"], 
                              on_confirm, calc_path)
        window.wait_window()
        
        root.destroy()
    
    test_preview()

