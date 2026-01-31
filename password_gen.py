#!/usr/bin/env python3

import argparse
import random
import string
import math
import json
import base64
import os
from datetime import datetime
from typing import List, Dict, Tuple


class PasswordSecurityTool:
    def __init__(self, common_passwords_file: str = "common_passwords.txt"):
        self.history_file = "password_history.enc"
        self.common_passwords_file = common_passwords_file
        self.common_passwords = self._load_common_passwords_from_file()
        self.word_list = self._load_word_list()

    def _load_common_passwords_from_file(self) -> List[str]:
        passwords = []
        try:
            if os.path.exists(self.common_passwords_file):
                with open(self.common_passwords_file, 'r', encoding='utf-8') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                if passwords:
                    print(f"Loaded {len(passwords)} common passwords from '{self.common_passwords_file}'")
                    return passwords[:1000]
        except Exception as e:
            print(f"Error loading file: {e}")

        print("Using default common passwords list")
        return self._get_default_passwords()[:1000]

    def _get_default_passwords(self) -> List[str]:
        default = [
            "password", "123456", "12345678", "1234", "qwerty", "12345",
            "dragon", "football", "baseball", "welcome", "abc123",
            "111111", "mustang", "access", "master", "michael", "superman",
            "696969", "123123", "batman", "trustno1", "monkey", "1234567",
            "letmein", "shadow", "ashley", "sunshine", "iloveyou", "fuckyou",
            "parola", "password123", "admin", "qwerty123", "welcome123"
        ]
        for i in range(1000, 2000):
            default.append(f"password{i}")
            default.append(f"parola{i}")
        return default

    def _load_word_list(self) -> List[str]:
        words = [
            "sun", "moon", "star", "sky", "earth", "water", "fire", "wind",
            "tree", "flower", "house", "car", "human", "animal", "time",
            "love", "friend", "family", "mountain", "sea", "river", "book",
            "computer", "phone", "window", "door", "chair",
            "blue", "red", "green", "yellow", "black", "white", "orange"
        ]
        return words

    def _calculate_entropy(self, password: str) -> float:
        if not password:
            return 0

        char_sets = 0
        length = len(password)

        if any(c.islower() for c in password):
            char_sets += 26
        if any(c.isupper() for c in password):
            char_sets += 26
        if any(c.isdigit() for c in password):
            char_sets += 10
        if any(c in string.punctuation for c in password):
            char_sets += 32

        if char_sets == 0:
            char_sets = 26

        entropy = length * math.log2(char_sets)
        return entropy

    def _entropy_to_score(self, entropy: float) -> Tuple[int, str]:
        if entropy < 28:
            return (max(0, int(entropy)), "VERY WEAK")
        elif entropy < 36:
            return (30 + int((entropy - 28) / 8 * 20), "WEAK")
        elif entropy < 60:
            return (50 + int((entropy - 36) / 24 * 30), "MEDIUM")
        elif entropy < 80:
            return (80 + int((entropy - 60) / 20 * 15), "STRONG")
        else:
            return (95 + min(5, int((entropy - 80) / 20 * 5)), "VERY STRONG")

    def generate_password(self, length: int = 16,
                          use_upper: bool = True,
                          use_numbers: bool = True,
                          use_special: bool = True) -> str:
        characters = string.ascii_lowercase

        if use_upper:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        password_chars = []
        if use_upper:
            password_chars.append(random.choice(string.ascii_uppercase))
        if use_numbers:
            password_chars.append(random.choice(string.digits))
        if use_special:
            password_chars.append(random.choice(string.punctuation))

        remaining_length = length - len(password_chars)
        if remaining_length > 0:
            password_chars.extend(random.choices(characters, k=remaining_length))

        random.shuffle(password_chars)
        password = ''.join(password_chars)

        return password

    def generate_memorable_password(self, num_words: int = 3) -> str:
        words = random.sample(self.word_list, num_words)

        add_number = random.choice([True, False])
        add_special = random.choice([True, False])

        password_parts = []
        separator = random.choice(['-', '.', '_', ''])

        for i, word in enumerate(words):
            if random.choice([True, False]):
                word = word.capitalize()
            password_parts.append(word)

        password = separator.join(password_parts)

        if add_number:
            password += str(random.randint(10, 99))
        if add_special:
            password += random.choice(string.punctuation)

        return password

    def analyze_password(self, password: str) -> Dict:
        entropy = self._calculate_entropy(password)
        score, strength = self._entropy_to_score(entropy)

        analysis = {
            'password': password,
            'length': len(password),
            'entropy': entropy,
            'score': score,
            'strength': strength,
            'has_lower': any(c.islower() for c in password),
            'has_upper': any(c.isupper() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_special': any(c in string.punctuation for c in password),
            'is_common': password.lower() in [p.lower() for p in self.common_passwords],
            'problems': [],
            'suggestions': []
        }

        if len(password) < 8:
            analysis['problems'].append("Too short (minimum recommended: 12 characters)")
        elif len(password) < 12:
            analysis['problems'].append("Suboptimal length (recommended: 12+ characters)")

        if not analysis['has_upper']:
            analysis['problems'].append("Missing uppercase letters")
        if not analysis['has_digits']:
            analysis['problems'].append("Missing digits")
        if not analysis['has_special']:
            analysis['problems'].append("Missing special characters")

        if analysis['is_common']:
            analysis['problems'].append("Found in common password lists")

        if password.isnumeric():
            analysis['problems'].append("Contains only digits")
        if password.isalpha():
            analysis['problems'].append("Contains only letters")

        sequences = ['123', 'abc', 'qwe', 'asd', 'password', 'parola']
        for seq in sequences:
            if seq in password.lower():
                analysis['problems'].append(f"Contains common sequence '{seq}'")
                break

        if analysis['score'] < 50:
            suggestions = []

            if len(password) < 12:
                suggestions.append(f"Add {12 - len(password)} characters")

            if not analysis['has_upper']:
                suggestions.append("Add uppercase letters")
            if not analysis['has_digits']:
                suggestions.append("Add digits")
            if not analysis['has_special']:
                suggestions.append("Add symbols (@, #, $, etc.)")

            improved = password
            if not analysis['has_upper'] and improved[0].islower():
                improved = improved[0].upper() + improved[1:]
            if not analysis['has_special']:
                improved += random.choice(['#', '!', '$', '@'])
            if len(improved) < 12:
                improved += str(random.randint(10, 99))

            if improved != password:
                analysis['suggestions'].append(f"Improved version: {improved}")

        return analysis

    def _encrypt_data(self, data: str) -> str:
        encoded = base64.b64encode(data.encode()).decode()
        return encoded

    def _decrypt_data(self, encrypted_data: str) -> str:
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return decoded
        except:
            return ""

    def save_to_history(self, password: str, metadata: Dict = None):
        history = self.load_history()

        entry = {
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        history.append(entry)

        if len(history) > 100:
            history = history[-100:]

        data_json = json.dumps(history)
        encrypted = self._encrypt_data(data_json)

        with open(self.history_file, 'w') as f:
            f.write(encrypted)

    def load_history(self) -> List[Dict]:
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(self.history_file, 'r') as f:
                encrypted = f.read()

            if not encrypted:
                return []

            decrypted = self._decrypt_data(encrypted)
            if decrypted:
                return json.loads(decrypted)
        except:
            pass

        return []

    def view_history(self):
        history = self.load_history()

        if not history:
            print("History is empty.")
            return

        print("\n=== PASSWORD HISTORY ===")
        print(f"Total entries: {len(history)}")
        print("-" * 50)

        for i, entry in enumerate(reversed(history[-10:]), 1):
            pwd = entry['password']
            timestamp = entry.get('timestamp', 'Unknown')

            if len(pwd) > 4:
                masked = pwd[0] + "*" * (len(pwd) - 2) + pwd[-1]
            else:
                masked = "*" * len(pwd)

            print(f"{i}. {masked} - {timestamp}")

        print("-" * 50)
        print("NOTE: Passwords are stored encrypted for security.")

    def generate_batch(self, count: int, **kwargs) -> List[str]:
        passwords = []
        for _ in range(count):
            if kwargs.get('memorable', False):
                pwd = self.generate_memorable_password(kwargs.get('words', 3))
            else:
                pwd = self.generate_password(
                    length=kwargs.get('length', 16),
                    use_upper=kwargs.get('upper', True),
                    use_numbers=kwargs.get('numbers', True),
                    use_special=kwargs.get('special', True)
                )
            passwords.append(pwd)
        return passwords

    def display_analysis(self, analysis: Dict, show_password: bool = False):
        print(f"\n=== PASSWORD ANALYSIS ===")
        if show_password:
            print(f"Password analyzed: {analysis['password']}")
        else:
            print(f"Password analyzed: {'*' * len(analysis['password'])}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")
        print(f"Entropy: {analysis['entropy']:.1f} bits")
        print(f"Length: {analysis['length']} characters")

        print(f"\nContains:")
        if analysis['has_lower']:
            print("  ✓ Lowercase letters")
        if analysis['has_upper']:
            print("  ✓ Uppercase letters")
        if analysis['has_digits']:
            print("  ✓ Digits")
        if analysis['has_special']:
            print("  ✓ Symbols")

        if analysis['is_common']:
            print(f"\n WARNING: This password appears in common password lists!")

        if analysis['problems']:
            print(f"\nProblems identified:")
            for problem in analysis['problems']:
                print(f"  • {problem}")

        if analysis['suggestions']:
            print(f"\nImprovement suggestions:")
            for suggestion in analysis['suggestions']:
                print(f"  → {suggestion}")

        print(f"\n{'=' * 50}")


def main():
    parser = argparse.ArgumentParser(
        description='Security tool for password generation and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  Generate password:
    ./password_gen.py --length 16 --upper --numbers --special

  Analyze password:
    ./password_gen.py --check "password123"

  Analyze with password shown:
    ./password_gen.py --check "password123" --show

  Generate batch:
    ./password_gen.py --batch 10 --length 12

  History:
    ./password_gen.py --history view

  Memorable password:
    ./password_gen.py --memorable --words 3
        """
    )

    parser.add_argument('--common-file', type=str, default="common_passwords.txt",
                        help='File with common passwords (default: common_passwords.txt)')
    parser.add_argument('--show', action='store_true',
                        help='Show password in analysis (NOT recommended in public)')

    gen_group = parser.add_argument_group('Password generation')
    gen_group.add_argument('--length', type=int, default=16, help='Password length')
    gen_group.add_argument('--upper', action='store_true', help='Include uppercase letters')
    gen_group.add_argument('--numbers', action='store_true', help='Include digits')
    gen_group.add_argument('--special', action='store_true', help='Include symbols')

    parser.add_argument('--check', type=str, help='Analyze a specific password')
    parser.add_argument('--batch', type=int, help='Generate multiple passwords')
    parser.add_argument('--history', choices=['view', 'clear'], help='Manage history')
    parser.add_argument('--memorable', action='store_true', help='Generate memorable password')
    parser.add_argument('--words', type=int, default=3, help='Number of words for memorable passwords')

    args = parser.parse_args()

    tool = PasswordSecurityTool(common_passwords_file=args.common_file)

    if not any(vars(args).values()):
        parser.print_help()
        return

    if args.check:
        analysis = tool.analyze_password(args.check)
        tool.display_analysis(analysis, show_password=args.show)

    elif args.batch:
        print(f"\nGenerating {args.batch} passwords...")
        print("-" * 50)

        passwords = tool.generate_batch(
            args.batch,
            length=args.length,
            upper=args.upper,
            numbers=args.numbers,
            special=args.special,
            memorable=args.memorable,
            words=args.words
        )

        for i, pwd in enumerate(passwords, 1):
            analysis = tool.analyze_password(pwd)
            print(f"{i:2d}. {pwd}")
            print(f"    Strength: {analysis['strength']} ({analysis['score']}/100)")

        print("-" * 50)
        print(f"Total generated: {len(passwords)} passwords")

    elif args.history:
        if args.history == 'view':
            tool.view_history()
        elif args.history == 'clear':
            if os.path.exists(tool.history_file):
                os.remove(tool.history_file)
                print("History cleared.")

    elif args.memorable:
        pwd = tool.generate_memorable_password(args.words)
        analysis = tool.analyze_password(pwd)

        print(f"\nGenerated password: {pwd}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")
        print(f"Entropy: {analysis['entropy']:.1f}/100")

        contains = []
        if analysis['has_lower']:
            contains.append("lowercase letters")
        if analysis['has_upper']:
            contains.append("UPPERCASE letters")
        if analysis['has_digits']:
            contains.append("digits")
        if analysis['has_special']:
            contains.append("symbols")
        print(f"Contains: {', '.join(contains)}")

        tool.save_to_history(pwd, {'type': 'memorable', 'words': args.words})
        print("Saved to encrypted history.")

    else:
        pwd = tool.generate_password(
            length=args.length,
            use_upper=args.upper,
            use_numbers=args.numbers,
            use_special=args.special
        )

        analysis = tool.analyze_password(pwd)

        print(f"\nGenerated password: {pwd}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/100)")
        print(f"Entropy: {analysis['entropy']:.1f} bits")

        contains = []
        if analysis['has_lower']:
            contains.append("lowercase letters")
        if analysis['has_upper']:
            contains.append("UPPERCASE letters")
        if analysis['has_digits']:
            contains.append("digits")
        if analysis['has_special']:
            contains.append("symbols")
        print(f"Contains: {', '.join(contains)}")

        tool.save_to_history(pwd, {
            'type': 'standard',
            'length': args.length,
            'has_upper': args.upper,
            'has_numbers': args.numbers,
            'has_special': args.special
        })
        print("Saved to encrypted history.")


if __name__ == "__main__":
    main()