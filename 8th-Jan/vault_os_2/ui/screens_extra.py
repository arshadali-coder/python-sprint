"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     ADDITIONAL SCREENS MODULE                                 ║
║           Password Generator, Security Audit, Settings                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Dict, Any
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.progress import Progress, BarColumn

from .components import VaultConsole, MenuSelector, ConfirmationModal
from .themes import ICONS, THEMES, STRENGTH_COLORS, STRENGTH_BARS
from ..core.database import VaultDatabase
from ..core.security import SecurityManager, PasswordGenerator


class PasswordGeneratorScreen:
    """Interactive password generator."""
    
    def __init__(self, console: VaultConsole, security: SecurityManager):
        self.console = console
        self.security = security
        self.theme = console.theme
    
    def render(self) -> str:
        """Render password generator interface."""
        self.console.clear()
        self.console.show_header(f"{ICONS['key']} Password Generator", "Create secure passwords")
        
        # Options
        length = 16
        include_upper = True
        include_digits = True
        include_symbols = True
        exclude_ambiguous = False
        
        while True:
            self.console.print(f"\n[{self.theme.muted}]Current Settings:[/]")
            self.console.print(f"  Length: [{self.theme.accent}]{length}[/]")
            self.console.print(f"  Uppercase: [{self.theme.success if include_upper else self.theme.error}]{'Yes' if include_upper else 'No'}[/]")
            self.console.print(f"  Numbers: [{self.theme.success if include_digits else self.theme.error}]{'Yes' if include_digits else 'No'}[/]")
            self.console.print(f"  Symbols: [{self.theme.success if include_symbols else self.theme.error}]{'Yes' if include_symbols else 'No'}[/]")
            self.console.print(f"  Exclude Ambiguous: [{self.theme.success if exclude_ambiguous else self.theme.error}]{'Yes' if exclude_ambiguous else 'No'}[/]")
            
            self.console.print(f"\n  [{self.theme.primary}][G][/] {ICONS['rocket']} Generate Password")
            self.console.print(f"  [{self.theme.primary}][L][/] Change Length")
            self.console.print(f"  [{self.theme.primary}][U][/] Toggle Uppercase")
            self.console.print(f"  [{self.theme.primary}][N][/] Toggle Numbers")
            self.console.print(f"  [{self.theme.primary}][S][/] Toggle Symbols")
            self.console.print(f"  [{self.theme.primary}][A][/] Toggle Ambiguous")
            self.console.print(f"  [{self.theme.error}][B][/] Back")
            
            choice = self.console.prompt("Option").strip().lower()
            
            if choice == 'b':
                return 'back'
            elif choice == 'l':
                try:
                    new_len = int(self.console.prompt("Password length (8-128)", default=str(length)))
                    length = max(8, min(128, new_len))
                except ValueError:
                    pass
            elif choice == 'u':
                include_upper = not include_upper
            elif choice == 'n':
                include_digits = not include_digits
            elif choice == 's':
                include_symbols = not include_symbols
            elif choice == 'a':
                exclude_ambiguous = not exclude_ambiguous
            elif choice == 'g':
                # Generate password
                password = PasswordGenerator.generate(
                    length=length,
                    include_uppercase=include_upper,
                    include_digits=include_digits,
                    include_symbols=include_symbols,
                    exclude_ambiguous=exclude_ambiguous
                )
                
                self.console.print(f"\n[{self.theme.success}]{ICONS['key']} Generated Password:[/]")
                self.console.print(f"  [{self.theme.accent}]{password}[/]")
                
                score, rating, issues = PasswordGenerator.analyze_strength(password)
                self.console.display_password_strength(score, rating, issues)
                
                self.console.print(f"\n  [{self.theme.primary}][C][/] Copy to Clipboard")
                self.console.print(f"  [{self.theme.primary}][R][/] Regenerate")
                self.console.print(f"  [{self.theme.muted}]Enter[/] Continue")
                
                action = self.console.prompt("Action").strip().lower()
                if action == 'c':
                    self._copy_to_clipboard(password)
    
    def _copy_to_clipboard(self, text: str):
        try:
            import pyperclip
            pyperclip.copy(text)
            self.console.show_success("Copied to clipboard!")
        except ImportError:
            self.console.show_warning("pyperclip not installed")


