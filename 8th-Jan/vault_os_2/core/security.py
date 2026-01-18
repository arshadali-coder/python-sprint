"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        SECURITY MODULE                                        ║
║              Master Password, Encryption, and Session Management              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import secrets
import base64
import time
import threading
from pathlib import Path
from typing import Optional, Tuple
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityManager:
    """Handles all security operations: hashing, encryption, session management."""
    
    PBKDF2_ITERATIONS = 480000  # High iteration count for security
    SALT_SIZE = 32
    AUTO_LOCK_TIMEOUT = 300  # 5 minutes default
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.master_hash_file = data_dir / "master.hash"
        self.salt_file = data_dir / "master.salt"
        self._fernet: Optional[Fernet] = None
        self._session_active = False
        self._last_activity = time.time()
        self._lock_timeout = self.AUTO_LOCK_TIMEOUT
        self._lock_timer: Optional[threading.Timer] = None
        self._on_lock_callback = None
        
    def set_lock_callback(self, callback):
        """Set callback function to be called when vault auto-locks."""
        self._on_lock_callback = callback
        
    def set_lock_timeout(self, seconds: int):
        """Set auto-lock timeout in seconds."""
        self._lock_timeout = max(60, seconds)  # Minimum 1 minute
        
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash password with salt using SHA-512."""
        combined = salt + password.encode()
        return hashlib.sha512(combined).hexdigest()
    
    def is_vault_initialized(self) -> bool:
        """Check if master password has been set up."""
        return self.master_hash_file.exists() and self.salt_file.exists()
    
    def create_master_password(self, password: str) -> bool:
        """Create and store master password hash."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Generate salt
        salt = secrets.token_bytes(self.SALT_SIZE)
        
        # Hash password
        password_hash = self._hash_password(password, salt)
        
        # Store salt and hash
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.salt_file.write_bytes(salt)
        self.master_hash_file.write_text(password_hash)
        
        # Initialize session
        self._initialize_session(password, salt)
        
        return True
    
    def verify_master_password(self, password: str) -> bool:
        """Verify master password against stored hash."""
        if not self.is_vault_initialized():
            return False
        
        salt = self.salt_file.read_bytes()
        stored_hash = self.master_hash_file.read_text()
        
        computed_hash = self._hash_password(password, salt)
        
        if secrets.compare_digest(computed_hash, stored_hash):
            self._initialize_session(password, salt)
            return True
        return False
    
    def _initialize_session(self, password: str, salt: bytes):
        """Initialize an authenticated session."""
        key = self._derive_key(password, salt)
        self._fernet = Fernet(key)
        self._session_active = True
        self._last_activity = time.time()
        self._start_lock_timer()
    
    def _start_lock_timer(self):
        """Start or reset the auto-lock timer."""
        if self._lock_timer:
            self._lock_timer.cancel()
        
        self._lock_timer = threading.Timer(self._lock_timeout, self._auto_lock)
        self._lock_timer.daemon = True
        self._lock_timer.start()
    
    def _auto_lock(self):
        """Auto-lock the vault after inactivity."""
        if self._session_active:
            self.lock_vault()
            if self._on_lock_callback:
                self._on_lock_callback()
    
    def refresh_activity(self):
        """Refresh last activity time to prevent auto-lock."""
        if self._session_active:
            self._last_activity = time.time()
            self._start_lock_timer()
    
    def lock_vault(self):
        """Lock the vault and clear sensitive data."""
        self._fernet = None
        self._session_active = False
        if self._lock_timer:
            self._lock_timer.cancel()
            self._lock_timer = None
    
    def is_unlocked(self) -> bool:
        """Check if vault is currently unlocked."""
        return self._session_active and self._fernet is not None
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext data."""
        if not self._fernet:
            raise RuntimeError("Vault is locked")
        self.refresh_activity()
        encrypted = self._fernet.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext data."""
        if not self._fernet:
            raise RuntimeError("Vault is locked")
        self.refresh_activity()
        try:
            encrypted = base64.urlsafe_b64decode(ciphertext.encode())
            decrypted = self._fernet.decrypt(encrypted)
            return decrypted.decode()
        except (InvalidToken, Exception):
            raise ValueError("Decryption failed - data may be corrupted")
    
    def change_master_password(self, old_password: str, new_password: str) -> bool:
        """Change master password and re-encrypt all data."""
        if not self.verify_master_password(old_password):
            return False
        
        if len(new_password) < 8:
            raise ValueError("New password must be at least 8 characters")
        
        # Generate new salt
        new_salt = secrets.token_bytes(self.SALT_SIZE)
        new_hash = self._hash_password(new_password, new_salt)
        
        # Store new credentials
        self.salt_file.write_bytes(new_salt)
        self.master_hash_file.write_text(new_hash)
        
        # Re-initialize session with new password
        self._initialize_session(new_password, new_salt)
        
        return True
    
    def get_time_until_lock(self) -> int:
        """Get seconds until auto-lock."""
        if not self._session_active:
            return 0
        elapsed = time.time() - self._last_activity
        remaining = max(0, self._lock_timeout - elapsed)
        return int(remaining)


class PasswordGenerator:
    """Secure password generation with customizable options."""
    
    LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    DIGITS = "0123456789"
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @classmethod
    def generate(
        cls,
        length: int = 16,
        include_uppercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """Generate a secure random password."""
        chars = cls.LOWERCASE
        
        if include_uppercase:
            chars += cls.UPPERCASE
        if include_digits:
            chars += cls.DIGITS
        if include_symbols:
            chars += cls.SYMBOLS
        
        if exclude_ambiguous:
            ambiguous = "0O1lI|"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # Ensure minimum complexity
        password = []
        if include_uppercase:
            password.append(secrets.choice(cls.UPPERCASE))
        if include_digits:
            password.append(secrets.choice(cls.DIGITS))
        if include_symbols:
            password.append(secrets.choice(cls.SYMBOLS))
        password.append(secrets.choice(cls.LOWERCASE))
        
        # Fill remaining length
        remaining = length - len(password)
        password.extend(secrets.choice(chars) for _ in range(remaining))
        
        # Shuffle
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        return ''.join(password_list)
    
    @classmethod
    def analyze_strength(cls, password: str) -> Tuple[int, str, list]:
        """
        Analyze password strength.
        Returns: (score 0-100, rating, list of issues)
        """
        score = 0
        issues = []
        
        # Length scoring
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 20
        elif length >= 8:
            score += 10
        else:
            issues.append("Too short (min 8 characters)")
        
        # Character diversity
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in cls.SYMBOLS for c in password)
        
        diversity = sum([has_lower, has_upper, has_digit, has_symbol])
        score += diversity * 15
        
        if not has_upper:
            issues.append("Add uppercase letters")
        if not has_digit:
            issues.append("Add numbers")
        if not has_symbol:
            issues.append("Add special characters")
        
        # Pattern detection
        common_patterns = ['123', 'abc', 'qwerty', 'password', 'admin']
        if any(p in password.lower() for p in common_patterns):
            score -= 20
            issues.append("Contains common patterns")
        
        # Repeated characters
        if any(password.count(c) > 3 for c in set(password)):
            score -= 10
            issues.append("Too many repeated characters")
        
        # Determine rating
        score = max(0, min(100, score))
        
        if score >= 80:
            rating = "Excellent"
        elif score >= 60:
            rating = "Good"
        elif score >= 40:
            rating = "Fair"
        elif score >= 20:
            rating = "Weak"
        else:
            rating = "Critical"
        
        return score, rating, issues
