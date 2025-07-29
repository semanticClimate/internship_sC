import subprocess

# Set your wordlist and output dict folder
wordlist_path = "Keyword_Extraction/WG1_CH04_wordlist.txt"
output_dir = "wg1_dict"

# Command to run ami-dict
command = [
    "python", "-m", "amilib.ami_dict",
    "-t", wordlist_path,
    "--dict", output_dir,
    "--debug", "true"
]

try:
    subprocess.run(command, check=True)
    print(f"✅ Dictionary generated at: {output_dir}/dictionary.html")
except subprocess.CalledProcessError as e:
    print("❌ Error occurred while generating dictionary:", e)
