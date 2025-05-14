import tkinter as tk
from variables import VariableManager, open_variable_editor_in_main_window
from tco import open_tco_page
from exporter import export_json, import_json

root = tk.Tk()
root.title("Main Application")
root.geometry("1600x1200")

var_manager = VariableManager()

def display_content(content_type):
    for widget in content_frame.winfo_children():
        widget.destroy()

    if content_type == "homepage":
        label = tk.Label(content_frame, text="This is the Homepage")
        label.pack(pady=20)
    elif content_type == "variable_editor":
        open_variable_editor_in_main_window(content_frame, var_manager)
    elif content_type == "tco":
        open_tco_page(content_frame, var_manager)
    elif content_type == "import from .json":
        # Try catch import_json() to handle errors
        try:
            import_json("src/results", "tco_results.json")
            label = tk.Label(content_frame, text="Importing from JSON...")
            label.pack(pady=20)
            # Add a fake progress bar
            progress = tk.Label(content_frame, text="Progress: 0%")
            progress.pack(pady=20)
            for i in range(1, 101):
                progress.config(text=f"Progress: {i}%")
                root.update_idletasks()
                root.after(50)
            label.config(text="Import complete!")
            label.pack(pady=20)
        except Exception as e:
            label = tk.Label(content_frame, text=f"An error occurred: {e}")
            label.pack(pady=20)
            return
        back_button = tk.Button(content_frame, text="Back to Homepage", command=lambda: display_content("homepage"))
        back_button.pack(pady=20)
        
    elif content_type == "export to .json":
        # Try catch export_json() to handle errors
        try:
            export_json("src/results", "tco_results.json")
            # Show a message that the export is in progress
            label = tk.Label(content_frame, text="Exporting to JSON...")
            label.pack(pady=20)
            progress = tk.Label(content_frame, text="Progress: 0%")
            progress.pack(pady=20)
            for i in range(1, 101):
                progress.config(text=f"Progress: {i}%")
                root.update_idletasks()
                root.after(50)
            label.config(text="Export complete!")
            label.pack(pady=20)
        except Exception as e:
            label = tk.Label(content_frame, text=f"Error: {e}")
            label.pack(pady=20)
            return
        back_button = tk.Button(content_frame, text="Back to Homepage", command=lambda: display_content("homepage"))
        back_button.pack(pady=20)

    elif content_type == "exit":
        root.quit()


menu_frame = tk.Frame(root, width=100, height=300)
menu_frame.pack(side="left", fill="y", padx=(10, 0))

creator_label = tk.Label(root, text="This program was made by Erik Råberg & Carl Lavö")
creator_label.pack(pady=5)

content_frame = tk.Frame(root)
content_frame.pack(side="left", expand=True, fill="both")

display_content("homepage")

menu_button1 = tk.Button(menu_frame, text="Homepage", command=lambda: display_content("homepage"))
menu_button1.pack(fill="x", pady=5)

menu_button2 = tk.Button(menu_frame, text="Variables", command=lambda: display_content("variable_editor"))
menu_button2.pack(fill="x", pady=5)

menu_button3 = tk.Button(menu_frame, text="TCO", command=lambda: display_content("tco"))
menu_button3.pack(fill="x", pady=5)

menu_button4 = tk.Button(menu_frame, text="Import from .json", command=lambda: display_content("import from .json"))
menu_button4.pack(fill="x", pady=5)

menu_button5 = tk.Button(menu_frame, text="Export to .json", command=lambda: display_content("export to .json"))
menu_button5.pack(fill="x", pady=5)

menu_button6 = tk.Button(menu_frame, text="Exit", command=lambda: display_content("exit"))
menu_button6.pack(fill="x", pady=5)

root.mainloop()
