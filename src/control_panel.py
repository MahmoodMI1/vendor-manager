import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import threading
from src.paths import get_root
from src.main import run

ROOT = get_root()
PAUSE_FILE = os.path.join(ROOT, "PAUSED")
LOG_PATH = os.path.join(ROOT, "log.txt")


class ControlPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vendor Reminder — Control Panel")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Status
        self.status_var = tk.StringVar()
        self._update_status()

        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=(20, 10))
        tk.Label(status_frame, text="Status:", font=("Arial", 12)).pack(side="left")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, font=("Arial", 12, "bold"))
        self.status_label.pack(side="left", padx=(5, 0))

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.pause_btn = tk.Button(btn_frame, text="Pause", width=12, command=self._pause)
        self.pause_btn.pack(side="left", padx=5)

        self.resume_btn = tk.Button(btn_frame, text="Resume", width=12, command=self._resume)
        self.resume_btn.pack(side="left", padx=5)

        tk.Button(btn_frame, text="Run Now", width=12, command=self._run_now).pack(side="left", padx=5)

        # Log viewer
        tk.Label(self.root, text="Log:", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(15, 0))
        self.log_text = scrolledtext.ScrolledText(self.root, width=55, height=15, state="disabled", font=("Courier", 10))
        self.log_text.pack(padx=20, pady=(5, 10))

        tk.Button(self.root, text="Refresh Log", command=self._load_log).pack(pady=(0, 10))

        self._update_buttons()
        self._load_log()

    def _update_status(self):
        if os.path.exists(PAUSE_FILE):
            self.status_var.set("⏸ Paused")
        else:
            self.status_var.set("✅ Active")

    def _update_buttons(self):
        paused = os.path.exists(PAUSE_FILE)
        self.pause_btn.config(state="disabled" if paused else "normal")
        self.resume_btn.config(state="normal" if paused else "disabled")

    def _pause(self):
        with open(PAUSE_FILE, "w") as f:
            f.write("paused")
        self._update_status()
        self._update_buttons()

    def _resume(self):
        if os.path.exists(PAUSE_FILE):
            os.remove(PAUSE_FILE)
        self._update_status()
        self._update_buttons()

    def _run_now(self):
        if os.path.exists(PAUSE_FILE):
            messagebox.showwarning("Paused", "Reminders are paused. Resume first.")
            return

        def run_in_thread():
            try:
                run()
                self._load_log()
                messagebox.showinfo("Done", "Reminder check complete. Check the log.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _load_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                lines = f.readlines()
                last_50 = lines[-50:]
                self.log_text.insert(tk.END, "".join(last_50))
        else:
            self.log_text.insert(tk.END, "No log file yet.")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)

    def start(self):
        self.root.mainloop()


def run_panel():
    panel = ControlPanel()
    panel.start()


if __name__ == "__main__":
    run_panel()
