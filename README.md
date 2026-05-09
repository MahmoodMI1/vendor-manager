#  vendor-reminder

![Python](https://img.shields.io/badge/Python-3.8+-1a1a2e?style=flat-square&logo=python&logoColor=e94560)
![License](https://img.shields.io/badge/License-Private-1a1a2e?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-23%20Passing-1a1a2e?style=flat-square&logo=pytest&logoColor=e94560)
![Platform](https://img.shields.io/badge/Platform-Windows-1a1a2e?style=flat-square&logo=windows&logoColor=e94560)

---

Automated vendor visit reminder system built for facilities management. Reads Excel schedules, matches vendor contacts, and fires off email reminders the night before — no human in the loop. Set it up once, forget it exists.

---

##  Stack

```
Python 3.8+
openpyxl          → Excel parsing
smtplib           → Gmail SMTP
msal + requests   → Microsoft Graph API (Outlook)
tkinter           → Setup wizard + control panel
pytest            → 23 automated tests
GitHub Actions    → CI on every push
```

---

##  Features

| Feature | Status |
|---|---|
| Read vendor visit schedules from Excel | ✅ |
| Match vendors to contacts (case-insensitive) | ✅ |
| Normalize any date format (string, datetime, serial) | ✅ |
| Send reminders via Gmail SMTP | ✅ |
| Send reminders via Outlook Graph API | ✅ |
| Editable email templates (no code changes) | ✅ |
| Smart column detection (headers, not positions) | ✅ |
| One-time GUI setup wizard | ✅ |
| Gmail / Outlook mode toggle | ✅ |
| Silent daily execution via Task Scheduler | ✅ |
| Full logging to file | ✅ |
| 23 automated tests with CI | ✅ |
| Control panel GUI (pause, resume, run now) | 🔜 |
| Package as .exe (no Python install needed) | 🔜 |
| Duplicate email prevention | 🔜 |

---


##  Quick Start

```bash
# install
pip install openpyxl msal requests

# setup (one time)
python -m src.setup_wizard

# run
python run.py

# test
pytest tests/ -v
```

---

##  Email Template

Edit `templates/default.txt`. No code changes needed.

```
Subject: Reminder: Vendor Visit Tomorrow — {vendor_name}

Hi {vendor_name},

Your visit is scheduled for tomorrow, {visit_date}.

Best regards,
{sender_name}
```

Available placeholders: `{vendor_name}` `{visit_date}` `{sender_name}` `{sender_email}`

---

##  Roadmap

- [ ] Control panel GUI — pause, resume, run now, view log
- [ ] Package as standalone .exe via PyInstaller
- [ ] Duplicate email prevention (sent log)
- [ ] Multiple reminder windows (48hr, 24hr, day-of)
- [ ] Summary email to sender
- [ ] Web dashboard for mobile access

---

## Author

**Mahmood Idelbi** — Software Engineering Student: Second Year 

---

<!-- ![demo](assets/demo.gif) -->
<!-- replace with a screen recording of the setup wizard + email landing -->
