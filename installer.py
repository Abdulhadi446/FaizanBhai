import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk
import win32com.client

def move_file(source_path, destination_folder, name):
    """
    Moves a file from source_path to destination_folder with the given name.
    """
    os.makedirs(destination_folder, exist_ok=True)
    destination_path = os.path.join(destination_folder, name)
    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        print(f"Error moving {name}: {e}")
    return destination_path

def create_shortcut(target, shortcut_path, icon=None):
    """
    Creates a Windows shortcut at shortcut_path that points to the target.
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = icon if icon else target
        shortcut.save()
    except Exception as e:
        print(f"Error creating shortcut: {e}")

def run_tasks(update_progress, status_update, set_progress_max, on_complete):
    """
    Executes the tasks, updates the progress bar after each step,
    and calls the on_complete callback when finished.
    """
    total_steps = 3
    set_progress_max(total_steps)
    step = 0
    home_dir = os.path.expanduser("~")
    app_folder = os.path.join(home_dir, "MyAppFolder")

    # Step 1: Move app.exe
    status_update("Moving app.exe...")
    app_exe = move_file('app.exe', app_folder, 'app.exe')
    step += 1
    update_progress(step)

    # Step 2: Move main.exe
    status_update("Moving main.exe...")
    move_file('main.exe', app_folder, 'main.exe')
    step += 1
    update_progress(step)

    # Step 3: Create desktop shortcut for app.exe
    status_update("Creating shortcut...")
    desktop = os.path.join(home_dir, "Desktop")
    shortcut_path = os.path.join(desktop, "MyProgram.lnk")
    create_shortcut(app_exe, shortcut_path)
    step += 1
    update_progress(step)

    status_update("All tasks completed.")
    on_complete()

def main():
    # Set up the main Tkinter window.
    root = tk.Tk()
    root.title("My App Installer")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Status label to display the current operation.
    status_label = tk.Label(frame, text="Ready")
    status_label.pack(pady=5)

    # Progress bar as a loading bar.
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=5)

    # Thread-safe helper functions.
    def update_progress(value):
        root.after(0, lambda: progress_bar.configure(value=value))

    def set_progress_max(max_value):
        root.after(0, lambda: progress_bar.configure(maximum=max_value))

    def status_update(message):
        root.after(0, lambda: status_label.config(text=message))

    def close_app():
        # Wait briefly to allow the user to see the final status before closing.
        root.after(1000, root.destroy)

    # Start tasks in a background thread to keep the GUI responsive.
    def start_tasks():
        start_button.config(state=tk.DISABLED)
        threading.Thread(target=run_tasks, args=(update_progress, status_update, set_progress_max, close_app)).start()

    start_button = tk.Button(root, text="Start Installation", command=start_tasks)
    start_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()