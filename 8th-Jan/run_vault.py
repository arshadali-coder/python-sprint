#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              VAULT OS 2.0                                     ║
║                    Next-Generation Password Manager                           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Run this file to start Vault OS 2.0
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vault_os_2.app import main

if __name__ == "__main__":
    main()
