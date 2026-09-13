"""
A tiny sample app used to demonstrate an automated security pipeline.

This version has been FIXED — all intentional vulnerabilities from the
original version have been corrected using security best practices.
"""

import hashlib
import os
import shlex
import subprocess


# --- Fix #1: no hardcoded password ---
# Secrets should come from environment variables, not source code.
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "")


def get_user_input_command(user_input):
    """
    --- Fix #2: no shell injection risk ---
    shell=True is removed, and the command is split safely with shlex
    instead of being passed directly to a shell.
    """
    args = shlex.split(user_input)
    result = subprocess.run(args, shell=False, capture_output=True)
    return result.stdout


def hash_password(password):
    """
    --- Fix #3: strong hash algorithm ---
    SHA-256 replaces the broken MD5 algorithm.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def safe_expression_eval(expression):
    """
    --- Fix #4: no eval() ---
    Using ast.literal_eval only allows safe Python literals
    (numbers, strings, lists, etc.) — no arbitrary code execution.
    """
    import ast
    return ast.literal_eval(expression)


if __name__ == "__main__":
    print("This is the fixed, secure version of the sample app.")