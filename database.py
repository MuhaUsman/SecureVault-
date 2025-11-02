"""
Database operations for the secure FinTech application.
Handles all database interactions with security best practices.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from security import SecurityManager
from config import DATABASE_PATH, AUDIT_ACTIONS


class DatabaseManager:
    """Handles all database operations with security focus"""
    
    def __init__(self):
        """Initialize database manager and create tables if needed"""
        self.db_path = DATABASE_PATH
        self._ensure_data_directory()
        self._initialize_database()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection handling and cleanup.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)  # Add timeout
            conn.row_factory = sqlite3.Row  # Enable column access by name
            conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode for better concurrency
            conn.execute("PRAGMA synchronous=NORMAL")  # Improve performance
            conn.execute("PRAGMA cache_size=10000")  # Increase cache size
            conn.execute("PRAGMA temp_store=MEMORY")  # Use memory for temp storage
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP
                )
            """)
            
            # Wallets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    balance_encrypted TEXT NOT NULL,
                    encryption_key TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    amount_encrypted TEXT NOT NULL,
                    recipient_username TEXT,
                    source TEXT,
                    description_encrypted TEXT,
                    balance_after_encrypted TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Audit logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT DEFAULT '127.0.0.1',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'SUCCESS'
                )
            """)
            
            # File uploads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER,
                    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_hash TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            conn.commit()
    
    def create_user(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new user account.
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Plain text password
            
        Returns:
            Tuple[bool, str, Optional[int]]: (success, message, user_id)
        """
        try:
            # Hash password
            password_hash = SecurityManager.hash_password(password)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if username or email already exists
                cursor.execute(
                    "SELECT username, email FROM users WHERE username = ? OR email = ?",
                    (username, email)
                )
                existing = cursor.fetchone()
                
                if existing:
                    if existing['username'] == username:
                        self.log_audit_event(None, username, AUDIT_ACTIONS['REGISTER'], 
                                           f"Registration failed - username exists: {username}", 'FAILED')
                        return False, "Username already exists", None
                    else:
                        self.log_audit_event(None, username, AUDIT_ACTIONS['REGISTER'], 
                                           f"Registration failed - email exists: {email}", 'FAILED')
                        return False, "Email already exists", None
                
                # Create user
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash)
                    VALUES (?, ?, ?)
                """, (username, email, password_hash))
                
                user_id = cursor.lastrowid
                
                # Create wallet with initial balance of 0
                encryption_key = SecurityManager.generate_encryption_key()
                initial_balance = "0.00"
                encrypted_balance = SecurityManager.encrypt_data(initial_balance, encryption_key)
                
                cursor.execute("""
                    INSERT INTO wallets (user_id, balance_encrypted, encryption_key)
                    VALUES (?, ?, ?)
                """, (user_id, encrypted_balance, encryption_key.decode()))
                
                conn.commit()
                
                # Log successful registration
                self.log_audit_event(user_id, username, AUDIT_ACTIONS['REGISTER'], 
                                   f"User registered successfully: {username}")
                
                return True, "Account created successfully", user_id
                
        except sqlite3.IntegrityError as e:
            self.log_audit_event(None, username, AUDIT_ACTIONS['REGISTER'], 
                               f"Registration failed - integrity error: {str(e)}", 'FAILED')
            return False, "Registration failed. Please try again.", None
        except Exception as e:
            self.log_audit_event(None, username, AUDIT_ACTIONS['REGISTER'], 
                               f"Registration failed - error: {str(e)}", 'FAILED')
            return False, "An error occurred during registration", None
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user login.
        
        Args:
            username (str): Username or email
            password (str): Plain text password
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (success, message, user_data)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Find user by username or email
                cursor.execute("""
                    SELECT id, username, email, password_hash, is_active, failed_attempts, locked_until
                    FROM users 
                    WHERE username = ? OR email = ?
                """, (username, username))
                
                user = cursor.fetchone()
                
                if not user:
                    # Generic error message to prevent username enumeration
                    self.log_audit_event(None, username, AUDIT_ACTIONS['LOGIN_FAILED'], 
                                       f"Login failed - user not found: {username}", 'FAILED')
                    return False, "Invalid username or password", None
                
                if not user['is_active']:
                    self.log_audit_event(user['id'], user['username'], AUDIT_ACTIONS['LOGIN_FAILED'], 
                                       "Login failed - account inactive", 'FAILED')
                    return False, "Account is inactive", None
                
                # Check if account is locked
                if user['locked_until']:
                    locked_until = datetime.fromisoformat(user['locked_until'])
                    if datetime.now() < locked_until:
                        self.log_audit_event(user['id'], user['username'], AUDIT_ACTIONS['LOGIN_FAILED'], 
                                           "Login failed - account locked", 'FAILED')
                        return False, f"Account is locked until {locked_until.strftime('%H:%M:%S')}", None
                
                # Verify password
                if not SecurityManager.verify_password(password, user['password_hash']):
                    # Increment failed attempts
                    new_attempts = user['failed_attempts'] + 1
                    locked_until = None
                    
                    if new_attempts >= 5:  # Lock after 5 failed attempts
                        locked_until = datetime.now().replace(microsecond=0) + \
                                     datetime.timedelta(minutes=15)
                        cursor.execute("""
                            UPDATE users 
                            SET failed_attempts = ?, locked_until = ?
                            WHERE id = ?
                        """, (new_attempts, locked_until.isoformat(), user['id']))
                        
                        self.log_audit_event(user['id'], user['username'], AUDIT_ACTIONS['ACCOUNT_LOCKED'], 
                                           f"Account locked after {new_attempts} failed attempts")
                    else:
                        cursor.execute("""
                            UPDATE users 
                            SET failed_attempts = ?
                            WHERE id = ?
                        """, (new_attempts, user['id']))
                    
                    conn.commit()
                    
                    self.log_audit_event(user['id'], user['username'], AUDIT_ACTIONS['LOGIN_FAILED'], 
                                       f"Login failed - wrong password (attempt {new_attempts})", 'FAILED')
                    return False, "Invalid username or password", None
                
                # Successful login - reset failed attempts and update last login
                cursor.execute("""
                    UPDATE users 
                    SET failed_attempts = 0, locked_until = NULL, last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user['id'],))
                
                conn.commit()
                
                user_data = {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
                
                self.log_audit_event(user['id'], user['username'], AUDIT_ACTIONS['LOGIN_SUCCESS'], 
                                   "User logged in successfully")
                
                return True, "Login successful", user_data
                
        except Exception as e:
            self.log_audit_event(None, username, AUDIT_ACTIONS['LOGIN_FAILED'], 
                               f"Login failed - error: {str(e)}", 'FAILED')
            return False, "An error occurred during login", None
    
    def get_wallet_balance(self, user_id: int) -> Tuple[bool, float]:
        """
        Get user's wallet balance.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Tuple[bool, float]: (success, balance)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT balance_encrypted, encryption_key
                    FROM wallets
                    WHERE user_id = ?
                """, (user_id,))
                
                wallet = cursor.fetchone()
                
                if not wallet:
                    # Create wallet with initial balance of 0 if it doesn't exist
                    encryption_key = SecurityManager.generate_encryption_key()
                    initial_balance = "0.00"
                    encrypted_balance = SecurityManager.encrypt_data(initial_balance, encryption_key)
                    
                    cursor.execute("""
                        INSERT INTO wallets (user_id, balance_encrypted, encryption_key)
                        VALUES (?, ?, ?)
                    """, (user_id, encrypted_balance, encryption_key.decode()))
                    
                    conn.commit()
                    return True, 0.0
                
                # Decrypt balance
                encryption_key = wallet['encryption_key'].encode()
                decrypted_balance = SecurityManager.decrypt_data(
                    wallet['balance_encrypted'], encryption_key
                )
                
                return True, float(decrypted_balance)
                
        except Exception as e:
            print(f"Error getting wallet balance: {e}")  # Debug print
            return False, 0.0
    
    def update_wallet_balance(self, user_id: int, new_balance: float) -> bool:
        """
        Update user's wallet balance.
        
        Args:
            user_id (int): User ID
            new_balance (float): New balance amount
            
        Returns:
            bool: Success status
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get encryption key
                cursor.execute("""
                    SELECT encryption_key FROM wallets WHERE user_id = ?
                """, (user_id,))
                
                wallet = cursor.fetchone()
                if not wallet:
                    # Create wallet if it doesn't exist
                    encryption_key = SecurityManager.generate_encryption_key()
                    encrypted_balance = SecurityManager.encrypt_data(f"{new_balance:.2f}", encryption_key)
                    
                    cursor.execute("""
                        INSERT INTO wallets (user_id, balance_encrypted, encryption_key)
                        VALUES (?, ?, ?)
                    """, (user_id, encrypted_balance, encryption_key.decode()))
                else:
                    # Encrypt new balance
                    encryption_key = wallet['encryption_key'].encode()
                    encrypted_balance = SecurityManager.encrypt_data(
                        f"{new_balance:.2f}", encryption_key
                    )
                    
                    # Update balance
                    cursor.execute("""
                        UPDATE wallets 
                        SET balance_encrypted = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (encrypted_balance, user_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error updating wallet balance: {e}")  # Debug print
            return False
    
    def create_transaction(self, user_id: int, transaction_type: str, amount: float,
                          recipient_username: str = None, source: str = None,
                          description: str = None) -> Tuple[bool, str]:
        """
        Create a new transaction.
        
        Args:
            user_id (int): User ID
            transaction_type (str): 'CREDIT' or 'DEBIT'
            amount (float): Transaction amount
            recipient_username (str): Recipient username (for DEBIT)
            source (str): Source of funds (for CREDIT)
            description (str): Transaction description
            
        Returns:
            Tuple[bool, str]: (success, transaction_id or error_message)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Start transaction
                cursor.execute("BEGIN IMMEDIATE")
                
                # Get or create wallet
                cursor.execute("""
                    SELECT balance_encrypted, encryption_key FROM wallets WHERE user_id = ?
                """, (user_id,))
                
                wallet = cursor.fetchone()
                
                if not wallet:
                    # Create wallet with initial balance of 0
                    encryption_key = SecurityManager.generate_encryption_key()
                    initial_balance = "0.00"
                    encrypted_balance = SecurityManager.encrypt_data(initial_balance, encryption_key)
                    
                    cursor.execute("""
                        INSERT INTO wallets (user_id, balance_encrypted, encryption_key)
                        VALUES (?, ?, ?)
                    """, (user_id, encrypted_balance, encryption_key.decode()))
                    
                    current_balance = 0.0
                    encryption_key_bytes = encryption_key
                else:
                    # Decrypt current balance
                    encryption_key_bytes = wallet['encryption_key'].encode()
                    current_balance = float(SecurityManager.decrypt_data(
                        wallet['balance_encrypted'], encryption_key_bytes
                    ))
                
                # Calculate new balance
                if transaction_type == 'CREDIT':
                    new_balance = current_balance + amount
                elif transaction_type == 'DEBIT':
                    if current_balance < amount:
                        conn.rollback()
                        return False, "Insufficient funds"
                    new_balance = current_balance - amount
                else:
                    conn.rollback()
                    return False, "Invalid transaction type"
                
                # Generate transaction ID
                transaction_id = SecurityManager.generate_transaction_id()
                
                # Encrypt transaction data
                encrypted_amount = SecurityManager.encrypt_data(f"{amount:.2f}", encryption_key_bytes)
                encrypted_description = SecurityManager.encrypt_data(
                    description or "", encryption_key_bytes
                )
                encrypted_balance_after = SecurityManager.encrypt_data(
                    f"{new_balance:.2f}", encryption_key_bytes
                )
                
                # Create transaction record
                cursor.execute("""
                    INSERT INTO transactions (
                        transaction_id, user_id, type, amount_encrypted,
                        recipient_username, source, description_encrypted,
                        balance_after_encrypted
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    transaction_id, user_id, transaction_type, encrypted_amount,
                    recipient_username, source, encrypted_description,
                    encrypted_balance_after
                ))
                
                # Update wallet balance
                encrypted_new_balance = SecurityManager.encrypt_data(f"{new_balance:.2f}", encryption_key_bytes)
                cursor.execute("""
                    UPDATE wallets 
                    SET balance_encrypted = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (encrypted_new_balance, user_id))
                
                # Commit all changes
                conn.commit()
                
                # Log transaction (outside the main transaction to avoid locks)
                username = self.get_username_by_id(user_id)
                self.log_audit_event(user_id, username, AUDIT_ACTIONS['TRANSACTION_CREATE'], 
                                   f"Transaction created: {transaction_id} ({transaction_type} ${amount:.2f})")
                
                return True, transaction_id
                
        except Exception as e:
            print(f"Transaction error: {e}")  # Debug print
            return False, f"Transaction failed: {str(e)}"
    
    def get_user_transactions(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get user's transaction history.
        
        Args:
            user_id (int): User ID
            limit (int): Number of transactions to return
            offset (int): Offset for pagination
            
        Returns:
            List[Dict]: List of transaction records
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get encryption key
                cursor.execute("""
                    SELECT encryption_key FROM wallets WHERE user_id = ?
                """, (user_id,))
                
                wallet = cursor.fetchone()
                if not wallet:
                    return []
                
                encryption_key = wallet['encryption_key'].encode()
                
                # Get transactions
                cursor.execute("""
                    SELECT transaction_id, type, amount_encrypted, recipient_username,
                           source, description_encrypted, balance_after_encrypted, created_at
                    FROM transactions
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                """, (user_id, limit, offset))
                
                transactions = []
                for row in cursor.fetchall():
                    try:
                        # Decrypt transaction data
                        amount = float(SecurityManager.decrypt_data(
                            row['amount_encrypted'], encryption_key
                        ))
                        description = SecurityManager.decrypt_data(
                            row['description_encrypted'], encryption_key
                        )
                        balance_after = float(SecurityManager.decrypt_data(
                            row['balance_after_encrypted'], encryption_key
                        ))
                        
                        transactions.append({
                            'transaction_id': row['transaction_id'],
                            'type': row['type'],
                            'amount': amount,
                            'recipient_username': row['recipient_username'],
                            'source': row['source'],
                            'description': description,
                            'balance_after': balance_after,
                            'created_at': row['created_at']
                        })
                    except Exception:
                        # Skip corrupted transactions
                        continue
                
                return transactions
                
        except Exception:
            return []
    
    def get_username_by_id(self, user_id: int) -> Optional[str]:
        """Get username by user ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
                result = cursor.fetchone()
                return result['username'] if result else None
        except Exception:
            return None
    
    def user_exists(self, username: str) -> bool:
        """Check if username exists"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                return cursor.fetchone() is not None
        except Exception:
            return False
    
    def log_audit_event(self, user_id: Optional[int], username: Optional[str], 
                       action: str, details: str, status: str = 'SUCCESS'):
        """
        Log audit event.
        
        Args:
            user_id (Optional[int]): User ID
            username (Optional[str]): Username
            action (str): Action performed
            details (str): Event details
            status (str): Event status
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO audit_logs (user_id, username, action, details, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, username or 'anonymous', action, details, status))
                conn.commit()
        except Exception:
            # Don't raise exceptions for audit logging failures
            pass
    
    def get_audit_logs(self, limit: int = 50, user_id: Optional[int] = None) -> List[Dict]:
        """Get audit logs"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if user_id:
                    cursor.execute("""
                        SELECT * FROM audit_logs 
                        WHERE user_id = ?
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (user_id, limit))
                else:
                    cursor.execute("""
                        SELECT * FROM audit_logs 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """, (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []