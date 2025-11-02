# 🔐 SecureVault Pro - Manual Security Testing Guide

## 📋 Pre-Testing Setup

### Step 1: Launch Application
```bash
streamlit run app.py
```
**URL**: http://localhost:8501

### Step 2: Enable Testing Mode
1. Open the application
2. In the sidebar, check "Enable Testing Panel"
3. Click "Create Test Accounts" to set up test users

### Step 3: Test Accounts Available
- **testuser1** / test1@securevault.com / Test@1234
- **testuser2** / test2@securevault.com / Test@5678
- **admintest** / admin@securevault.com / Admin@9999

---

## 🧪 Manual Security Test Cases (25 Tests)

### Test 1: SQL Injection - Login Form
**Objective**: Verify SQL injection prevention in login
**Steps**:
1. Go to login page
2. Username: `admin' OR '1'='1' --`
3. Password: `anything`
4. Click Login
**Expected**: Login fails, no SQL error exposed
**Screenshot**: `test_01_sql_injection_login.png`

### Test 2: Password Strength Validation
**Objective**: Test password requirements enforcement
**Steps**:
1. Go to registration page
2. Username: `weakuser`
3. Password: `12345`
4. Try to register
**Expected**: Password rejected with requirements shown
**Screenshot**: `test_02_weak_password_rejection.png`

### Test 3: XSS Attack - Username Field
**Objective**: Verify XSS prevention in input fields
**Steps**:
1. Go to registration page
2. Username: `<script>alert('XSS')</script>`
3. Complete other fields correctly
4. Try to register
**Expected**: Script tags escaped, no JavaScript execution
**Screenshot**: `test_03_xss_username_sanitization.png`

### Test 4: Unauthorized Dashboard Access
**Objective**: Test access control without authentication
**Steps**:
1. Open incognito/private browser window
2. Try to navigate directly to dashboard
3. Attempt to access protected pages
**Expected**: Redirected to login page
**Screenshot**: `test_04_unauthorized_access_blocked.png`

### Test 5: Session Expiry Test
**Objective**: Verify automatic session timeout
**Steps**:
1. Login successfully
2. Go to Security → Security Testing tab
3. Click "Test Session Timeout"
4. Try to navigate or perform actions
**Expected**: Auto logout, redirect to login
**Screenshot**: `test_05_session_timeout.png`

### Test 6: Logout Functionality
**Objective**: Test complete session destruction
**Steps**:
1. Login successfully
2. Navigate to dashboard
3. Click Logout
4. Use browser back button to access dashboard
**Expected**: Cannot access dashboard, session cleared
**Screenshot**: `test_06_logout_functionality.png`

### Test 7: Data Confidentiality - Database Inspection
**Objective**: Verify data encryption at rest
**Steps**:
1. Add money to wallet (create some data)
2. Navigate to `data/secure_vault.db`
3. Open with SQLite browser or text editor
4. Check users table (password column) and wallets table (balance)
**Expected**: Passwords hashed, balances encrypted
**Screenshot**: `test_07_database_password_hashing.png`

### Test 8: File Upload Validation
**Objective**: Test file type restrictions (if implemented)
**Steps**:
1. Go to any file upload section
2. Try to upload `malicious.exe`
3. Attempt upload
**Expected**: File rejected with error message
**Screenshot**: `test_08_file_upload_restriction.png`

### Test 9: Error Message Leakage
**Objective**: Verify no sensitive information in errors
**Steps**:
1. Login with correct username, wrong password
2. Try invalid operations (send money with insufficient balance)
3. Enter malformed data
**Expected**: Generic error messages, no stack traces
**Screenshot**: `test_09_error_message_handling.png`

### Test 10: Input Length Validation
**Objective**: Test buffer overflow protection
**Steps**:
1. Go to Add Money → Description field
2. Enter 5000+ characters (copy-paste long text)
3. Try to submit
**Expected**: Input rejected or truncated safely
**Screenshot**: `test_10_input_length_validation.png`

