# secure-ci-cd-pipeline

A demo Python project with an automated CI/CD pipeline that scans code for security vulnerabilities on every push, using GitHub Actions, Bandit, and Trivy.

![Security Scan](https://github.com/YOUR-USERNAME/secure-ci-cd-pipeline/actions/workflows/security-scan.yml/badge.svg)

## What this project demonstrates

Real companies run automated security checks every time someone pushes code, so vulnerabilities get caught before they reach production — instead of relying on a human to manually review every line. This project is a small-scale version of that same practice.

Every push to this repo automatically triggers two scans:
1. **Bandit** checks the Python source code for risky patterns (hardcoded secrets, unsafe function calls, weak encryption).
2. **Trivy** checks the project's dependencies (`requirements.txt`) for known, publicly documented vulnerabilities (CVEs).

If either tool finds a serious issue, the pipeline fails — the same way a real CI/CD gate would block insecure code from being merged.

## Tech stack

- **GitHub Actions** — free CI/CD automation built into GitHub, triggers on every push
- **Bandit** — a Python security linter
- **Trivy** — a dependency/CVE scanner
- **A small sample app** (`app/main.py`) — intentionally written with a few common security flaws, so the pipeline has something real to catch

## Project structure

secure-ci-cd-pipeline/
├── .github/workflows/
│ └── security-scan.yml # the automation config
├── app/
│ └── main.py # sample app with intentional vulnerabilities
├── requirements.txt # intentionally outdated dependency
├── LICENSE
└── README.md

## Vulnerabilities intentionally included (for demo purposes)

| Flaw | Tool that catches it | Why it's dangerous |
|---|---|---|
| Hardcoded password | Bandit | Secrets in source code can leak via version control |
| `subprocess` with `shell=True` | Bandit | Allows command injection if user input reaches it |
| MD5 password hashing | Bandit | MD5 is cryptographically broken and crackable |
| Use of `eval()` | Bandit | Executes arbitrary code, a major attack surface |
| Outdated `requests` library (2.19.1) | Trivy | Has 5 known CVEs, including an HTTPS→HTTP header leak |

> ⚠️ These flaws are intentional and exist only to demonstrate the scanning pipeline. Never write code like this in a real project.

## Proof it works

### ❌ Failing run (vulnerabilities present)
*(screenshot of the failed GitHub Actions run goes here)*

**Bandit output:**
*(screenshot of local Bandit run showing 5 findings)*

**Trivy output:**
*(screenshot of local Trivy run showing 5 CVEs in requests)*

### ✅ Passing run (after fixes)
*(screenshot of the passing GitHub Actions run goes here, once you fix the flaws and push again)*

## How to run this locally

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/secure-ci-cd-pipeline.git
cd secure-ci-cd-pipeline

# Install Bandit and run it
pip install bandit
bandit -r app/

# Install Trivy (Mac) and run it
brew install trivy
trivy fs .
```

## How the automation works

The workflow file at `.github/workflows/security-scan.yml` runs two jobs in parallel on every push or pull request to `main`:

- **bandit-scan** — installs Bandit and scans the `app/` directory
- **trivy-scan** — runs Trivy against the whole project to check `requirements.txt` for known CVEs

If either job finds a HIGH or CRITICAL severity issue, that job fails, which shows up as a red ❌ on the Actions tab — blocking the "merge" the same way a real security gate would.

## How each vulnerability was fixed

| Flaw | Before | After |
|---|---|---|
| Hardcoded password | `DATABASE_PASSWORD = "SuperSecret123!"` | Pulled from an environment variable via `os.environ.get(...)` |
| Shell injection risk | `subprocess.run(user_input, shell=True, ...)` | `shell=False` with `shlex.split()` to safely parse arguments |
| Weak hash (MD5) | `hashlib.md5(...)` | `hashlib.sha256(...)` |
| Arbitrary code execution (`eval`) | `eval(expression)` | `ast.literal_eval(expression)` — only allows safe literals |
| Outdated dependency | `requests==2.19.1` (5 known CVEs) | `requests==2.33.0` (patched) |

After these fixes, both Bandit and Trivy report zero issues, and the pipeline passes automatically on push.