import tkinter as tk
from variables import VariableManager, open_variable_editor_in_main_window
from tco import open_tco_page
from results import open_stats_page

root = tk.Tk()
root.title("Main Application")
root.geometry("1400x1000")

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
    elif content_type == "stats":
        open_stats_page(content_frame, var_manager)

menu_frame = tk.Frame(root, width=100, height=300)
menu_frame.pack(side="left", fill="y", padx=(10, 0))

welcome_label = tk.Label(root, text="Welcome")
welcome_label.pack(pady=(20, 5))

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

menu_button4 = tk.Button(menu_frame, text="Show Stats", command=lambda: display_content("stats"))
menu_button4.pack(fill="x", pady=5)

menu_button5 = tk.Button(menu_frame, text="Exit", command=root.quit)
menu_button5.pack(fill="x", pady=5)

root.mainloop()
