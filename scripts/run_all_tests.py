import subprocess
import sys

def main():
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-v",
        "--disable-warnings",
        "tests",
    ]
    print("Executing:", " ".join(cmd))
    code = subprocess.call(cmd)
    if code == 0:
        print("\n[SUCCESS] All tests passed cleanly.")
    else:
        print(f"\n[FAIL] Pytest exited with code {code}.")
    sys.exit(code)

if __name__ == "__main__":
    main()