### Test 11: Duplicate User Registration
**Objective**: Test unique constraint enforcement
**Steps**:
1. Register new user: `duplicatetest`
2. Logout
3. Try to register again with same username
**Expected**: "Username already exists" error
**Screenshot**: `test_11_duplicate_username_error.png`

### Test 12: Number Field Validation
**Objective**: Test numeric input validation
**Steps**:
1. Go to Add Money page
2. Amount field: enter `abc123xyz`
3. Try to submit
**Expected**: Validation error, only numbers accepted
**Screenshot**: `test_12_numeric_validation.png`

### Test 13: Password Match Validation
**Objective**: Test password confirmation
**Steps**:
1. Go to registration page
2. Password: `Test@1234`
3. Confirm Password: `Test@5678` (different)
4. Try to register
**Expected**: "Passwords don't match" error
**Screenshot**: `test_13_password_mismatch_error.png`

### Test 14: Data Modification Attempt
**Objective**: Test backend validation
**Steps**:
1. Login and view transaction history
2. Use browser inspector to modify transaction amounts in HTML
3. Attempt to submit modified data
**Expected**: Backend validates, changes rejected
**Screenshot**: `test_14_data_modification_blocked.png`

### Test 15: Email Validation
**Objective**: Test email format validation
**Steps**:
1. Go to registration page
2. Email: `abc@` (invalid format)
3. Also try: `notanemail`, `user@`, `@domain.com`
4. Try to register
**Expected**: Validation error for invalid email
**Screenshot**: `test_15_email_validation_error.png`

### Test 16: Login Attempt Lockout
**Objective**: Test brute force protection
**Steps**:
1. Go to login page
2. Enter correct username, wrong password
3. Repeat 5 times consecutively
4. Try 6th login
**Expected**: Account locked, lockout message shown
**Screenshot**: `test_16_login_lockout_triggered.png`

### Test 17: Secure Error Handling
**Objective**: Test graceful error handling
**Steps**:
1. Cause various errors intentionally
2. Access non-existent pages
3. Send invalid requests
**Expected**: No crashes, controlled error messages
**Screenshot**: `test_17_error_handling_graceful.png`

### Test 18: Encrypted Record Verification
**Objective**: Verify encryption implementation
**Steps**:
1. Add money to wallet
2. Open database file
3. Look at wallets and transactions tables
4. Verify data appears encrypted
**Expected**: Sensitive data encrypted in storage
**Screenshot**: `test_18_encrypted_database_records.png`

### Test 19: Unicode/Emoji Input Handling
**Objective**: Test international character support
**Steps**:
1. Try entering unicode in various fields
2. Username: `user😀123`
3. Description: `Payment for 🍕 pizza`
4. Submit and verify behavior
**Expected**: Unicode handled gracefully or rejected safely
**Screenshot**: `test_19_unicode_emoji_handling.png`

### Test 20: Empty Field Submission
**Objective**: Test required field validation
**Steps**:
1. Go to registration form
2. Leave all fields empty/blank
3. Try to submit
4. Also try with only some fields filled
**Expected**: Validation warnings, form not submitted
**Screenshot**: `test_20_empty_field_validation.png`

### Test 21: Session Hijacking Prevention (Bonus)
**Objective**: Test session security
**Steps**:
1. Login and inspect session tokens (if visible)
2. Open new browser window
3. Try to use the same session token
**Expected**: Session not reusable, forced to login
**Screenshot**: `test_21_session_hijacking_prevention.png`

### Test 22: CSRF Protection (Bonus)
**Objective**: Test cross-site request forgery protection
**Steps**:
1. Login successfully
2. Try to submit transaction from external form
3. Verify token validation
**Expected**: Transaction rejected without valid token
**Screenshot**: `test_22_csrf_protection.png`

### Test 23: Password Change Security (Bonus)
**Objective**: Test password change security
**Steps**:
1. Login and go to Security → Change Password
2. Try to change without entering old password
3. Try with wrong old password
**Expected**: Requires old password verification
**Screenshot**: `test_23_password_change_security.png`

