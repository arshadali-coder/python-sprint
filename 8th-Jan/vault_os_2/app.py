"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              VAULT OS 2.0                                     ║
║                    Next-Generation Password Manager                           ║
║                                                                               ║
║  A premium, secure, and beautiful terminal application for managing          ║
║  your credentials with military-grade encryption.                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import signal
from pathlib import Path
from typing import Optional

from .core.security import SecurityManager, PasswordGenerator
from .core.database import VaultDatabase
from .ui.components import VaultConsole, ConfirmationModal
from .ui.themes import THEMES, CYBER_DARK, ICONS, ASCII_LOGO
from .ui.screens import DashboardScreen, CredentialsScreen
from .ui.screens_extra import PasswordGeneratorScreen, SecurityAuditScreen, SettingsScreen


class VaultOS:
    """Main Vault OS 2.0 Application."""
    
    VERSION = "2.0.0"
    
    def __init__(self, data_dir: Path = None):
        """Initialize Vault OS."""
        self.data_dir = data_dir or Path.home() / ".vault_os"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize core components
        self.security = SecurityManager(self.data_dir)
        self.db = VaultDatabase(self.data_dir / "vault.db")
        
        # Load theme from settings
        theme_name = self.db.get_setting('theme', 'cyber_dark')
        theme = THEMES.get(theme_name, CYBER_DARK)
        self.console = VaultConsole(theme)
        
        # Load settings
        lock_timeout = int(self.db.get_setting('lock_timeout', '300'))
        self.security.set_lock_timeout(lock_timeout)
        
        # Set lock callback
        self.security.set_lock_callback(self._on_vault_locked)
        
        # Initialize screens
        self.dashboard = DashboardScreen(self.console, self.db, self.security)
        self.credentials_screen = CredentialsScreen(self.console, self.db, self.security)
        self.generator_screen = PasswordGeneratorScreen(self.console, self.security)
        self.audit_screen = SecurityAuditScreen(self.console, self.db, self.security)
        self.settings_screen = SettingsScreen(self.console, self.db, self.security)
        
        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        self.console.print(f"\n\n[{self.console.theme.warning}]{ICONS['warning']} Shutting down Vault OS...[/]")
        self.security.lock_vault()
        self.db.close()
        sys.exit(0)
    
    def _on_vault_locked(self):
        """Callback when vault auto-locks."""
        self.console.show_lock_screen()
        self.console.print(f"\n[{self.console.theme.warning}]Vault locked due to inactivity[/]")
        self._unlock_vault()
    
    def run(self):
        """Main application entry point."""
        try:
            self._show_startup()
            
            if not self._authenticate():
                return
            
            self._main_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self._shutdown()
    
    def _show_startup(self):
        """Show startup animation."""
        self.console.clear()
        self.console.print_logo(animated=True)
        
        self.console.print()
        self.console.print_centered(f"Version {self.VERSION}", style=self.console.theme.muted)
        self.console.print_centered("Next-Generation Password Manager", style=self.console.theme.secondary)
        self.console.print()
        
        time.sleep(0.5)
    
    def _authenticate(self) -> bool:
        """Handle authentication flow."""
        if not self.security.is_vault_initialized():
            return self._first_run_setup()
        else:
            return self._unlock_vault()
    
    def _first_run_setup(self) -> bool:
        """First-time setup wizard."""
        self.console.clear()
        self.console.show_header(f"{ICONS['rocket']} Welcome to Vault OS 2.0!", "Let's set up your secure vault")
        
        self.console.print(f"""
[{self.console.theme.text}]Vault OS uses military-grade encryption to protect your passwords.

{ICONS['shield']} All data is encrypted with AES-256
{ICONS['key']} Master password is never stored
{ICONS['lock']} Auto-lock protects against unauthorized access
[/]
""")
        
        self.console.show_divider("Create Master Password")
        
        while True:
            password = self.console.prompt("Create master password (min 8 chars)", password=True)
            
            if len(password) < 8:
                self.console.show_error("Password must be at least 8 characters")
                continue
            
            score, rating, issues = PasswordGenerator.analyze_strength(password)
            self.console.display_password_strength(score, rating, issues)
            
            if score < 40:
                if not self.console.confirm("Password is weak. Continue anyway?"):
                    continue
            
            confirm = self.console.prompt("Confirm master password", password=True)
            
            if password != confirm:
                self.console.show_error("Passwords don't match")
                continue
            
            break
        
        self.console.show_spinner("Initializing secure vault...", 1.5)
        
        try:
            self.security.create_master_password(password)
            self.console.show_unlock_animation()
            self.console.show_success("Vault created successfully!")
            time.sleep(1)
            return True
        except Exception as e:
            self.console.show_error(f"Failed to create vault: {str(e)}")
            return False
    
    def _unlock_vault(self) -> bool:
        """Unlock existing vault."""
        self.console.clear()
        self.console.show_lock_screen()
        
        attempts = 3
        
        while attempts > 0:
            self.console.print()
            password = self.console.prompt("Enter master password", password=True)
            
            self.console.show_spinner("Verifying...", 0.5)
            
            if self.security.verify_master_password(password):
                self.console.show_unlock_animation()
                return True
            
            attempts -= 1
            if attempts > 0:
                self.console.show_error(f"Invalid password. {attempts} attempts remaining.")
            else:
                self.console.show_error("Too many failed attempts. Vault locked.")
                time.sleep(2)
                return False
        
        return False
    
    def _main_loop(self):
        """Main application loop."""
        while True:
            if not self.security.is_unlocked():
                if not self._unlock_vault():
                    break
            
            action = self.dashboard.render()
            
            if action == '1':
                self._credentials_flow()
            elif action == '2':
                self.credentials_screen.add_credential()
                self.console.wait_for_key()
            elif action == '3':
                self.generator_screen.render()
            elif action == '4':
                self.audit_screen.render()
            elif action == '5':
                self.settings_screen.render()
            elif action == '6':
                self.security.lock_vault()
                if not self._unlock_vault():
                    break
            elif action == 'q':
                if self._confirm_exit():
                    break
    
    def _credentials_flow(self):
        """Handle credentials browsing flow."""
        search_query = None
        
        while True:
            result = self.credentials_screen.list_credentials(search_query)
            
            if result == 'back':
                break
            elif result is None:
                continue
            elif isinstance(result, tuple):
                action, data = result
                
                if action == 'search':
                    search_query = data
                elif action == 'view':
                    view_result = self.credentials_screen.view_credential(data)
                    
                    if isinstance(view_result, tuple):
                        sub_action, cred = view_result
                        if sub_action == 'edit':
                            self.credentials_screen.edit_credential(cred)
                        elif sub_action == 'delete':
                            self.credentials_screen.delete_credential(cred)
                    elif view_result == 'back':
                        continue
    
    def _confirm_exit(self) -> bool:
        """Confirm exit with modal."""
        modal = ConfirmationModal(self.console)
        return modal.show(
            "Exit Vault OS",
            "Are you sure you want to exit? Your vault will be locked.",
            confirm_text="Exit",
            cancel_text="Stay"
        )
    
    def _shutdown(self):
        """Clean shutdown."""
        self.console.clear()
        self.console.print_logo(animated=False)
        self.console.print()
        self.console.print_centered(f"{ICONS['shield']} Vault locked and secured", 
                                    style=self.console.theme.success)
        self.console.print_centered("Stay safe, Commander!", style=self.console.theme.muted)
        self.console.print()
        
        self.security.lock_vault()
        self.db.close()


def main():
    """Application entry point."""
    app = VaultOS()
    app.run()


if __name__ == "__main__":
    main()
