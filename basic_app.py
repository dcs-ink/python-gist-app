import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

TOKEN_FILENAME = ".github_token"
GITHUB_TOKEN = None
GITHUB_API_URL = 'https://api.github.com/gists'

# --- Read GitHub Token from file ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, TOKEN_FILENAME)

    with open(token_path, 'r') as f:
        GITHUB_TOKEN = f.readline().strip()

    if not GITHUB_TOKEN:
        messagebox.showerror("Token Error", f"Token file not found. Will not save")

except FileNotFoundError:
    messagebox.showerror("Token Error", f"Token file not found. Will not save")
except Exception as e:
    messagebox.showerror("Token Error", f"Error reading token file:\n{e}")

def create_gist():
    if GITHUB_TOKEN == "YOUR_TOKEN_HERE":
        messagebox.showerror("Error", "Please set your GitHub Token in the code.")
        return

    filename = filename_entry.get()
    content = content_text.get("1.0", tk.END).strip()

    if not filename or not content:
        messagebox.showwarning("Error", "Filename and content cannot be empty.")
        return
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "public": False, # Set to True for public gists, False for secret
        "files": {
            filename: {
                "content": content
            }
        }
    }

    try:
        response = requests.post(GITHUB_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        gist_url = response.json().get("html_url")
        messagebox.showinfo("Success", f"Gist created successfully!\nURL: {gist_url}")
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to create Gist:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

# --- Use Tab Key to Navigate Widgets ---
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def focus_prev_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

# --- Setup The App Window ---
window = tk.Tk()
window.title("dcs_gist_creator")

window_width = 600
window_height = 500

# Center the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")


tk.Label(window, text="Filename:").pack(pady=(10,0))
filename_entry = tk.Entry(window, width=50)
filename_entry.pack()

tk.Label(window, text="Content:").pack(pady=(10,0))
content_text = tk.Text(window, height=20, width=80)
content_text.pack()

# --- Use Tab Key to Navigate Widgets ---
content_text.bind("<Tab>", focus_next_widget)
content_text.bind("<Shift-Tab>", focus_prev_widget)


create_button = tk.Button(window, text="Create Gist", command=create_gist)
create_button.pack(pady=20)

window.mainloop()