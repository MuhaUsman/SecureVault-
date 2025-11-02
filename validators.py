"""
Input validation functions for the FinTech application.
Provides comprehensive validation for all user inputs with security focus.
"""

import re
import html
from typing import Tuple, List
from decimal import Decimal, InvalidOperation
from config import (
    PASSWORD_MIN_LENGTH, PASSWORD_REQUIREMENTS, COMMON_PASSWORDS,
    MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH, MAX_EMAIL_LENGTH,
    MAX_DESCRIPTION_LENGTH, MAX_PURPOSE_LENGTH, MAX_AMOUNT, MIN_AMOUNT,
    MAX_FILE_SIZE_MB, ALLOWED_FILE_EXTENSIONS
)


class InputValidator:
    """Comprehensive input validation with security focus"""
    
    # SQL injection patterns to detect
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\b)",
        r"(--|#|/\*|\*/)",
        r"(\bOR\b.*=.*\bOR\b)",
        r"(\bAND\b.*=.*\bAND\b)",
        r"(;|\||&)",
        r"(\bxp_cmdshell\b)",
        r"(\bsp_executesql\b)"
    ]
    
    # XSS patterns to detect
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>",
        r"<link[^>]*>",
        r"<meta[^>]*>"
    ]
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username according to security requirements.
        
        Args:
            username (str): Username to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"
        
        # Length validation
        if len(username) < MIN_USERNAME_LENGTH:
            return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters"
        
        if len(username) > MAX_USERNAME_LENGTH:
            return False, f"Username must not exceed {MAX_USERNAME_LENGTH} characters"
        
        # Pattern validation (alphanumeric and underscore only)
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        # Check for SQL injection patterns
        if InputValidator._contains_sql_injection(username):
            return False, "Username contains invalid characters"
        
        # Check for reserved words
        reserved_words = ['admin', 'root', 'system', 'null', 'undefined']
        if username.lower() in reserved_words:
            return False, "Username is not available"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email address format and security.
        
        Args:
            email (str): Email to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        if len(email) > MAX_EMAIL_LENGTH:
            return False, f"Email must not exceed {MAX_EMAIL_LENGTH} characters"
        
        # Basic email pattern validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address"
        
        # Check for SQL injection
        if InputValidator._contains_sql_injection(email):
            return False, "Email contains invalid characters"
        
        # Check for common invalid formats
        invalid_patterns = [
            r"\.{2,}",  # Multiple consecutive dots
            r"^\.|\.$",  # Starting or ending with dot
            r"@.*@",  # Multiple @ symbols
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False, "Please enter a valid email address"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password against security requirements.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        # Length check
        if len(password) < PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters long"
        
        errors = []
        
        # Check requirements
        if PASSWORD_REQUIREMENTS['uppercase'] and not re.search(r"[A-Z]", password):
            errors.append("at least one uppercase letter")
        
        if PASSWORD_REQUIREMENTS['lowercase'] and not re.search(r"[a-z]", password):
            errors.append("at least one lowercase letter")
        
        if PASSWORD_REQUIREMENTS['digit'] and not re.search(r"\d", password):
            errors.append("at least one digit")
        
        if PASSWORD_REQUIREMENTS['special_char'] and not re.search(r"[@#$%&*!]", password):
            errors.append("at least one special character (@#$%&*!)")
        
        if errors:
            return False, f"Password must contain {', '.join(errors)}"
        
        # Check against common passwords
        if password.lower() in [pwd.lower() for pwd in COMMON_PASSWORDS]:
            return False, "Password is too common. Please choose a stronger password"
        
        # Check for username in password (if available in context)
        # This would need to be passed as parameter in real implementation
        
        return True, ""
    
    @staticmethod
    def validate_amount(amount_str: str) -> Tuple[bool, str, float]:
        """
        Validate monetary amount input.
        
        Args:
            amount_str (str): Amount as string
            
        Returns:
            Tuple[bool, str, float]: (is_valid, error_message, amount_value)
        """
        if not amount_str:
            return False, "Amount is required", 0.0
        
        # Remove whitespace
        amount_str = amount_str.strip()
        
        # Check for valid decimal format
        if not re.match(r"^\d+(\.\d{1,2})?$", amount_str):
            return False, "Amount must be a valid number with up to 2 decimal places", 0.0
        
        try:
            amount = float(amount_str)
        except ValueError:
            return False, "Invalid amount format", 0.0
        
        # Range validation
        if amount < MIN_AMOUNT:
            return False, f"Amount must be at least ${MIN_AMOUNT:.2f}", 0.0
        
        if amount > MAX_AMOUNT:
            return False, f"Amount cannot exceed ${MAX_AMOUNT:,.2f}", 0.0
        
        # Check for negative numbers
        if amount < 0:
            return False, "Amount cannot be negative", 0.0
        
        return True, "", amount
    
    @staticmethod
    def validate_text_field(text: str, field_name: str, max_length: int, 
                          required: bool = True) -> Tuple[bool, str]:
        """
        Validate text field with XSS and injection protection.
        
        Args:
            text (str): Text to validate
            field_name (str): Name of the field for error messages
            max_length (int): Maximum allowed length
            required (bool): Whether field is required
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not text and required:
            return False, f"{field_name} is required"
        
        if not text and not required:
            return True, ""
        
        # Length validation
        if len(text) > max_length:
            return False, f"{field_name} must not exceed {max_length} characters"
        
        # Check for SQL injection
        if InputValidator._contains_sql_injection(text):
            return False, f"{field_name} contains invalid characters"
        
        # Check for XSS attempts
        if InputValidator._contains_xss(text):
            return False, f"{field_name} contains invalid content"
        
        return True, ""
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize text input by escaping HTML entities and removing dangerous content.
        
        Args:
            text (str): Text to sanitize
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Escape HTML entities
        text = html.escape(text)
        
        # Remove potential script tags and dangerous content
        dangerous_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>",
            r"<embed[^>]*>.*?</embed>"
        ]
        
        for pattern in dangerous_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()
    
    @staticmethod
    def validate_file_upload(file_content: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validate file upload for security.
        
        Args:
            file_content (bytes): File content
            filename (str): Original filename
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not file_content:
            return False, "No file content provided"
        
        if not filename:
            return False, "Filename is required"
        
        # Check file size
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            return False, f"File size must not exceed {MAX_FILE_SIZE_MB}MB"
        
        # Check file extension
        file_extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''
        if file_extension not in ALLOWED_FILE_EXTENSIONS:
            allowed_exts = ', '.join(ALLOWED_FILE_EXTENSIONS)
            return False, f"File type not allowed. Allowed types: {allowed_exts}"
        
        # Check for directory traversal in filename
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Invalid filename"
        
        return True, ""
    
    @staticmethod
    def _contains_sql_injection(text: str) -> bool:
        """
        Check if text contains SQL injection patterns.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if SQL injection detected
        """
        text_upper = text.upper()
        
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def _contains_xss(text: str) -> bool:
        """
        Check if text contains XSS patterns.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if XSS detected
        """
        for pattern in InputValidator.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                return True
        
        return False
    
    @staticmethod
    def validate_search_query(query: str) -> Tuple[bool, str]:
        """
        Validate search query to prevent injection attacks.
        
        Args:
            query (str): Search query
            
        Returns:
            Tuple[bool, str]: (is_valid, sanitized_query)
        """
        if not query:
            return True, ""
        
        # Length limit
        if len(query) > 100:
            return False, "Search query too long"
        
        # Remove dangerous characters
        sanitized = re.sub(r"[<>\"'&;]", "", query)
        
        # Check for SQL injection
        if InputValidator._contains_sql_injection(sanitized):
            return False, "Invalid search query"
        
        return True, sanitized.strip()
    
    @staticmethod
    def get_password_strength_score(password: str) -> Tuple[int, List[str]]:
        """
        Calculate password strength score and provide feedback.
        
        Args:
            password (str): Password to analyze
            
        Returns:
            Tuple[int, List[str]]: (score_out_of_100, suggestions)
        """
        score = 0
        suggestions = []
        
        if len(password) >= 8:
            score += 20
        else:
            suggestions.append("Use at least 8 characters")
        
        if len(password) >= 12:
            score += 10
        
        if re.search(r"[a-z]", password):
            score += 15
        else:
            suggestions.append("Add lowercase letters")
        
        if re.search(r"[A-Z]", password):
            score += 15
        else:
            suggestions.append("Add uppercase letters")
        
        if re.search(r"\d", password):
            score += 15
        else:
            suggestions.append("Add numbers")
        
        if re.search(r"[@#$%&*!]", password):
            score += 15
        else:
            suggestions.append("Add special characters (@#$%&*!)")
        
        # Bonus for variety
        unique_chars = len(set(password))
        if unique_chars >= 8:
            score += 10
        
        # Penalty for common patterns
        if re.search(r"(123|abc|qwe|password)", password.lower()):
            score -= 20
            suggestions.append("Avoid common patterns")
        
        return min(100, max(0, score)), suggestions