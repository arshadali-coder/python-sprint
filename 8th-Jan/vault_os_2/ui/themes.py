"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           THEME MODULE                                        ║
║                      Colors, Styles, and Aesthetics                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

from rich.theme import Theme
from rich.style import Style
from dataclasses import dataclass
from typing import Dict


@dataclass
class VaultTheme:
    """Theme configuration for Vault OS."""
    name: str
    primary: str
    secondary: str
    accent: str
    success: str
    warning: str
    error: str
    info: str
    background: str
    surface: str
    text: str
    muted: str
    border: str
    

# Dark Cyber Theme - Default
CYBER_DARK = VaultTheme(
    name="Cyber Dark",
    primary="#00d4ff",       # Cyan
    secondary="#7c3aed",     # Purple
    accent="#f59e0b",        # Amber
    success="#10b981",       # Emerald
    warning="#f59e0b",       # Amber
    error="#ef4444",         # Red
    info="#3b82f6",          # Blue
    background="#0a0a0f",    # Near black
    surface="#1a1a2e",       # Dark blue-gray
    text="#e4e4e7",          # Light gray
    muted="#71717a",         # Gray
    border="#27272a",        # Dark gray
)

# Neon Matrix Theme
NEON_MATRIX = VaultTheme(
    name="Neon Matrix",
    primary="#00ff00",       # Matrix green
    secondary="#00cc00",     # Darker green
    accent="#00ff88",        # Mint
    success="#00ff00",       # Green
    warning="#ffff00",       # Yellow
    error="#ff0000",         # Red
    info="#00ffff",          # Cyan
    background="#000000",    # Black
    surface="#001100",       # Very dark green
    text="#00ff00",          # Green
    muted="#006600",         # Dark green
    border="#003300",        # Border green
)

# Ocean Depth Theme
OCEAN_DEPTH = VaultTheme(
    name="Ocean Depth",
    primary="#06b6d4",       # Cyan
    secondary="#0ea5e9",     # Sky blue
    accent="#8b5cf6",        # Violet
    success="#22c55e",       # Green
    warning="#eab308",       # Yellow
    error="#f43f5e",         # Rose
    info="#0ea5e9",          # Sky
    background="#0c1222",    # Deep blue
    surface="#162032",       # Navy
    text="#e2e8f0",          # Slate
    muted="#64748b",         # Slate gray
    border="#1e3a5f",        # Blue border
)

# Sunset Glow Theme
SUNSET_GLOW = VaultTheme(
    name="Sunset Glow",
    primary="#f97316",       # Orange
    secondary="#ec4899",     # Pink
    accent="#fbbf24",        # Amber
    success="#22c55e",       # Green
    warning="#f59e0b",       # Amber
    error="#dc2626",         # Red
    info="#8b5cf6",          # Violet
    background="#1c1917",    # Stone dark
    surface="#292524",       # Stone
    text="#fafaf9",          # Stone light
    muted="#78716c",         # Stone gray
    border="#44403c",        # Stone border
)

# Light Mode Theme
LIGHT_MODE = VaultTheme(
    name="Light Mode",
    primary="#2563eb",       # Blue
    secondary="#7c3aed",     # Purple
    accent="#0891b2",        # Cyan
    success="#16a34a",       # Green
    warning="#ca8a04",       # Yellow
    error="#dc2626",         # Red
    info="#0284c7",          # Sky
    background="#ffffff",    # White
    surface="#f4f4f5",       # Zinc light
    text="#18181b",          # Zinc dark
    muted="#71717a",         # Zinc gray
    border="#d4d4d8",        # Zinc border
)

# Available themes
THEMES: Dict[str, VaultTheme] = {
    "cyber_dark": CYBER_DARK,
    "neon_matrix": NEON_MATRIX,
    "ocean_depth": OCEAN_DEPTH,
    "sunset_glow": SUNSET_GLOW,
    "light_mode": LIGHT_MODE,
}


def get_rich_theme(vault_theme: VaultTheme) -> Theme:
    """Convert VaultTheme to Rich Theme."""
    return Theme({
        "primary": Style(color=vault_theme.primary, bold=True),
        "secondary": Style(color=vault_theme.secondary),
        "accent": Style(color=vault_theme.accent),
        "success": Style(color=vault_theme.success),
        "warning": Style(color=vault_theme.warning),
        "error": Style(color=vault_theme.error, bold=True),
        "info": Style(color=vault_theme.info),
        "muted": Style(color=vault_theme.muted),
        "title": Style(color=vault_theme.primary, bold=True),
        "subtitle": Style(color=vault_theme.secondary, italic=True),
        "highlight": Style(color=vault_theme.accent, bold=True),
        "panel.border": Style(color=vault_theme.border),
        "table.header": Style(color=vault_theme.primary, bold=True),
        "progress.percentage": Style(color=vault_theme.accent),
        "progress.bar.complete": Style(color=vault_theme.success),
        "prompt": Style(color=vault_theme.primary),
        "password": Style(color=vault_theme.warning),
        "danger": Style(color=vault_theme.error, bold=True),
        "locked": Style(color=vault_theme.error),
        "unlocked": Style(color=vault_theme.success),
    })


