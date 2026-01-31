# Password Security Tool

A secure password generator and analyzer tool with strong encryption features.

## Features
- Generate strong passwords with configurable criteria
- Analyze existing password strength (entropy-based)
- Batch password generation
- Test against common password lists (top 1000)
- Encrypted history storage (Base64)
- Memorable password generation (with words)
- Password improvement suggestions

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/password-security-tool.git
cd password-security-tool

# Make script executable
chmod +x password_gen.py

# Create common passwords file
python3 create_common_passwords.py