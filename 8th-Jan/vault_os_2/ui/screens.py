"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          SCREENS MODULE                                       ║
║              Dashboard, Credentials, Settings, and More                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from typing import Optional, List
from datetime import datetime
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.box import ROUNDED

from .components import VaultConsole, MenuSelector, ConfirmationModal, StatusBar
from .themes import ICONS, THEMES
from ..core.database import VaultDatabase, Credential
from ..core.security import SecurityManager, PasswordGenerator


class DashboardScreen:
    """Main dashboard with vault overview."""
    
    def __init__(self, console: VaultConsole, db: VaultDatabase, security: SecurityManager):
        self.console = console
        self.db = db
        self.security = security
        self.theme = console.theme
    
    def render(self) -> str:
        """Render dashboard and return user action."""
        self.console.clear()
        
        # Status bar
        status = StatusBar(self.console)
        self.console.print(status.render(
            vault_status="Unlocked" if self.security.is_unlocked() else "Locked",
            credential_count=self.db.get_credential_count(),
            time_to_lock=self.security.get_time_until_lock(),
            current_screen="Dashboard"
        ))
        
        # Stats cards
        stats = self.db.get_statistics()
        self._render_stats_cards(stats)
        
        # Recent activity
        self._render_recent_activity()
        
        # Quick actions menu
        return self._show_quick_actions()
    
    def _render_stats_cards(self, stats: dict):
        """Render statistics cards."""
        cards = []
        
        # Total credentials
        card1 = Text()
        card1.append(f"\n{ICONS['vault']} ", style=self.theme.primary)
        card1.append("Total Credentials\n", style=self.theme.muted)
        card1.append(f"    {stats['total_credentials']}\n", style=f"bold {self.theme.primary}")
        cards.append(Panel(card1, border_style=self.theme.border, box=ROUNDED))
        
        # Categories
        card2 = Text()
        card2.append(f"\n{ICONS['folder']} ", style=self.theme.secondary)
        card2.append("Categories\n", style=self.theme.muted)
        card2.append(f"    {len(stats.get('by_category', {}))}\n", style=f"bold {self.theme.secondary}")
        cards.append(Panel(card2, border_style=self.theme.border, box=ROUNDED))
        
        # Security status
        card3 = Text()
        card3.append(f"\n{ICONS['shield']} ", style=self.theme.success)
        card3.append("Security\n", style=self.theme.muted)
        card3.append(f"    Active\n", style=f"bold {self.theme.success}")
        cards.append(Panel(card3, border_style=self.theme.border, box=ROUNDED))
        
        # Last modified
        last_mod = self.db.get_last_modified_credential()
        card4 = Text()
        card4.append(f"\n{ICONS['time']} ", style=self.theme.accent)
        card4.append("Last Updated\n", style=self.theme.muted)
        if last_mod:
            card4.append(f"    {last_mod.website[:12]}\n", style=f"bold {self.theme.accent}")
        else:
            card4.append(f"    None\n", style=self.theme.muted)
        cards.append(Panel(card4, border_style=self.theme.border, box=ROUNDED))
        
        self.console.print(Columns(cards, equal=True, expand=True))
    
    def _render_recent_activity(self):
        """Render recent activity section."""
        logs = self.db.get_activity_logs(5)
        
        if logs:
            self.console.show_divider("Recent Activity")
            for log in logs[:5]:
                action_icon = {
                    'ADD': ICONS['add'],
                    'EDIT': ICONS['edit'],
                    'DELETE': ICONS['delete'],
                    'EXPORT': ICONS['export'],
                    'IMPORT': ICONS['import']
                }.get(log.action, ICONS['info'])
                
                timestamp = log.timestamp[:16].replace('T', ' ')
                self.console.print(f"  {action_icon} [{self.theme.muted}]{timestamp}[/] {log.target}")
    
    def _show_quick_actions(self) -> str:
        """Show quick actions menu."""
        self.console.print()
        self.console.show_divider("Quick Actions")
        
        options = [
            ('1', ICONS['search'], "View Credentials"),
            ('2', ICONS['add'], "Add New Credential"),
            ('3', ICONS['key'], "Password Generator"),
            ('4', ICONS['audit'], "Security Audit"),
            ('5', ICONS['settings'], "Settings"),
            ('6', ICONS['lock'], "Lock Vault"),
        ]
        
        for key, icon, label in options:
            self.console.print(f"  [{self.theme.primary}][{key}][/] {icon} {label}")
        
        self.console.print(f"\n  [{self.theme.error}][Q][/] {ICONS['logout']} Exit Vault OS")
        self.console.print()
        
        return self.console.prompt("Select action").strip().lower()


