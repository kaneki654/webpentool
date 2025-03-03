import socket
import time
import sys

def print_banner():
    banner = """
██╗     ██╗███████╗████████╗   ██╗██████╗       ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██║     ██║██╔════╝╚══██╔══╝   ██║██╔══██╗      ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██║     ██║███████╗   ██║█████╗██║██████╔╝█████╗███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║     ██║╚════██║   ██║╚════╝██║██╔═══╝ ╚════╝╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████╗██║███████║   ██║      ██║██║           ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝╚═╝╚══════╝   ╚═╝      ╚═╝╚═╝           ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                  priv tools OF 0x.Zh3n
    """
    print(banner)

def loading_pyramid():
    pyramid = [
        "█     ",
        "██    ",
        "███   ",
        "████  ",
        "█████ ",
        "██████"
    ]
    
    for line in pyramid:
        print(line, end="\r")
        time.sleep(0.3)  # Delay effect
        sys.stdout.write("\033[K")  # Clear line before next print
    
    print("\nLoading Complete!\n")

def resolve_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            domains = file.read().splitlines()

        if not domains:
            print("The file is empty. Please provide a valid file.")
            return

        with open("ip.txt", "w") as output_file:
            for domain in domains:
                domain = domain.replace("https://", "").replace("http://", "").strip()
                if not domain:
                    continue
                try:
                    ip = socket.gethostbyname(domain)
                    output_file.write(f"{ip}\n")
                    print(f"Resolved: {domain} -> {ip}")
                except socket.gaierror:
                    print(f"Failed to resolve: {domain}")
        
        print("\nResolution complete! Check 'ip.txt' for results.")

    except FileNotFoundError:
        print("Error: File not found. Please provide a valid file path.")

if __name__ == "__main__":
    print_banner()
    file_path = input("Enter the path to your web list (TXT file): ").strip()
    print()
    loading_pyramid()
    resolve_domains(file_path)
