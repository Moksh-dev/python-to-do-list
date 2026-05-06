import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

FILE_NAME = "tasks.json"

tasks = []

# ------------------ FILE HANDLING ------------------
def load_tasks():
    global tasks
    try:
        with open(FILE_NAME, "r") as file:
            tasks = json.load(file)
    except:
        tasks = []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ------------------ UI UPDATE ------------------
def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["done"] else "✘"
        text = f"{status} [{task['priority']}] {task['title']} ({task['time']})"
        listbox.insert(tk.END, text)

# ------------------ FUNCTIONS ------------------
def add_task():
    title = entry.get()
    priority = priority_var.get()

    if title == "":
        messagebox.showwarning("Warning", "Enter a task")
        return

    task = {
        "title": title,
        "priority": priority,
        "time": datetime.now().strftime("%d-%m %H:%M"),
        "done": False
    }

    tasks.append(task)
    save_tasks()
    update_listbox()
    entry.delete(0, tk.END)

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        save_tasks()
        update_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task")

def mark_done():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks()
        update_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task")

def clear_all():
    global tasks
    if messagebox.askyesno("Confirm", "Delete all tasks?"):
        tasks = []
        save_tasks()
        update_listbox()

# ------------------ UI ------------------
root = tk.Tk()
root.title("Advanced To-Do List")
root.geometry("450x500")
root.configure(bg="#121212")

frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    frame,
    width=55,
    height=15,
    yscrollcommand=scrollbar.set,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#333"
)
listbox.pack()

scrollbar.config(command=listbox.yview)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Priority Dropdown
priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.pack(pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task, width=20).pack(pady=5)
tk.Button(root, text="Mark Done ✔", command=mark_done, width=20).pack(pady=5)
tk.Button(root, text="Delete Task", command=delete_task, width=20).pack(pady=5)
tk.Button(root, text="Clear All", command=clear_all, width=20).pack(pady=5)

# Load existing tasks
load_tasks()
update_listbox()

root.mainloop()