class CredentialsScreen:
    """Credential management screen."""
    
    def __init__(self, console: VaultConsole, db: VaultDatabase, security: SecurityManager):
        self.console = console
        self.db = db
        self.security = security
        self.theme = console.theme
    
    def list_credentials(self, search_query: str = None):
        """Display list of all credentials."""
        self.console.clear()
        self.console.show_header(f"{ICONS['vault']} Credential Vault", 
                                 f"Search: '{search_query}'" if search_query else "All credentials")
        
        if search_query:
            credentials = self.db.search_credentials(search_query)
        else:
            credentials = self.db.get_all_credentials()
        
        if not credentials:
            self.console.show_info("No credentials found.")
            return None
        
        # Create table
        table = self.console.create_table(columns=[
            ("#", self.theme.muted),
            ("Website", f"bold {self.theme.primary}"),
            ("Username", self.theme.text),
            ("Category", self.theme.secondary),
            ("Last Updated", self.theme.muted),
        ])
        
        for i, cred in enumerate(credentials, 1):
            table.add_row(
                str(i),
                cred.website[:25],
                cred.username[:20],
                cred.category,
                cred.last_updated[:10]
            )
        
        self.console.print(table)
        self.console.print()
        
        # Options
        self.console.print(f"  [{self.theme.primary}][#][/] View credential by number")
        self.console.print(f"  [{self.theme.primary}][S][/] {ICONS['search']} Search")
        self.console.print(f"  [{self.theme.error}][B][/] Back to Dashboard")
        self.console.print()
        
        choice = self.console.prompt("Action").strip().lower()
        
        if choice == 'b':
            return 'back'
        elif choice == 's':
            query = self.console.prompt("Search query")
            return ('search', query)
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(credentials):
                    return ('view', credentials[idx])
            except ValueError:
                pass
        
        return None
    
    def view_credential(self, credential: Credential):
        """View a single credential with actions."""
        self.console.clear()
        self.console.show_header(f"{ICONS['vault']} View Credential")
        
        # Decrypt password
        try:
            decrypted_pw = self.security.decrypt(credential.encrypted_password)
        except:
            decrypted_pw = "[Error decrypting]"
        
        # Display card
        card = Text()
        card.append(f"\n{ICONS['website']} Website: ", style=self.theme.muted)
        card.append(f"{credential.website}\n", style=f"bold {self.theme.primary}")
        card.append(f"{ICONS['user']} Username: ", style=self.theme.muted)
        card.append(f"{credential.username}\n", style=self.theme.text)
        card.append(f"{ICONS['password']} Password: ", style=self.theme.muted)
        card.append(f"{'•' * 12}\n", style=self.theme.warning)
        card.append(f"{ICONS['folder']} Category: ", style=self.theme.muted)
        card.append(f"{credential.category}\n", style=self.theme.secondary)
        if credential.notes:
            card.append(f"{ICONS['info']} Notes: ", style=self.theme.muted)
            card.append(f"{credential.notes}\n", style=self.theme.text)
        card.append(f"{ICONS['calendar']} Created: ", style=self.theme.muted)
        card.append(f"{credential.created_at[:10]}\n", style=self.theme.muted)
        card.append(f"{ICONS['time']} Updated: ", style=self.theme.muted)
        card.append(f"{credential.last_updated[:10]}\n", style=self.theme.muted)
        
        panel = self.console.create_panel(card, title=credential.website)
        self.console.print(panel)
        self.console.print()
        
        # Actions
        self.console.print(f"  [{self.theme.primary}][R][/] {ICONS['unlock']} Reveal Password")
        self.console.print(f"  [{self.theme.primary}][C][/] {ICONS['copy']} Copy to Clipboard")
        self.console.print(f"  [{self.theme.primary}][E][/] {ICONS['edit']} Edit Credential")
        self.console.print(f"  [{self.theme.error}][D][/] {ICONS['delete']} Delete Credential")
        self.console.print(f"  [{self.theme.muted}][B][/] Back")
        self.console.print()
        
        choice = self.console.prompt("Action").strip().lower()
        
        if choice == 'r':
            self.console.print(f"\n[{self.theme.accent}]{ICONS['key']} Password: {decrypted_pw}[/]\n")
            self.console.wait_for_key()
        elif choice == 'c':
            self._copy_to_clipboard(decrypted_pw)
        elif choice == 'e':
            return ('edit', credential)
        elif choice == 'd':
            return ('delete', credential)
        elif choice == 'b':
            return 'back'
        
        return None
    
    def add_credential(self) -> Optional[Credential]:
        """Add a new credential."""
        self.console.clear()
        self.console.show_header(f"{ICONS['add']} Add New Credential")
        
        website = self.console.prompt(f"{ICONS['website']} Website")
        if not website:
            self.console.show_error("Website is required")
            return None
        
        username = self.console.prompt(f"{ICONS['user']} Username")
        if not username:
            self.console.show_error("Username is required")
            return None
        
        # Password options
        self.console.print(f"\n  [{self.theme.primary}][1][/] Enter password manually")
        self.console.print(f"  [{self.theme.primary}][2][/] Generate secure password")
        
        pw_choice = self.console.prompt("Password option", choices=['1', '2'])
        
        if pw_choice == '2':
            password = PasswordGenerator.generate()
            self.console.print(f"\n[{self.theme.success}]Generated: {password}[/]")
            score, rating, issues = PasswordGenerator.analyze_strength(password)
            self.console.display_password_strength(score, rating, issues)
        else:
            password = self.console.prompt(f"{ICONS['password']} Password", password=True)
            if password:
                score, rating, issues = PasswordGenerator.analyze_strength(password)
                self.console.display_password_strength(score, rating, issues)
        
        if not password:
            self.console.show_error("Password is required")
            return None
        
        # Category selection
        categories = self.db.get_categories()
        cat_names = [c['name'] for c in categories]
        
        self.console.print(f"\n[{self.theme.muted}]Available categories:[/]")
        for i, cat in enumerate(categories, 1):
            self.console.print(f"  [{self.theme.primary}][{i}][/] {cat['icon']} {cat['name']}")
        
        cat_idx = self.console.prompt("Category (number)", default="1")
        try:
            category = cat_names[int(cat_idx) - 1]
        except:
            category = "General"
        
        notes = self.console.prompt(f"{ICONS['info']} Notes (optional)", default="")
        
        # Encrypt and save
        encrypted_pw = self.security.encrypt(password)
        
        credential = Credential(
            id=None,
            website=website,
            username=username,
            encrypted_password=encrypted_pw,
            notes=notes,
            category=category,
            created_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            last_accessed=None,
            access_count=0
        )
        
        try:
            self.db.add_credential(credential)
            self.console.show_success(f"Credential for {website} saved successfully!")
            return credential
        except Exception as e:
            self.console.show_error(f"Failed to save: {str(e)}")
            return None
    
    def edit_credential(self, credential: Credential) -> bool:
        """Edit an existing credential."""
        self.console.clear()
        self.console.show_header(f"{ICONS['edit']} Edit Credential")
        
        self.console.print(f"[{self.theme.muted}]Press Enter to keep current value[/]\n")
        
        website = self.console.prompt(f"{ICONS['website']} Website", default=credential.website)
        username = self.console.prompt(f"{ICONS['user']} Username", default=credential.username)
        
        if self.console.confirm("Change password?"):
            password = self.console.prompt(f"{ICONS['password']} New password", password=True)
            if password:
                encrypted_pw = self.security.encrypt(password)
            else:
                encrypted_pw = credential.encrypted_password
        else:
            encrypted_pw = credential.encrypted_password
        
        notes = self.console.prompt(f"{ICONS['info']} Notes", default=credential.notes)
        
        credential.website = website
        credential.username = username
        credential.encrypted_password = encrypted_pw
        credential.notes = notes
        
        if self.db.update_credential(credential):
            self.console.show_success("Credential updated successfully!")
            return True
        else:
            self.console.show_error("Failed to update credential")
            return False
    
    def delete_credential(self, credential: Credential) -> bool:
        """Delete a credential with confirmation."""
        modal = ConfirmationModal(self.console)
        
        if modal.show(
            "Delete Credential",
            f"Are you sure you want to delete the credential for {credential.website}?",
            dangerous=True
        ):
            if self.db.delete_credential(credential.id):
                self.console.show_success(f"Credential for {credential.website} deleted")
                return True
            else:
                self.console.show_error("Failed to delete credential")
        
        return False
    
    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            self.console.show_success("Password copied to clipboard!")
            self.console.show_warning("Clipboard will be cleared in 30 seconds")
            
            # Auto-clear clipboard (simplified - would need threading for background)
            import threading
            def clear_clipboard():
                import time
                time.sleep(30)
                try:
                    pyperclip.copy('')
                except:
                    pass
            
            t = threading.Thread(target=clear_clipboard, daemon=True)
            t.start()
        except ImportError:
            self.console.show_warning("pyperclip not installed. Install with: pip install pyperclip")