# ASCII Art for different screens
ASCII_LOGO = """
██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗     ██████╗ ███████╗
██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝    ██╔═══██╗██╔════╝
██║   ██║███████║██║   ██║██║     ██║       ██║   ██║███████╗
╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║       ██║   ██║╚════██║
 ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║       ╚██████╔╝███████║
  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝        ╚═════╝ ╚══════╝
                         ╔═════════════════════╗
                         ║    VERSION 2.0      ║
                         ╚═════════════════════╝
"""

ASCII_LOCK = """
    ╔═══════════╗
    ║   ┌───┐   ║
    ║   │ 🔒│   ║
    ║   └───┘   ║
    ║  ┌─────┐  ║
    ║  │█████│  ║
    ║  │█████│  ║
    ║  └─────┘  ║
    ╚═══════════╝
"""

ASCII_UNLOCK = """
    ╔═══════════╗
    ║  ┌───┐    ║
    ║  │ 🔓│    ║
    ║  └───┘    ║
    ║  ┌─────┐  ║
    ║  │░░░░░│  ║
    ║  │░░░░░│  ║
    ║  └─────┘  ║
    ╚═══════════╝
"""

ASCII_SHIELD = """
       ╱╲
      ╱  ╲
     ╱ 🛡️ ╲
    ╱──────╲
    │      │
    │ SAFE │
    │      │
    ╲      ╱
     ╲    ╱
      ╲  ╱
       ╲╱
"""

ASCII_KEY = """
    ┌─────────────┐
    │    ◯◯◯     │
    │  ╔═══╗     │
    │  ║ 🔑║═════│
    │  ╚═══╝     │
    │            │
    └─────────────┘
"""

# Box drawing characters
BOX_CHARS = {
    'top_left': '╔',
    'top_right': '╗',
    'bottom_left': '╚',
    'bottom_right': '╝',
    'horizontal': '═',
    'vertical': '║',
    'cross': '╬',
    'tee_left': '╠',
    'tee_right': '╣',
    'tee_top': '╦',
    'tee_bottom': '╩',
}

# Status icons
ICONS = {
    'vault': '🔐',
    'key': '🔑',
    'lock': '🔒',
    'unlock': '🔓',
    'shield': '🛡️',
    'warning': '⚠️',
    'error': '❌',
    'success': '✅',
    'info': 'ℹ️',
    'search': '🔍',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'copy': '📋',
    'export': '📤',
    'import': '📥',
    'settings': '⚙️',
    'logout': '🚪',
    'user': '👤',
    'website': '🌐',
    'password': '🔐',
    'time': '⏰',
    'folder': '📁',
    'star': '⭐',
    'rocket': '🚀',
    'fire': '🔥',
    'check': '✓',
    'cross': '✗',
    'arrow_right': '→',
    'arrow_left': '←',
    'arrow_up': '↑',
    'arrow_down': '↓',
    'bullet': '•',
    'diamond': '◆',
    'circle': '●',
    'square': '■',
    'heart': '❤️',
    'lightning': '⚡',
    'clock': '🕐',
    'calendar': '📅',
    'chart': '📊',
    'gear': '⚙️',
    'bell': '🔔',
    'home': '🏠',
    'terminal': '💻',
    'database': '🗄️',
    'audit': '📋',
    'health': '💚',
    'weak': '💔',
    'strong': '💪',
}

# Loading messages
LOADING_MESSAGES = [
    "Initializing security protocols...",
    "Establishing encrypted connection...",
    "Loading vault contents...",
    "Decrypting credentials...",
    "Verifying integrity...",
    "Preparing secure environment...",
]

# Fun facts while loading
FUN_FACTS = [
    "💡 Did you know? A 12-character password takes 62 trillion times longer to crack than a 6-character one.",
    "🔐 Pro tip: Use a unique password for every account.",
    "🛡️ Fun fact: The first computer password was created in 1961 at MIT.",
    "⚡ Security tip: Enable 2FA wherever possible.",
    "🔑 Remember: A passphrase like 'correct-horse-battery-staple' is secure AND memorable!",
    "💪 Strong passwords combine length, complexity, and uniqueness.",
    "🎯 The average person has 100+ online accounts. That's a lot of passwords!",
    "🌐 Tip: Never use personal info in passwords - it's often publicly available.",
]

# Strength colors
STRENGTH_COLORS = {
    'Critical': 'red',
    'Weak': 'red3',
    'Fair': 'yellow',
    'Good': 'green3',
    'Excellent': 'green',
}

# Strength bars
STRENGTH_BARS = {
    'Critical': '▓░░░░',
    'Weak': '▓▓░░░',
    'Fair': '▓▓▓░░',
    'Good': '▓▓▓▓░',
    'Excellent': '▓▓▓▓▓',
}
