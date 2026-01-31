# 🔐 Password Security Tool

![GitHub](https://img.shields.io/github/license/sandu04/password-security-tool)
![Docker Image](https://img.shields.io/docker/image-size/sandu04/password-tool/latest)
![Docker Pulls](https://img.shields.io/docker/pulls/sandu04/password-tool)

**Run with one command:**
```bash
docker run --rm sandu04/password-tool --help

## 🐳 Quick Run with Docker

### One-command run:
```bash
docker run --rm yourusername/password-tool --length 16 --upper --numbers --special

# Password Security Tool

# Generate password
docker run --rm yourusername/password-tool --length 20

# Analyze password
docker run --rm yourusername/password-tool --check "password123" --show

# Help
docker run --rm yourusername/password-tool --help

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