"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                          COMPONENTS MODULE                                    ║
║                    Reusable UI Components with Rich                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import time
import random
from typing import List, Optional, Tuple, Callable, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED, DOUBLE, MINIMAL
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.rule import Rule
from getpass import getpass

from .themes import (
    VaultTheme, CYBER_DARK, get_rich_theme, 
    ASCII_LOGO, ASCII_LOCK, ASCII_UNLOCK,
    ICONS, FUN_FACTS, STRENGTH_COLORS, STRENGTH_BARS
)


class VaultConsole:
    """Enhanced console with Vault OS theming."""
    
    def __init__(self, theme: VaultTheme = CYBER_DARK):
        self.theme = theme
        self.console = Console(theme=get_rich_theme(theme), force_terminal=True)
        self._width = min(self.console.width, 100)
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)
    
    def print_centered(self, text: str, style: str = "primary"):
        self.console.print(Align.center(Text(text, style=style)))
    
    def print_logo(self, animated: bool = True):
        if animated:
            for line in ASCII_LOGO.split('\n'):
                styled_line = Text(line, style=f"bold {self.theme.primary}")
                self.console.print(Align.center(styled_line))
                time.sleep(0.05)
        else:
            self.console.print(Align.center(Text(ASCII_LOGO, style=f"bold {self.theme.primary}")))
    
    def create_panel(self, content: Any, title: str = "", subtitle: str = "",
                     border_style: str = None, padding: Tuple[int, int] = (1, 2)) -> Panel:
        border = border_style or self.theme.primary
        return Panel(content, title=f"[bold {self.theme.primary}]{title}[/]" if title else None,
                    subtitle=f"[{self.theme.muted}]{subtitle}[/]" if subtitle else None,
                    border_style=border, box=ROUNDED, padding=padding)
    
    def create_table(self, title: str = "", columns: List[Tuple[str, str]] = None,
                    show_header: bool = True, expand: bool = True) -> Table:
        table = Table(title=f"[bold {self.theme.primary}]{title}[/]" if title else None,
                     show_header=show_header, expand=expand, border_style=self.theme.border,
                     header_style=f"bold {self.theme.primary}", box=ROUNDED)
        if columns:
            for name, style in columns:
                table.add_column(name, style=style)
        return table
    
    def show_loading(self, message: str = "Loading...", duration: float = 1.5, show_fact: bool = True):
        with Progress(SpinnerColumn("dots12", style=f"bold {self.theme.primary}"),
                     TextColumn(f"[{self.theme.secondary}]{message}"), console=self.console, transient=True) as progress:
            task = progress.add_task("", total=100)
            for _ in range(int(duration * 20)):
                time.sleep(duration / (duration * 20))
                progress.update(task, advance=5)
        if show_fact:
            self.print(f"\n[{self.theme.muted}]{random.choice(FUN_FACTS)}[/]\n")
    
    def show_spinner(self, message: str, duration: float = 1.0):
        with self.console.status(f"[{self.theme.secondary}]{message}", spinner="dots12",
                                spinner_style=f"bold {self.theme.primary}"):
            time.sleep(duration)
    
    def prompt(self, message: str, default: str = "", password: bool = False, choices: List[str] = None) -> str:
        prompt_text = f"[{self.theme.primary}]{ICONS.get('arrow_right', '>')}[/] [{self.theme.text}]{message}[/]"
        if password:
            self.console.print(prompt_text, end=" ")
            return getpass("")
        if choices:
            return Prompt.ask(prompt_text, choices=choices, default=default, console=self.console)
        return Prompt.ask(prompt_text, default=default, console=self.console)
    
    def confirm(self, message: str, default: bool = False) -> bool:
        prompt_text = f"[{self.theme.warning}]{ICONS.get('warning', '!')}[/] [{self.theme.text}]{message}[/]"
        return Confirm.ask(prompt_text, default=default, console=self.console)
    
    def show_success(self, message: str):
        self.console.print(f"\n[{self.theme.success}]{ICONS['success']} {message}[/]\n")
    
    def show_error(self, message: str):
        self.console.print(f"\n[{self.theme.error}]{ICONS['error']} {message}[/]\n")
    
    def show_warning(self, message: str):
        self.console.print(f"\n[{self.theme.warning}]{ICONS['warning']} {message}[/]\n")
    
    def show_info(self, message: str):
        self.console.print(f"\n[{self.theme.info}]{ICONS['info']} {message}[/]\n")
    
    def display_password_strength(self, score: int, rating: str, issues: List[str]):
        color = STRENGTH_COLORS.get(rating, 'white')
        bar = STRENGTH_BARS.get(rating, '░░░░░')
        strength_text = Text()
        strength_text.append(f"\n{ICONS['shield']} Strength: ", style=self.theme.text)
        strength_text.append(f"{rating} ", style=f"bold {color}")
        strength_text.append(f"[{bar}] ", style=color)
        strength_text.append(f"{score}/100", style=self.theme.muted)
        self.console.print(strength_text)
        if issues:
            self.console.print(f"\n[{self.theme.muted}]Suggestions:[/]")
            for issue in issues:
                self.console.print(f"  [{self.theme.warning}]•[/] {issue}")
    
    def show_header(self, title: str, subtitle: str = ""):
        self.console.print()
        self.console.print(Rule(f"[bold {self.theme.primary}]{title}[/]", style=self.theme.border))
        if subtitle:
            self.console.print(Align.center(Text(subtitle, style=self.theme.muted)))
        self.console.print()
    
    def show_divider(self, text: str = ""):
        self.console.print(Rule(f"[{self.theme.muted}]{text}[/]" if text else "", style=self.theme.border))
    
    def wait_for_key(self, message: str = "Press Enter to continue..."):
        self.console.print(f"\n[{self.theme.muted}]{message}[/]", end="")
        input()
    
    def show_lock_screen(self):
        self.clear()
        self.console.print(Align.center(Text(ASCII_LOCK, style=f"bold {self.theme.error}")))
        self.console.print()
        self.print_centered("VAULT LOCKED", style=f"bold {self.theme.error}")
    
    def show_unlock_animation(self):
        for frame, color in [(ASCII_LOCK, self.theme.error), (ASCII_UNLOCK, self.theme.success)]:
            self.clear()
            self.console.print(Align.center(Text(frame, style=f"bold {color}")))
            time.sleep(0.3)
        self.print_centered("VAULT UNLOCKED", style=f"bold {self.theme.success}")
        time.sleep(0.5)