class SecurityAuditScreen:
    """Security audit and analysis."""
    
    def __init__(self, console: VaultConsole, db: VaultDatabase, security: SecurityManager):
        self.console = console
        self.db = db
        self.security = security
        self.theme = console.theme
    
    def render(self):
        """Render security audit screen."""
        self.console.clear()
        self.console.show_header(f"{ICONS['audit']} Security Audit", "Analyzing vault security...")
        
        self.console.show_spinner("Scanning credentials...", 1.0)
        
        credentials = self.db.get_all_credentials()
        
        if not credentials:
            self.console.show_info("No credentials to audit")
            self.console.wait_for_key()
            return
        
        audit_results = self._analyze_credentials(credentials)
        self._display_audit_results(audit_results)
        
        self.console.wait_for_key()
    
    def _analyze_credentials(self, credentials) -> Dict[str, Any]:
        """Analyze all credentials for security issues."""
        results = {
            'total': len(credentials),
            'weak_passwords': [],
            'reused_passwords': [],
            'old_passwords': [],
            'strength_distribution': {'Critical': 0, 'Weak': 0, 'Fair': 0, 'Good': 0, 'Excellent': 0}
        }
        
        password_hashes = {}
        
        for cred in credentials:
            try:
                password = self.security.decrypt(cred.encrypted_password)
                score, rating, issues = PasswordGenerator.analyze_strength(password)
                
                results['strength_distribution'][rating] += 1
                
                if score < 40:
                    results['weak_passwords'].append({
                        'website': cred.website,
                        'username': cred.username,
                        'score': score,
                        'rating': rating
                    })
                
                # Check for reuse
                import hashlib
                pw_hash = hashlib.sha256(password.encode()).hexdigest()
                if pw_hash in password_hashes:
                    password_hashes[pw_hash].append(cred.website)
                else:
                    password_hashes[pw_hash] = [cred.website]
                
                # Check age (>90 days)
                from datetime import datetime, timedelta
                last_updated = datetime.fromisoformat(cred.last_updated.replace('Z', '+00:00'))
                if datetime.now(last_updated.tzinfo) - last_updated > timedelta(days=90):
                    results['old_passwords'].append({
                        'website': cred.website,
                        'age_days': (datetime.now(last_updated.tzinfo) - last_updated).days
                    })
            except:
                continue
        
        # Find reused passwords
        for pw_hash, sites in password_hashes.items():
            if len(sites) > 1:
                results['reused_passwords'].append(sites)
        
        return results
    
    def _display_audit_results(self, results: Dict[str, Any]):
        """Display audit results."""
        # Health score
        total = results['total']
        weak_count = len(results['weak_passwords'])
        reused_count = sum(len(sites) for sites in results['reused_passwords'])
        
        health_score = max(0, 100 - (weak_count * 10) - (reused_count * 5))
        
        self.console.print()
        
        # Health score panel
        health_color = 'green' if health_score >= 80 else 'yellow' if health_score >= 50 else 'red'
        health_text = Text()
        health_text.append(f"\n{ICONS['health']} Vault Health Score: ", style=self.theme.text)
        health_text.append(f"{health_score}/100\n", style=f"bold {health_color}")
        
        panel = self.console.create_panel(health_text, title="Security Overview")
        self.console.print(panel)
        
        # Strength distribution
        self.console.show_divider("Password Strength Distribution")
        
        dist = results['strength_distribution']
        for rating in ['Excellent', 'Good', 'Fair', 'Weak', 'Critical']:
            count = dist[rating]
            bar_len = int((count / max(total, 1)) * 20)
            bar = '█' * bar_len + '░' * (20 - bar_len)
            color = STRENGTH_COLORS.get(rating, 'white')
            self.console.print(f"  [{color}]{rating:10}[/] [{color}]{bar}[/] {count}/{total}")
        
        # Issues
        if results['weak_passwords']:
            self.console.print()
            self.console.show_divider(f"{ICONS['warning']} Weak Passwords")
            for item in results['weak_passwords'][:5]:
                self.console.print(f"  [{self.theme.error}]•[/] {item['website']} ({item['rating']})")
        
        if results['reused_passwords']:
            self.console.print()
            self.console.show_divider(f"{ICONS['error']} Reused Passwords")
            for sites in results['reused_passwords'][:5]:
                self.console.print(f"  [{self.theme.error}]•[/] {', '.join(sites)}")
        
        if results['old_passwords']:
            self.console.print()
            self.console.show_divider(f"{ICONS['clock']} Old Passwords (>90 days)")
            for item in results['old_passwords'][:5]:
                self.console.print(f"  [{self.theme.warning}]•[/] {item['website']} ({item['age_days']} days)")


