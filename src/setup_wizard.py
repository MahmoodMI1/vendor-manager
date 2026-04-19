import tkinter as tk
from tkinter import filedialog, messagebox
from config_manager import save_config


def run_setup():
    root = tk.Tk()
    root.title("Vendor Reminder — Setup")
    root.geometry("500x400")
    root.resizable(False, False)

    paths = {"schedule": "", "directory": ""}

    # Visit Schedule
    tk.Label(root, text="Visit Schedule File:").pack(anchor="w", padx=20, pady=(20, 0))
    schedule_var = tk.StringVar()
    tk.Entry(root, textvariable=schedule_var, width=50, state="readonly").pack(padx=20)

    def browse_schedule():
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            schedule_var.set(path)
            paths["schedule"] = path

    tk.Button(root, text="Browse", command=browse_schedule).pack(anchor="e", padx=20)

    # Vendor Directory
    tk.Label(root, text="Vendor Directory File:").pack(anchor="w", padx=20, pady=(15, 0))
    directory_var = tk.StringVar()
    tk.Entry(root, textvariable=directory_var, width=50, state="readonly").pack(padx=20)

    def browse_directory():
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            directory_var.set(path)
            paths["directory"] = path

    tk.Button(root, text="Browse", command=browse_directory).pack(anchor="e", padx=20)

    # Sender Name
    tk.Label(root, text="Your Name:").pack(anchor="w", padx=20, pady=(15, 0))
    name_entry = tk.Entry(root, width=50)
    name_entry.pack(padx=20)

    # Sender Email
    tk.Label(root, text="Gmail Address:").pack(anchor="w", padx=20, pady=(15, 0))
    email_entry = tk.Entry(root, width=50)
    email_entry.pack(padx=20)

    # App Password
    tk.Label(root, text="Gmail App Password:").pack(anchor="w", padx=20, pady=(15, 0))
    password_entry = tk.Entry(root, width=50, show="*")
    password_entry.pack(padx=20)

    def save_and_close():
        schedule = paths["schedule"]
        directory = paths["directory"]
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not all([schedule, directory, name, email, password]):
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        config = {
            "visit_schedule_path": schedule,
            "vendor_directory_path": directory,
            "sender_name": name,
            "sender_email": email,
            "app_password": password,
        }
        save_config(config)
        messagebox.showinfo("Success", "Setup complete! You can close this window.")
        root.destroy()

    tk.Button(root, text="Save", command=save_and_close, bg="#4CAF50", fg="white").pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    run_setup()