class MenuSelector:
    def __init__(self, console: VaultConsole):
        self.console = console
        self.theme = console.theme
    
    def select(self, title: str, options: List[Tuple[str, str]], allow_cancel: bool = True) -> Optional[str]:
        self.console.show_header(title)
        for i, (value, display) in enumerate(options, 1):
            self.console.print(f"  [{self.theme.primary}][{i}][/] {display}")
        if allow_cancel:
            self.console.print(f"\n  [{self.theme.error}][0][/] Cancel")
        self.console.print()
        while True:
            try:
                choice = self.console.prompt("Select option")
                if choice == '0' and allow_cancel:
                    return None
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx][0]
                self.console.show_error("Invalid selection")
            except ValueError:
                self.console.show_error("Please enter a number")


class ConfirmationModal:
    def __init__(self, console: VaultConsole):
        self.console = console
        self.theme = console.theme
    
    def show(self, title: str, message: str, confirm_text: str = "Yes",
             cancel_text: str = "No", dangerous: bool = False) -> bool:
        border_color = self.theme.error if dangerous else self.theme.warning
        icon = ICONS['error'] if dangerous else ICONS['warning']
        content = Text()
        content.append(f"\n{icon} ", style="bold")
        content.append(message, style=self.theme.text)
        content.append("\n")
        panel = Panel(Align.center(content), title=f"[bold {border_color}]{title}[/]",
                     border_style=border_color, box=DOUBLE, padding=(1, 4))
        self.console.print()
        self.console.print(panel)
        self.console.print()
        self.console.print(f"  [{self.theme.success}][Y][/] {confirm_text}")
        self.console.print(f"  [{self.theme.error}][N][/] {cancel_text}")
        self.console.print()
        while True:
            choice = self.console.prompt("Confirm").strip().lower()
            if choice in ('y', 'yes'):
                return True
            if choice in ('n', 'no'):
                return False
            self.console.show_error("Please enter Y or N")


class StatusBar:
    def __init__(self, console: VaultConsole):
        self.console = console
        self.theme = console.theme
    
    def render(self, vault_status: str = "Unlocked", credential_count: int = 0,
               time_to_lock: int = 0, current_screen: str = "Dashboard") -> Panel:
        status_icon = ICONS['unlock'] if vault_status == "Unlocked" else ICONS['lock']
        status_color = self.theme.success if vault_status == "Unlocked" else self.theme.error
        left = Text()
        left.append(f"{status_icon} {vault_status}", style=f"bold {status_color}")
        left.append(f"  {ICONS['folder']} {credential_count} creds", style=self.theme.muted)
        center = Text(f"{ICONS['terminal']} {current_screen}", style=f"bold {self.theme.primary}")
        right = Text()
        if time_to_lock > 0:
            right.append(f"{ICONS['clock']} {time_to_lock // 60:02d}:{time_to_lock % 60:02d}", style=self.theme.warning)
        return Panel(Columns([left, center, right], expand=True, equal=True),
                    border_style=self.theme.border, box=MINIMAL, padding=(0, 1))
