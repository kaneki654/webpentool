import sys
import requests
import os
from colorama import Fore, Style, init
from urllib.parse import urlparse

# Initialize colorama
init(autoreset=True)

# ASCII Art Header with Yellow Color
ascii_art = """
   _____ _             _____      _   _     ______ _           _           
  / ____| |           |  __ \    | | | |   |  ____(_)         | |          
 | (___ | |_ __ _ _ __| |__) |_ _| |_| |__ | |__   _ _ __   __| | ___ _ __ 
  \___ \| __/ _` | '__|  ___/ _` | __| '_ \|  __| | | '_ \ / _` |/ _ \ '__|
  ____) | || (_| | |  | |  | (_| | |_| | | | |    | | | | | (_| |  __/ |   
 |_____/ \__\__,_|_|  |_|   \__,_|\__|_| |_|_|    |_|_| |_|\__,_|\___|_|   
"""

# Credit text for the bottom
credit_text = """
   TheNexusSquad admin finder
   Created by MR.S3ND0
"""

def ensure_http(url):
    """
    Ensure the URL has a scheme (http:// or https://).
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return "http://" + url
    return url

def find_admin_page(target_url):
    """
    Checks if the /admin/ path exists on the target URL and displays the status code with colored output.

    Args:
        target_url (str): The base URL of the target site.

    Returns:
        str: Result string indicating the URL and status.
    """
    # Ensure the target URL ends with a slash
    if not target_url.endswith('/'):
        target_url += '/'

    admin_path = "admin/"
    full_url = ensure_http(target_url + admin_path)  # Ensure URL has http://

    try:
        # Increase timeout to 5 seconds
        response = requests.get(full_url, timeout=5)
        status_code = int(response.status_code)  # Ensure status_code is an integer

        # Display the result with the correct color based on the status code
        if 200 <= status_code < 300:
            result = f"{Fore.GREEN}[+] {full_url} - Status Code: {status_code} (Success){Style.RESET_ALL}"
            return result, full_url
        elif 300 <= status_code < 400:
            result = f"{Fore.YELLOW}[~] {full_url} - Status Code: {status_code} (Redirect){Style.RESET_ALL}"
            return result, None
        elif status_code == 403:
            result = f"{Fore.RED}[!] {full_url} - Status Code: {status_code} (Forbidden){Style.RESET_ALL}"
            return result, None
        elif 400 <= status_code < 500:
            result = f"{Fore.RED}[!] {full_url} - Status Code: {status_code} (Client Error){Style.RESET_ALL}"
            return result, None
        elif 500 <= status_code < 600:
            result = f"{Fore.RED + Style.BRIGHT}[!] {full_url} - Status Code: {status_code} (Server Error){Style.RESET_ALL}"
            return result, None
        else:
            result = f"{Fore.WHITE}[?] {full_url} - Status Code: {status_code} (Unknown){Style.RESET_ALL}"
            return result, None
    except requests.RequestException as e:
        result = f"{Fore.RED + Style.BRIGHT}[!] Error accessing {full_url}: {e}{Style.RESET_ALL}"
        return result, None

if __name__ == "__main__":
    # Print the ASCII Art header in Yellow
    print(Fore.YELLOW + Style.BRIGHT + ascii_art)
    
    # Print the credit text in a styled format
    print(Fore.CYAN + Style.BRIGHT + credit_text)
    
    print(f"{Fore.WHITE + Style.BRIGHT}Reading URLs from stdin...{Style.RESET_ALL}")  # Indicator for piped input

    results = []  # List to store successful results
    successful_urls = []  # List for URLs to save

    # Read URLs from stdin (piped input)
    urls = [line.strip() for line in sys.stdin if line.strip()]

    # Process each URL sequentially
    for url in urls:
        if url:  # Skip empty lines
            result, full_url = find_admin_page(url)
            if result:
                print(result)  # Display the result in real time
                results.append(result)  # Append the result with status code
                if full_url:  # Only append the full_url if it's not None
                    successful_urls.append(full_url)

    # Save only the successful URLs (200-299 and 350+ status codes) to a fixed file name (findadmin.txt)
    if successful_urls:
        output_file = "findadmin.txt"  # Fixed output file name
        output_file_path = os.path.join(os.getcwd(), output_file)

        try:
            with open(output_file_path, "w") as file:
                # Write only the successful URLs to the file
                file.write("\n".join(successful_urls))
            print(f"{Fore.GREEN}Results saved to {output_file_path}.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Failed to save results: {e}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}No successful results to save.{Style.RESET_ALL}")

