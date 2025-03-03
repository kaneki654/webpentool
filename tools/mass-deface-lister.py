import os

def banner():
    print("""
    ============================
         Mass Lister Tool
         for defacer
            created by TNS-ZH3N
    ============================
    """)

def main():
    banner()
    websites_file = input("Enter the name of the websites list file (e.g., websites.txt): ").strip()
    directory = input("Enter the your deface script name: ").strip()
    output_file = "output.txt"

    if not os.path.exists(websites_file):
        print(f"[!] The file '{websites_file}' does not exist.")
        return

    with open(websites_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            url = line.strip()
            if url:
                modified_url = f"{url.rstrip('/')}/{directory}"
                outfile.write(modified_url + "\n")

    print(f"[+] Process completed. Check '{output_file}' for results.")

if __name__ == "__main__":
    main()
