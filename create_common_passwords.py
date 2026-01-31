#!/usr/bin/env python3

common_passwords = [
    "password", "123456", "12345678", "1234", "qwerty", "12345",
    "dragon", "football", "baseball", "welcome", "abc123",
    "111111", "mustang", "access", "master", "michael", "superman",
    "696969", "123123", "batman", "trustno1", "monkey", "1234567",
    "letmein", "shadow", "ashley", "sunshine", "iloveyou", "fuckyou",
    "parola", "password123", "admin", "qwerty123", "welcome123",
    "123456789", "1234567890", "qwertyuiop", "1q2w3e4r", "qazwsx",
    "123qwe", "zaq12wsx", "!@#$%^&*", "password1", "123abc",
    "test", "test123", "guest", "root", "administrator",
    "hello", "hello123", "pass", "pass123", "123pass",
    "qwerty1234", "qwertyui", "q1w2e3r4", "1qaz2wsx", "1q2w3e",
    "123456a", "a123456", "123456b", "b123456", "123456c",
    "c123456", "123456d", "d123456", "123456e", "e123456",
    "123456f", "f123456", "123456g", "g123456", "123456h",
    "h123456", "123456i", "i123456", "123456j", "j123456",
    "123456k", "k123456", "123456l", "l123456", "123456m",
    "m123456", "123456n", "n123456", "123456o", "o123456",
    "123456p", "p123456", "123456q", "q123456", "123456r",
    "r123456", "123456s", "s123456", "123456t", "t123456",
    "123456u", "u123456", "123456v", "v123456", "123456w",
    "w123456", "123456x", "x123456", "123456y", "y123456",
    "123456z", "z123456", "admin123", "administrator123",
    "root123", "system", "system123", "server", "server123",
    "database", "database123", "network", "network123",
    "security", "security123", "info", "info123", "web",
    "web123", "www", "www123", "http", "http123",
    "https", "https123", "ftp", "ftp123", "ssh",
    "ssh123", "telnet", "telnet123", "mysql", "mysql123",
    "oracle", "oracle123", "postgres", "postgres123",
    "windows", "windows123", "linux", "linux123", "ubuntu",
    "ubuntu123", "debian", "debian123", "centos", "centos123",
    "redhat", "redhat123", "freebsd", "freebsd123", "solaris",
    "solaris123", "unix", "unix123", "macos", "macos123",
    "apple", "apple123", "microsoft", "microsoft123",
    "google", "google123", "facebook", "facebook123",
    "twitter", "twitter123", "instagram", "instagram123",
    "linkedin", "linkedin123", "youtube", "youtube123",
    "amazon", "amazon123", "ebay", "ebay123", "paypal",
    "paypal123", "visa", "visa123", "mastercard", "mastercard123"
]

for i in range(100, 2000, 10):
    common_passwords.append(f"password{i}")
    common_passwords.append(f"parola{i}")
    common_passwords.append(f"pass{i}")
    common_passwords.append(f"admin{i}")
    common_passwords.append(f"user{i}")
    common_passwords.append(f"test{i}")
    common_passwords.append(f"qwerty{i}")

with open("common_passwords.txt", "w", encoding="utf-8") as f:
    for password in common_passwords[:1000]:
        f.write(password + "\n")

print(f"File 'common_passwords.txt' created with {len(common_passwords[:1000])} common passwords.")