# Vendor Manager
Automatically sends reminder emails to vendors the day before their scheduled facility visits. The app reads a visit schedule and a vendor directory (both Excel files), matches vendors to their email addresses, and sends personalized reminder emails via Gmail or Outlook.

## How It Works
1. Every day, `VendorReminderRunner` checks the visit schedule for tomorrow's visits
2. For each visit, it looks up the vendor's email in the vendor directory
3. It sends a reminder email using the configured Gmail or Outlook account
4. All activity is logged to `log.txt` next to the app

## Email Modes
- **Gmail** — uses your Gmail address and an [App Password](https://support.google.com/accounts/answer/185833)
- **Outlook** — uses Microsoft Graph API with a Client ID and Tenant ID (obtained from your IT department)

## Packaging the App

### 1. Install dependencies
```bash
pip install pyinstaller openpyxl msal requests
```

### 2. Build the executables
```bash
pyinstaller build.spec --distpath release
```

### 3. Copy the email template
```bash
cp -r templets/ release/
```

This produces three standalone executables in `release/`:

| Executable | Purpose |
|---|---|
| `VendorReminder` | Main control panel — pause, resume, run now, view log |
| `VendorReminderSetup` | First-time setup wizard — run this before anything else |
| `VendorReminderRunner` | Background runner — called automatically by the scheduler |

### 4. Distribute
Copy the entire `release/` folder to the target machine. On first launch, run `VendorReminderSetup` to configure credentials and file paths.

> **macOS note:** If you see "cannot be opened because the developer cannot be verified", right-click the executable and choose **Open**, or run:
> ```bash
> xattr -cr /path/to/VendorManager
> ```
