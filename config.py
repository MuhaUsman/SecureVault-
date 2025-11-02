# Configuration constants for SecureVault Pro

# Database configuration
DATABASE_PATH = "data/secure_vault.db"

# Security configuration
BCRYPT_ROUNDS = 12
SESSION_TIMEOUT_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

# Password requirements
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIREMENTS = {
    'uppercase': True,
    'lowercase': True,
    'digit': True,
    'special_char': True
}

# Common passwords to reject
COMMON_PASSWORDS = [
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password123', 'admin', 'letmein', 'welcome', 'monkey',
    '1234567890', 'password1', '123123', 'admin123'
]

# Input validation limits
MAX_USERNAME_LENGTH = 20
MIN_USERNAME_LENGTH = 3
MAX_EMAIL_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 100
MAX_PURPOSE_LENGTH = 50
MAX_AMOUNT = 1000000.00
MIN_AMOUNT = 0.01

# File upload limits
MAX_FILE_SIZE_MB = 5
ALLOWED_FILE_EXTENSIONS = ['.pdf', '.jpg', '.png', '.txt']

# UI Configuration
APP_TITLE = "SecureVault Pro - Premium Wealth Management"
COMPANY_NAME = "SecureVault Technologies"

# Color scheme
COLORS = {
    'primary': '#1E3A8A',
    'secondary': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'background': '#F9FAFB'
}

# Audit log actions
AUDIT_ACTIONS = {
    'REGISTER': 'User registration',
    'LOGIN_SUCCESS': 'Successful login',
    'LOGIN_FAILED': 'Failed login attempt',
    'LOGOUT': 'User logout',
    'PASSWORD_CHANGE': 'Password changed',
    'PROFILE_UPDATE': 'Profile updated',
    'TRANSACTION_CREATE': 'Transaction created',
    'BALANCE_INQUIRY': 'Balance inquiry',
    'VALIDATION_FAILED': 'Input validation failed',
    'SUSPICIOUS_ACTIVITY': 'Suspicious activity detected',
    'SESSION_TIMEOUT': 'Session timeout',
    'ACCOUNT_LOCKED': 'Account locked',
    'FILE_UPLOAD': 'File uploaded'
}