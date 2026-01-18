# Vault OS 2.0 - Next-Generation Password Manager

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-00d4ff?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Security-AES--256-green?style=for-the-badge&logo=shield" alt="Security">
  <img src="https://img.shields.io/badge/UI-Rich%20TUI-purple?style=for-the-badge" alt="UI">
</p>

```
██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗     ██████╗ ███████╗
██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝    ██╔═══██╗██╔════╝
██║   ██║███████║██║   ██║██║     ██║       ██║   ██║███████╗
╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║       ██║   ██║╚════██║
 ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║       ╚██████╔╝███████║
  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝        ╚═════╝ ╚══════╝
                     VERSION 2.0
```

A **premium, secure, and beautiful** terminal password manager that feels like a desktop app inside your terminal.

---

## ✨ Features

### 🔐 Security First
- **Master Password Protection** - PBKDF2 with 480,000 iterations
- **AES-256 Encryption** - Military-grade Fernet encryption for all credentials
- **Auto-Lock** - Automatic vault locking after inactivity
- **Secure Memory** - Sensitive data cleared on lock
- **No Plaintext Storage** - Master password is never stored

### 🎨 Beautiful Terminal UI
- **Rich TUI** - Panels, tables, progress bars, and spinners
- **Multiple Themes** - Cyber Dark, Neon Matrix, Ocean Depth, Sunset Glow, Light Mode
- **Animated Transitions** - Smooth lock/unlock animations
- **Color-Coded States** - Visual feedback for all actions
- **ASCII Art** - Premium branding experience

### 💾 Robust Data Management
- **SQLite Database** - Scalable and reliable storage
- **Categories** - Organize credentials (Social, Finance, Work, etc.)
- **Search & Filter** - Instant fuzzy search
- **Activity Logs** - Track all actions (never logs passwords)
- **Export/Import** - Encrypted backup and restore

### 🔑 Password Tools
- **Password Generator** - Customizable secure passwords
- **Strength Analyzer** - Visual strength indicators
- **Security Audit** - Detect weak/reused passwords
- **Clipboard Integration** - Copy without displaying

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the project directory
cd vault_os_2

# Install dependencies
pip install -r requirements.txt

# Run Vault OS
python run_vault.py
```

### First Run

1. Launch Vault OS - animated logo appears
2. Create your master password (min 8 characters)
3. View strength analysis and suggestions
4. Your encrypted vault is ready!

---

## 📖 User Guide

### Dashboard

The main dashboard shows:
- **Total Credentials** - Count of stored passwords
- **Categories** - Number of organization categories
- **Security Status** - Vault encryption status
- **Recent Activity** - Last actions performed

### Quick Actions

| Key | Action |
|-----|--------|
| `1` | View Credentials |
| `2` | Add New Credential |
| `3` | Password Generator |
| `4` | Security Audit |
| `5` | Settings |
| `6` | Lock Vault |
| `Q` | Exit |

### Managing Credentials

**Add a Credential:**
1. Press `2` from dashboard
2. Enter website, username
3. Choose to enter password or generate one
4. Select category
5. Add optional notes

**View/Edit/Delete:**
1. Press `1` to view all credentials
2. Enter number to select
3. `R` - Reveal password | `C` - Copy | `E` - Edit | `D` - Delete

### Password Generator

Customizable options:
- **Length** - 8 to 128 characters
- **Uppercase** - A-Z
- **Numbers** - 0-9
- **Symbols** - !@#$%^&*
- **Exclude Ambiguous** - No 0O1lI

### Security Audit

Analyzes your vault for:
- ❌ **Weak passwords** - Low entropy
- 🔄 **Reused passwords** - Same across sites
- ⏰ **Old passwords** - Over 90 days old
- 📊 **Health Score** - Overall vault security

---

## ⚙️ Settings

### Themes
- `cyber_dark` - Default cyan/purple (recommended)
- `neon_matrix` - Matrix-style green
- `ocean_depth` - Deep blue ocean
- `sunset_glow` - Warm orange/pink
- `light_mode` - Light theme

### Configuration
- **Auto-Lock Timeout** - 1-60 minutes
- **Master Password Change** - Re-encrypts all data
- **Export Vault** - Password-protected backup
- **Import Vault** - Restore from backup
- **Activity Logs** - View all actions

---

## 🏗️ Architecture

```
vault_os_2/
├── __init__.py          # Package info
├── app.py               # Main application orchestrator
├── core/
│   ├── __init__.py
│   ├── security.py      # Encryption, hashing, sessions
│   └── database.py      # SQLite storage layer
└── ui/
    ├── __init__.py
    ├── themes.py        # Colors, ASCII art, icons
    ├── components.py    # Reusable UI elements
    ├── screens.py       # Dashboard, credentials
    └── screens_extra.py # Generator, audit, settings
```

### Design Principles
- **Clean Architecture** - Separation of concerns
- **No Global State** - Encapsulated components
- **Modular Design** - Easily extensible
- **Security by Design** - Defense in depth

---

## 📈 Improvements Over Vault OS 1.0

| Feature | 1.0 | 2.0 |
|---------|-----|-----|
| Storage | JSON file | SQLite database |
| Encryption | None ❌ | AES-256 ✅ |
| Master Password | None ❌ | PBKDF2 hashed ✅ |
| UI | Basic input() | Rich TUI ✅ |
| Password Generator | None ❌ | Full featured ✅ |
| Security Audit | None ❌ | Complete ✅ |
| Auto-Lock | None ❌ | Configurable ✅ |
| Themes | None ❌ | 5 themes ✅ |
| Categories | None ❌ | 6 default ✅ |
| Export/Import | None ❌ | Encrypted ✅ |
| Activity Logs | None ❌ | Full history ✅ |
| Clipboard | None ❌ | Auto-clear ✅ |

---

## 🔒 Security Details

### Encryption
- **Algorithm**: Fernet (AES-128-CBC with HMAC)
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 480,000 (OWASP recommended)
- **Salt**: 32 bytes cryptographically random

### Session Security
- Auto-lock after configurable inactivity
- Session cleared from memory on lock
- No password caching

---

## 🎯 Pro Tips

1. **Strong Master Password** - Use a passphrase like "correct-horse-battery-staple"
2. **Regular Audits** - Check security audit weekly
3. **Backup Often** - Export encrypted backups
4. **Unique Passwords** - Use generator for every site
5. **Update Old Passwords** - Check the "old passwords" audit

---

## 📜 License

MIT License - Free to use, modify, and distribute.

---

<p align="center">
  <b>Stay Secure, Commander! 🛡️</b>
</p>
