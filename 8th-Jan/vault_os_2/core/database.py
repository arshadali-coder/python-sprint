"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        DATABASE MODULE                                        ║
║              SQLite Storage with Encrypted Credentials                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
import json


@dataclass
class Credential:
    """Represents a stored credential."""
    id: Optional[int]
    website: str
    username: str
    encrypted_password: str
    notes: str
    category: str
    created_at: str
    last_updated: str
    last_accessed: Optional[str]
    access_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass 
class ActivityLog:
    """Represents an activity log entry."""
    id: Optional[int]
    action: str
    target: str
    details: str
    timestamp: str


class VaultDatabase:
    """SQLite database manager for the password vault."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._connection is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Credentials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                notes TEXT DEFAULT '',
                category TEXT DEFAULT 'General',
                created_at TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0,
                UNIQUE(website, username)
            )
        ''')
        
        # Activity logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                target TEXT NOT NULL,
                details TEXT DEFAULT '',
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                icon TEXT DEFAULT '📁',
                color TEXT DEFAULT 'white'
            )
        ''')
        
        # Insert default categories
        default_categories = [
            ('General', '📁', 'white'),
            ('Social Media', '💬', 'cyan'),
            ('Finance', '💰', 'green'),
            ('Work', '💼', 'blue'),
            ('Gaming', '🎮', 'magenta'),
            ('Shopping', '🛒', 'yellow'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO categories (name, icon, color) VALUES (?, ?, ?)
        ''', default_categories)
        
        conn.commit()
    
    def add_credential(self, credential: Credential) -> int:
        """Add a new credential to the vault."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO credentials 
            (website, username, encrypted_password, notes, category, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            credential.website,
            credential.username,
            credential.encrypted_password,
            credential.notes,
            credential.category,
            now,
            now
        ))
        
        conn.commit()
        credential_id = cursor.lastrowid
        
        self._log_activity('ADD', f'{credential.website}', f'Added credential for {credential.username}')
        
        return credential_id
    
    def get_credential(self, credential_id: int) -> Optional[Credential]:
        """Get a credential by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM credentials WHERE id = ?', (credential_id,))
        row = cursor.fetchone()
        
        if row:
            # Update access tracking
            now = datetime.now().isoformat()
            cursor.execute('''
                UPDATE credentials 
                SET last_accessed = ?, access_count = access_count + 1 
                WHERE id = ?
            ''', (now, credential_id))
            conn.commit()
            
            return Credential(
                id=row['id'],
                website=row['website'],
                username=row['username'],
                encrypted_password=row['encrypted_password'],
                notes=row['notes'],
                category=row['category'],
                created_at=row['created_at'],
                last_updated=row['last_updated'],
                last_accessed=row['last_accessed'],
                access_count=row['access_count']
            )
        return None
    
    def get_all_credentials(self) -> List[Credential]:
        """Get all credentials."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM credentials ORDER BY website ASC')
        rows = cursor.fetchall()
        
        return [Credential(
            id=row['id'],
            website=row['website'],
            username=row['username'],
            encrypted_password=row['encrypted_password'],
            notes=row['notes'],
            category=row['category'],
            created_at=row['created_at'],
            last_updated=row['last_updated'],
            last_accessed=row['last_accessed'],
            access_count=row['access_count']
        ) for row in rows]
    
    def search_credentials(self, query: str) -> List[Credential]:
        """Search credentials by website or username."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        search_pattern = f'%{query}%'
        cursor.execute('''
            SELECT * FROM credentials 
            WHERE website LIKE ? OR username LIKE ? OR category LIKE ?
            ORDER BY website ASC
        ''', (search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        
        return [Credential(
            id=row['id'],
            website=row['website'],
            username=row['username'],
            encrypted_password=row['encrypted_password'],
            notes=row['notes'],
            category=row['category'],
            created_at=row['created_at'],
            last_updated=row['last_updated'],
            last_accessed=row['last_accessed'],
            access_count=row['access_count']
        ) for row in rows]
    
    def update_credential(self, credential: Credential) -> bool:
        """Update an existing credential."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE credentials 
            SET website = ?, username = ?, encrypted_password = ?, 
                notes = ?, category = ?, last_updated = ?
            WHERE id = ?
        ''', (
            credential.website,
            credential.username,
            credential.encrypted_password,
            credential.notes,
            credential.category,
            now,
            credential.id
        ))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            self._log_activity('EDIT', f'{credential.website}', f'Updated credential for {credential.username}')
            return True
        return False
    
    def delete_credential(self, credential_id: int) -> bool:
        """Delete a credential by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get info for logging before deletion
        cursor.execute('SELECT website, username FROM credentials WHERE id = ?', (credential_id,))
        row = cursor.fetchone()
        
        if row:
            cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
            conn.commit()
            self._log_activity('DELETE', row['website'], f'Deleted credential for {row["username"]}')
            return True
        return False
    
    def get_credential_count(self) -> int:
        """Get total number of stored credentials."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM credentials')
        return cursor.fetchone()[0]
    
    def get_last_modified_credential(self) -> Optional[Credential]:
        """Get the most recently modified credential."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM credentials ORDER BY last_updated DESC LIMIT 1')
        row = cursor.fetchone()
        
        if row:
            return Credential(
                id=row['id'],
                website=row['website'],
                username=row['username'],
                encrypted_password=row['encrypted_password'],
                notes=row['notes'],
                category=row['category'],
                created_at=row['created_at'],
                last_updated=row['last_updated'],
                last_accessed=row['last_accessed'],
                access_count=row['access_count']
            )
        return None
    
    def get_credentials_by_category(self, category: str) -> List[Credential]:
        """Get credentials filtered by category."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM credentials WHERE category = ? ORDER BY website ASC', (category,))
        rows = cursor.fetchall()
        
        return [Credential(
            id=row['id'],
            website=row['website'],
            username=row['username'],
            encrypted_password=row['encrypted_password'],
            notes=row['notes'],
            category=row['category'],
            created_at=row['created_at'],
            last_updated=row['last_updated'],
            last_accessed=row['last_accessed'],
            access_count=row['access_count']
        ) for row in rows]
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all categories with their credential counts."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.name, c.icon, c.color, COUNT(cr.id) as count
            FROM categories c
            LEFT JOIN credentials cr ON c.name = cr.category
            GROUP BY c.name
            ORDER BY c.name
        ''')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def _log_activity(self, action: str, target: str, details: str = ''):
        """Log an activity (never logs actual passwords)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO activity_logs (action, target, details, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (action, target, details, now))
        
        conn.commit()
    
    def get_activity_logs(self, limit: int = 50) -> List[ActivityLog]:
        """Get recent activity logs."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
        return [ActivityLog(
            id=row['id'],
            action=row['action'],
            target=row['target'],
            details=row['details'],
            timestamp=row['timestamp']
        ) for row in rows]
    
    def get_setting(self, key: str, default: str = '') -> str:
        """Get a setting value."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        
        return row['value'] if row else default
    
    def set_setting(self, key: str, value: str):
        """Set a setting value."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        
        conn.commit()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get vault statistics."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total credentials
        cursor.execute('SELECT COUNT(*) FROM credentials')
        stats['total_credentials'] = cursor.fetchone()[0]
        
        # By category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM credentials 
            GROUP BY category
        ''')
        stats['by_category'] = {row['category']: row['count'] for row in cursor.fetchall()}
        
        # Most accessed
        cursor.execute('''
            SELECT website, username, access_count 
            FROM credentials 
            ORDER BY access_count DESC 
            LIMIT 5
        ''')
        stats['most_accessed'] = [dict(row) for row in cursor.fetchall()]
        
        # Recently added
        cursor.execute('''
            SELECT website, username, created_at 
            FROM credentials 
            ORDER BY created_at DESC 
            LIMIT 5
        ''')
        stats['recently_added'] = [dict(row) for row in cursor.fetchall()]
        
        return stats
    
    def export_vault(self, security_manager, export_password: str) -> str:
        """Export vault as encrypted JSON."""
        from .security import SecurityManager
        
        credentials = self.get_all_credentials()
        
        # Decrypt all passwords first, then re-encrypt with export password
        export_data = []
        for cred in credentials:
            try:
                decrypted_pw = security_manager.decrypt(cred.encrypted_password)
                export_data.append({
                    'website': cred.website,
                    'username': cred.username,
                    'password': decrypted_pw,  # Will be encrypted below
                    'notes': cred.notes,
                    'category': cred.category,
                    'created_at': cred.created_at,
                })
            except:
                continue
        
        # Encrypt export with export password
        import base64
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import secrets
        
        salt = secrets.token_bytes(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(export_password.encode()))
        fernet = Fernet(key)
        
        json_data = json.dumps(export_data)
        encrypted = fernet.encrypt(json_data.encode())
        
        # Combine salt and encrypted data
        combined = base64.urlsafe_b64encode(salt + encrypted).decode()
        
        self._log_activity('EXPORT', 'Vault', f'Exported {len(export_data)} credentials')
        
        return combined
    
    def import_vault(self, security_manager, encrypted_data: str, import_password: str) -> int:
        """Import credentials from encrypted export."""
        import base64
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        # Decode and split salt from data
        combined = base64.urlsafe_b64decode(encrypted_data.encode())
        salt = combined[:32]
        encrypted = combined[32:]
        
        # Derive key and decrypt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(import_password.encode()))
        fernet = Fernet(key)
        
        decrypted = fernet.decrypt(encrypted)
        import_data = json.loads(decrypted.decode())
        
        # Import credentials
        imported_count = 0
        for item in import_data:
            try:
                # Re-encrypt password with vault's key
                encrypted_pw = security_manager.encrypt(item['password'])
                
                cred = Credential(
                    id=None,
                    website=item['website'],
                    username=item['username'],
                    encrypted_password=encrypted_pw,
                    notes=item.get('notes', ''),
                    category=item.get('category', 'General'),
                    created_at=item.get('created_at', datetime.now().isoformat()),
                    last_updated=datetime.now().isoformat(),
                    last_accessed=None,
                    access_count=0
                )
                
                self.add_credential(cred)
                imported_count += 1
            except:
                continue
        
        self._log_activity('IMPORT', 'Vault', f'Imported {imported_count} credentials')
        
        return imported_count
    
    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
