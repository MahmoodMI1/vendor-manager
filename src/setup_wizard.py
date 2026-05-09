import tkinter as tk
from tkinter import filedialog, messagebox
from .config_manager import save_config


def run_setup():
    root = tk.Tk()
    root.title("Vendor Reminder — Setup")
    root.geometry("500x600")
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

    # Email Mode
    tk.Label(root, text="Email Mode:").pack(anchor="w", padx=20, pady=(15, 0))
    mode_var = tk.StringVar(value="gmail")

    mode_frame = tk.Frame(root)
    mode_frame.pack(anchor="w", padx=20)
    tk.Radiobutton(mode_frame, text="Gmail", variable=mode_var, value="gmail", command=lambda: toggle_mode()).pack(side="left")
    tk.Radiobutton(mode_frame, text="Outlook", variable=mode_var, value="outlook", command=lambda: toggle_mode()).pack(side="left")

    # Gmail fields
    gmail_frame = tk.Frame(root)

    tk.Label(gmail_frame, text="Gmail Address:").pack(anchor="w")
    email_entry = tk.Entry(gmail_frame, width=50)
    email_entry.pack()

    tk.Label(gmail_frame, text="Gmail App Password:").pack(anchor="w", pady=(10, 0))
    password_entry = tk.Entry(gmail_frame, width=50, show="*")
    password_entry.pack()

    # Outlook fields
    outlook_frame = tk.Frame(root)

    tk.Label(outlook_frame, text="Outlook Email:").pack(anchor="w")
    outlook_email_entry = tk.Entry(outlook_frame, width=50)
    outlook_email_entry.pack()

    tk.Label(outlook_frame, text="Client ID (from IT):").pack(anchor="w", pady=(10, 0))
    client_id_entry = tk.Entry(outlook_frame, width=50)
    client_id_entry.pack()

    tk.Label(outlook_frame, text="Tenant ID (from IT):").pack(anchor="w", pady=(10, 0))
    tenant_id_entry = tk.Entry(outlook_frame, width=50)
    tenant_id_entry.pack()

    def toggle_mode():
        if mode_var.get() == "gmail":
            outlook_frame.pack_forget()
            gmail_frame.pack(padx=20, pady=(5, 0))
        else:
            gmail_frame.pack_forget()
            outlook_frame.pack(padx=20, pady=(5, 0))

    gmail_frame.pack(padx=20, pady=(5, 0))

    def save_and_close():
        schedule = paths["schedule"]
        directory = paths["directory"]
        name = name_entry.get().strip()
        mode = mode_var.get()

        if not all([schedule, directory, name]):
            messagebox.showerror("Missing Info", "Please fill in all fields.")
            return

        config = {
            "visit_schedule_path": schedule,
            "vendor_directory_path": directory,
            "sender_name": name,
            "email_mode": mode,
        }

        if mode == "gmail":
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            if not all([email, password]):
                messagebox.showerror("Missing Info", "Please fill in Gmail address and app password.")
                return
            config["sender_email"] = email
            config["app_password"] = password
        else:
            outlook_email = outlook_email_entry.get().strip()
            client_id = client_id_entry.get().strip()
            tenant_id = tenant_id_entry.get().strip()
            if not all([outlook_email, client_id, tenant_id]):
                messagebox.showerror("Missing Info", "Please fill in Outlook email, Client ID, and Tenant ID.")
                return
            config["sender_email"] = outlook_email
            config["client_id"] = client_id
            config["tenant_id"] = tenant_id

        save_config(config)
        messagebox.showinfo("Success", "Setup complete! You can close this window.")
        root.destroy()

    tk.Button(root, text="Save", command=save_and_close, bg="#4CAF50", fg="white").pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    run_setup()