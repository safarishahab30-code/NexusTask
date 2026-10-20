import os

root_dir = r"C:\NexusTask"
for dirpath, _, filenames in os.walk(root_dir):
    # رد کردن پوشه مجازی و گیت
    if ".venv" in dirpath or ".git" in dirpath:
        continue
    rel_path = os.path.relpath(dirpath, root_dir)
    print(f"پوشه: {rel_path if rel_path != '.' else 'ریشه'}")
    for f in filenames:
        print(f"    ├── {f}")
