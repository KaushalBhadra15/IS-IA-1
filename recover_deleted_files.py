import os
import subprocess

# Set paths
DISK_IMAGE = "disk.img"  # Replace with your disk image file
OUTPUT_DIR = "recovered_files"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Step 1: List deleted files using fls
print("[*] Scanning for deleted files...")
fls_cmd = ["fls", "-r", "-o", "2048", DISK_IMAGE]  # Adjust -o (offset) if needed
result = subprocess.run(fls_cmd, capture_output=True, text=True)

# Step 2: Process fls output
for line in result.stdout.split("\n"):
    if line.strip() and "r/" in line:  # 'r/' means a deleted file
        parts = line.strip().split()
        inode = parts[0]  # Extract inode number
        filename = " ".join(parts[1:]).replace("/", "_")  # Extract filename

        print(f"[*] Recovering: {filename} (inode {inode})")

        # Step 3: Recover file using icat
        recovered_path = os.path.join(OUTPUT_DIR, filename)
        with open(recovered_path, "wb") as outfile:
            icat_cmd = ["icat", "-o", "2048", DISK_IMAGE, inode]
            subprocess.run(icat_cmd, stdout=outfile)

print("[*] Recovery complete. Check the 'recovered_files' folder.")
