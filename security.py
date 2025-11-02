"""
Security utilities for the FinTech application.
Handles encryption, hashing, session management, and security validations.
"""

import bcrypt
import secrets
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, Any
import streamlit as st
from config import BCRYPT_ROUNDS, SESSION_TIMEOUT_MINUTES, MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES


class SecurityManager:
    """Handles all security-related operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt with salt.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password (str): Plain text password
            hashed (str): Hashed password from database
            
        Returns:
            bool: True if password matches
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    @staticmethod
    def generate_encryption_key() -> bytes:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            bytes: Encryption key
        """
        return Fernet.generate_key()
    
    @staticmethod
    def encrypt_data(data: str, key: bytes) -> str:
        """
        Encrypt data using Fernet symmetric encryption.
        
        Args:
            data (str): Data to encrypt
            key (bytes): Encryption key
            
        Returns:
            str: Encrypted data as string
        """
        try:
            f = Fernet(key)
            return f.encrypt(data.encode()).decode()
        except Exception:
            raise ValueError("Encryption failed")
    
    @staticmethod
    def decrypt_data(encrypted_data: str, key: bytes) -> str:
        """
        Decrypt data using Fernet symmetric encryption.
        
        Args:
            encrypted_data (str): Encrypted data
            key (bytes): Encryption key
            
        Returns:
            str: Decrypted data
        """
        try:
            f = Fernet(key)
            return f.decrypt(encrypted_data.encode()).decode()
        except Exception:
            raise ValueError("Decryption failed")
    
    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a secure session token.
        
        Returns:
            str: URL-safe session token
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_transaction_id() -> str:
        """
        Generate a unique transaction ID.
        
        Returns:
            str: Transaction ID
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = secrets.token_hex(8)
        return f"TXN{timestamp}{random_part.upper()}"
    
    @staticmethod
    def hash_file_content(content: bytes) -> str:
        """
        Generate SHA-256 hash of file content.
        
        Args:
            content (bytes): File content
            
        Returns:
            str: SHA-256 hash
        """
        return hashlib.sha256(content).hexdigest()


class SessionManager:
    """Manages user sessions and authentication state"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'session_token' not in st.session_state:
            st.session_state.session_token = None
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = None
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = {}
        if 'lockout_until' not in st.session_state:
            st.session_state.lockout_until = {}
    
    @staticmethod
    def create_session(username: str, user_id: int) -> str:
        """
        Create a new user session.
        
        Args:
            username (str): Username
            user_id (int): User ID
            
        Returns:
            str: Session token
        """
        session_token = SecurityManager.generate_session_token()
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user_id
        st.session_state.session_token = session_token
        st.session_state.last_activity = datetime.now()
        
        # Clear login attempts on successful login
        if username in st.session_state.login_attempts:
            del st.session_state.login_attempts[username]
        if username in st.session_state.lockout_until:
            del st.session_state.lockout_until[username]
        
        return session_token
    
    @staticmethod
    def update_activity():
        """Update last activity timestamp"""
        if st.session_state.logged_in:
            st.session_state.last_activity = datetime.now()
    
    @staticmethod
    def is_session_valid() -> bool:
        """
        Check if current session is valid.
        
        Returns:
            bool: True if session is valid
        """
        if not st.session_state.logged_in:
            return False
        
        if not st.session_state.last_activity:
            return False
        
        # Check session timeout
        timeout_threshold = datetime.now() - timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        if st.session_state.last_activity < timeout_threshold:
            SessionManager.destroy_session()
            return False
        
        return True
    
    @staticmethod
    def destroy_session():
        """Destroy current session"""
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_id = None
        st.session_state.session_token = None
        st.session_state.last_activity = None
    
    @staticmethod
    def record_login_attempt(username: str, success: bool):
        """
        Record login attempt for rate limiting.
        
        Args:
            username (str): Username
            success (bool): Whether login was successful
        """
        if success:
            # Clear attempts on successful login
            if username in st.session_state.login_attempts:
                del st.session_state.login_attempts[username]
            return
        
        # Record failed attempt
        if username not in st.session_state.login_attempts:
            st.session_state.login_attempts[username] = 0
        
        st.session_state.login_attempts[username] += 1
        
        # Lock account if max attempts reached
        if st.session_state.login_attempts[username] >= MAX_LOGIN_ATTEMPTS:
            lockout_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            st.session_state.lockout_until[username] = lockout_until
    
    @staticmethod
    def is_account_locked(username: str) -> Tuple[bool, Optional[datetime]]:
        """
        Check if account is locked.
        
        Args:
            username (str): Username to check
            
        Returns:
            Tuple[bool, Optional[datetime]]: (is_locked, lockout_until)
        """
        if username not in st.session_state.lockout_until:
            return False, None
        
        lockout_until = st.session_state.lockout_until[username]
        if datetime.now() >= lockout_until:
            # Lockout expired, clear it
            del st.session_state.lockout_until[username]
            if username in st.session_state.login_attempts:
                del st.session_state.login_attempts[username]
            return False, None
        
        return True, lockout_until
    
    @staticmethod
    def get_remaining_attempts(username: str) -> int:
        """
        Get remaining login attempts for user.
        
        Args:
            username (str): Username
            
        Returns:
            int: Remaining attempts
        """
        attempts = st.session_state.login_attempts.get(username, 0)
        return max(0, MAX_LOGIN_ATTEMPTS - attempts)


class SecurityValidator:
    """Additional security validation utilities"""
    
    @staticmethod
    def is_safe_redirect_url(url: str) -> bool:
        """
        Validate redirect URL to prevent open redirect attacks.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL is safe
        """
        # Only allow relative URLs or same-origin URLs
        if url.startswith('/') and not url.startswith('//'):
            return True
        return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove directory traversal attempts
        filename = filename.replace('..', '').replace('/', '').replace('\\', '')
        # Generate random filename to prevent conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_part = secrets.token_hex(4)
        extension = filename.split('.')[-1] if '.' in filename else 'txt'
        return f"upload_{timestamp}_{random_part}.{extension}"
    
    @staticmethod
    def check_file_signature(content: bytes, expected_extension: str) -> bool:
        """
        Basic file signature validation.
        
        Args:
            content (bytes): File content
            expected_extension (str): Expected file extension
            
        Returns:
            bool: True if file signature matches extension
        """
        if len(content) < 4:
            return False
        
        # Basic signature checks
        signatures = {
            '.pdf': [b'%PDF'],
            '.jpg': [b'\xff\xd8\xff'],
            '.png': [b'\x89PNG'],
            '.txt': []  # Text files don't have specific signatures
        }
        
        if expected_extension not in signatures:
            return False
        
        if not signatures[expected_extension]:  # No signature required (like .txt)
            return True
        
        for signature in signatures[expected_extension]:
            if content.startswith(signature):
                return True
        
        return False