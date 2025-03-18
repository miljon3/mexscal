import tkinter as tk
from tkinter import font
from variables import VariableManager, open_variable_editor_in_main_window

# ChatGPT used to add style and layout to the application

# Initialize main application window
root = tk.Tk()
root.title("Main Application")
root.geometry("1200x800")

# Set modern font and colors
root.config(bg="#f7f7f7")
modern_font = font.nametofont("TkDefaultFont")
modern_font.actual()  # Retrieve font properties for more control

var_manager = VariableManager()

# Function to display content in the main area
def display_content(content_type):
    # Clear existing widgets in the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    if content_type == "homepage":
        label = tk.Label(content_frame, text="This is the Homepage", font=(modern_font, 14), bg="#f7f7f7")
        label.pack(pady=20)
    elif content_type == "variable_editor":
        open_variable_editor_in_main_window(content_frame, var_manager)  # Show in main window
    elif content_type == "tco":
        label = tk.Label(content_frame, text="Total Cost of Ownership (TCO) Analysis", font=(modern_font, 14), bg="#f7f7f7")
        label.pack(pady=20)

# Set modern font and layout
modern_font = font.nametofont("TkDefaultFont")
modern_font.actual()

# Create a frame for the left-side menu (green background)
menu_frame = tk.Frame(root, width=100, bg="#4CAF50", height=300)
menu_frame.pack(side="left", fill="y", padx=(10, 0))

# Create introductory labels
welcome_label = tk.Label(root, text="Welcome", font=(modern_font, 16), bg="#f7f7f7")
welcome_label.pack(pady=(20, 5))

creator_label = tk.Label(root, text="Placeholder", font=(modern_font, 12), bg="#f7f7f7")
creator_label.pack(pady=5)

date_label = tk.Label(root, text="Placeholder", font=(modern_font, 12), bg="#f7f7f7")
date_label.pack(pady=(5, 20))

# Define the button style for hover effect
button_style = {
    'fg': "#ffffff",  # White text
    'bg': "#4CAF50",  # Green background
    'font': (modern_font, 12),
    'relief': "flat",  # Flat button for modern look
    'bd': 0,  # No border
    'highlightthickness': 0,
    'padx': 20,
    'pady': 10,
}

# Button hover effect
def on_enter(event):
    event.widget.config(bg="#45a049")  # Slightly darker green on hover

def on_leave(event):
    event.widget.config(bg="#4CAF50")  # Original green on leave

# Main content frame
content_frame = tk.Frame(root, bg="#f7f7f7")
content_frame.pack(side="left", expand=True, fill="both")

# Initialize content to be displayed
display_content("homepage")  # Default content is the homepage

# Create menu items in the left-side menu frame
menu_button1 = tk.Button(menu_frame, text="Homepage", command=lambda: display_content("homepage"), **button_style)
menu_button1.pack(fill="x", pady=5)
menu_button1.bind("<Enter>", on_enter)
menu_button1.bind("<Leave>", on_leave)

menu_button2 = tk.Button(menu_frame, text="Open Variable Editor", command=lambda: display_content("variable_editor"), **button_style)
menu_button2.pack(fill="x", pady=5)
menu_button2.bind("<Enter>", on_enter)
menu_button2.bind("<Leave>", on_leave)

menu_button3 = tk.Button(menu_frame, text="TCO", command=lambda: display_content("tco"), **button_style)
menu_button3.pack(fill="x", pady=5)
menu_button3.bind("<Enter>", on_enter)
menu_button3.bind("<Leave>", on_leave)

root.mainloop()
