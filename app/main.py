"""
A tiny sample app used to demonstrate an automated security pipeline.

This file intentionally contains a few common security mistakes,
so that Bandit (a Python security linter) has something real to catch
when the CI/CD pipeline runs. Don't copy these patterns into real projects!
"""

import hashlib
import subprocess

# --- Intentional flaw #1: hardcoded credentials ---
# Bandit flags this because secrets should never live in source code.
DATABASE_PASSWORD = "SuperSecret123!"


def get_user_input_command(user_input):
    """
    --- Intentional flaw #2: shell injection risk ---
    Using shell=True with unsanitized user input lets an attacker run
    arbitrary commands on the server. Bandit flags this as high severity.
    """
    result = subprocess.run(user_input, shell=True, capture_output=True)
    return result.stdout


def hash_password(password):
    """
    --- Intentional flaw #3: weak/broken hash algorithm ---
    MD5 is cryptographically broken and should never be used for passwords.
    Bandit flags this too.
    """
    return hashlib.md5(password.encode()).hexdigest()


def run_dangerous_eval(expression):
    """
    --- Intentional flaw #4: use of eval() ---
    eval() executes arbitrary code, which is extremely dangerous if the
    input isn't 100% trusted. Bandit flags this as well.
    """
    return eval(expression)


if __name__ == "__main__":
    print("This is a sample app with intentional security flaws for demo purposes.")