class SettingsScreen:
    """Settings and configuration."""
    
    def __init__(self, console: VaultConsole, db: VaultDatabase, security: SecurityManager):
        self.console = console
        self.db = db
        self.security = security
        self.theme = console.theme
    
    def render(self) -> str:
        """Render settings screen."""
        while True:
            self.console.clear()
            self.console.show_header(f"{ICONS['settings']} Settings")
            
            current_theme = self.db.get_setting('theme', 'cyber_dark')
            lock_time = int(self.db.get_setting('lock_timeout', '300'))
            
            self.console.print(f"  [{self.theme.primary}][1][/] {ICONS['gear']} Theme: [{self.theme.accent}]{current_theme}[/]")
            self.console.print(f"  [{self.theme.primary}][2][/] {ICONS['clock']} Auto-lock: [{self.theme.accent}]{lock_time // 60} minutes[/]")
            self.console.print(f"  [{self.theme.primary}][3][/] {ICONS['key']} Change Master Password")
            self.console.print(f"  [{self.theme.primary}][4][/] {ICONS['export']} Export Vault")
            self.console.print(f"  [{self.theme.primary}][5][/] {ICONS['import']} Import Vault")
            self.console.print(f"  [{self.theme.primary}][6][/] {ICONS['chart']} View Activity Logs")
            self.console.print(f"\n  [{self.theme.error}][B][/] Back")
            
            choice = self.console.prompt("Option").strip().lower()
            
            if choice == 'b':
                return 'back'
            elif choice == '1':
                self._change_theme()
            elif choice == '2':
                self._change_lock_timeout()
            elif choice == '3':
                self._change_master_password()
            elif choice == '4':
                self._export_vault()
            elif choice == '5':
                self._import_vault()
            elif choice == '6':
                self._view_activity_logs()
    
    def _change_theme(self):
        """Change application theme."""
        self.console.print(f"\n[{self.theme.muted}]Available Themes:[/]")
        themes = list(THEMES.keys())
        for i, name in enumerate(themes, 1):
            self.console.print(f"  [{self.theme.primary}][{i}][/] {name}")
        
        try:
            idx = int(self.console.prompt("Select theme")) - 1
            if 0 <= idx < len(themes):
                self.db.set_setting('theme', themes[idx])
                self.console.show_success(f"Theme changed to {themes[idx]}. Restart to apply.")
        except ValueError:
            pass
    
    def _change_lock_timeout(self):
        """Change auto-lock timeout."""
        try:
            minutes = int(self.console.prompt("Auto-lock timeout (minutes)", default="5"))
            seconds = max(60, minutes * 60)  # Minimum 1 minute
            self.db.set_setting('lock_timeout', str(seconds))
            self.security.set_lock_timeout(seconds)
            self.console.show_success(f"Auto-lock set to {minutes} minutes")
        except ValueError:
            self.console.show_error("Invalid input")
    
    def _change_master_password(self):
        """Change master password."""
        old_pw = self.console.prompt("Current master password", password=True)
        new_pw = self.console.prompt("New master password", password=True)
        confirm_pw = self.console.prompt("Confirm new password", password=True)
        
        if new_pw != confirm_pw:
            self.console.show_error("Passwords don't match")
            return
        
        # Re-encrypt all credentials
        credentials = self.db.get_all_credentials()
        decrypted_passwords = {}
        
        for cred in credentials:
            try:
                decrypted_passwords[cred.id] = self.security.decrypt(cred.encrypted_password)
            except:
                self.console.show_error("Failed to decrypt credentials")
                return
        
        if self.security.change_master_password(old_pw, new_pw):
            # Re-encrypt all passwords
            for cred in credentials:
                cred.encrypted_password = self.security.encrypt(decrypted_passwords[cred.id])
                self.db.update_credential(cred)
            
            self.console.show_success("Master password changed successfully!")
        else:
            self.console.show_error("Failed to change password")
    
    def _export_vault(self):
        """Export vault to encrypted file."""
        export_pw = self.console.prompt("Export password", password=True)
        confirm_pw = self.console.prompt("Confirm password", password=True)
        
        if export_pw != confirm_pw:
            self.console.show_error("Passwords don't match")
            return
        
        try:
            encrypted_data = self.db.export_vault(self.security, export_pw)
            
            filename = f"vault_export_{self.console.prompt('Filename', default='backup')}.vault"
            
            from pathlib import Path
            export_path = Path.cwd() / filename
            export_path.write_text(encrypted_data)
            
            self.console.show_success(f"Vault exported to {filename}")
        except Exception as e:
            self.console.show_error(f"Export failed: {str(e)}")
    
    def _import_vault(self):
        """Import vault from encrypted file."""
        filename = self.console.prompt("Import filename (without .vault)")
        import_pw = self.console.prompt("Import password", password=True)
        
        try:
            from pathlib import Path
            import_path = Path.cwd() / f"{filename}.vault"
            
            if not import_path.exists():
                self.console.show_error("File not found")
                return
            
            encrypted_data = import_path.read_text()
            count = self.db.import_vault(self.security, encrypted_data, import_pw)
            
            self.console.show_success(f"Imported {count} credentials")
        except Exception as e:
            self.console.show_error(f"Import failed: {str(e)}")
    
    def _view_activity_logs(self):
        """View activity logs."""
        self.console.clear()
        self.console.show_header(f"{ICONS['chart']} Activity Logs")
        
        logs = self.db.get_activity_logs(20)
        
        if not logs:
            self.console.show_info("No activity logs yet")
        else:
            table = self.console.create_table(columns=[
                ("Time", self.theme.muted),
                ("Action", self.theme.primary),
                ("Target", self.theme.text),
                ("Details", self.theme.muted),
            ])
            
            for log in logs:
                action_color = {
                    'ADD': self.theme.success,
                    'EDIT': self.theme.warning,
                    'DELETE': self.theme.error,
                }.get(log.action, self.theme.text)
                
                table.add_row(
                    log.timestamp[:16].replace('T', ' '),
                    f"[{action_color}]{log.action}[/]",
                    log.target,
                    log.details[:30]
                )
            
            self.console.print(table)
        
        self.console.wait_for_key()