### Test 24: Audit Log Completeness (Bonus)
**Objective**: Test comprehensive logging
**Steps**:
1. Perform various actions (login, transactions, logout)
2. Go to Security → Activity Log
3. Verify all actions are logged
**Expected**: All security-relevant actions logged
**Screenshot**: `test_24_audit_log_completeness.png`

### Test 25: Rate Limiting (Bonus)
**Objective**: Test request throttling
**Steps**:
1. Attempt rapid-fire login attempts
2. Try submitting multiple transactions quickly
3. Test rapid API requests
**Expected**: Rate limiting kicks in, requests throttled
**Screenshot**: `test_25_rate_limiting.png`

---

## 📊 Test Results Table Template

| No. | Test Case | Action Performed | Expected Outcome | Observed Result | Screenshot Ref | Pass/Fail |
|-----|-----------|------------------|------------------|-----------------|----------------|-----------|
| 1 | SQL Injection | Entered `' OR '1'='1' --` in login | Input rejected | Login failed with "Invalid credentials" | Screenshot 1 | ✅ Pass |
| 2 | Password Strength | Tried weak password `12345` | Password rejected | Requirements shown | Screenshot 2 | ✅ Pass |
| ... | ... | ... | ... | ... | ... | ... |

---

## 🎯 Testing Checklist

### Pre-Testing
- [ ] Application running at http://localhost:8501
- [ ] Testing panel enabled in sidebar
- [ ] Test accounts created
- [ ] Screenshot tool ready

### Core Security Tests (1-20)
- [ ] Test 1: SQL Injection
- [ ] Test 2: Password Strength
- [ ] Test 3: XSS Attack
- [ ] Test 4: Unauthorized Access
- [ ] Test 5: Session Expiry
- [ ] Test 6: Logout Function
- [ ] Test 7: Database Confidentiality
- [ ] Test 8: File Upload
- [ ] Test 9: Error Messages
- [ ] Test 10: Input Length
- [ ] Test 11: Duplicate User
- [ ] Test 12: Number Validation
- [ ] Test 13: Password Match
- [ ] Test 14: Data Modification
- [ ] Test 15: Email Validation
- [ ] Test 16: Login Lockout
- [ ] Test 17: Error Handling
- [ ] Test 18: Encryption Check
- [ ] Test 19: Unicode Input
- [ ] Test 20: Empty Fields

### Bonus Tests (21-25)
- [ ] Test 21: Session Hijacking
- [ ] Test 22: CSRF Protection
- [ ] Test 23: Password Change
- [ ] Test 24: Audit Logs
- [ ] Test 25: Rate Limiting

### Documentation
- [ ] All screenshots captured and named correctly
- [ ] Word document created with proper formatting
- [ ] Test results table completed
- [ ] Screenshots inserted and labeled
- [ ] Document proofread and finalized

---

## 🔧 Testing Utilities Available

### In Sidebar Testing Panel:
- **Quick Test Inputs**: Copy-paste ready attack vectors
- **System Information**: Database location, session state
- **Session Testing**: Simulate timeout, force logout
- **Test Accounts**: Pre-created user credentials

### In Security Center:
- **Security Testing Tab**: Current session info, security features status
- **Database Security Check**: Verify encryption
- **Quick Security Tests**: One-click test simulations

---

## 📝 Screenshot Naming Convention

Save screenshots with descriptive names:
- `test_01_sql_injection_login.png`
- `test_02_weak_password_rejection.png`
- `test_03_xss_username_sanitization.png`
- etc.

---

## 🎯 Success Criteria

**PASS Criteria**: Security feature works as expected, prevents attack
**FAIL Criteria**: Security vulnerability found, attack succeeds

**Overall Goal**: Demonstrate that SecureVault Pro implements comprehensive security measures and handles attack attempts gracefully.

---

## 📞 Need Help?

If you encounter issues during testing:
1. Check the sidebar testing panel for utilities
2. Use the "Show Test Inputs" button for attack vectors
3. Check the Security Center for system status
4. Review the audit logs for detailed activity tracking

**Happy Testing! 🔐**