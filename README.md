# Vendor Manager
Automatically sends reminder emails to vendors before scheduled visits.

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
