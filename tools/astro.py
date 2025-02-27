from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
try:
    from fake_useragent import UserAgent
    from colorama import Fore, Style, init
    from bs4 import BeautifulSoup
    from tqdm import tqdm
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    os.system('pip install fake_useragent colorama beautifulsoup4 tqdm concurrent')
    os.system('python astro.py')
# Initialize colorama
init()

# ASCII Art with Yellow Color and Red Credits
print(Fore.YELLOW + r"""
    _        _            ____                                  
   / \   ___| |_ _ __ ___/ ___|  ___ __ _ _ __  _ __   ___ _ __ 
  / _ \ / __| __| '__/ _ \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 / ___ \\__ \ |_| | | (_) |__) | (_| (_| | | | | | | |  __/ |   
/_/   \_\___/\__|_|  \___/____/ \___\__,_|_| |_|_| |_|\___|_|                                                                                                                                   
""" + Fore.RED + r"""
                                                            
TheNexusSquad Reverse IP Scanner
tags:
MR.SEND0 | GOJU.VBS
""" + Style.RESET_ALL)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

fbi = UserAgent()

def get_status_code(domain, proxy=None):
    """Fetch the HTTP/HTTPS status code for a given domain, always using HTTP in the output."""
    urls = [f"http://{domain}", f"https://{domain}"]  # Check both HTTP and HTTPS
    status_codes = []
    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": fbi.random}, timeout=5, proxies=proxy)
            status_codes.append((url, response.status_code))  # Add both URL and status code
        except requests.RequestException:
            continue
    return status_codes  # Return list of tuples with URL and status code

def color_status_code(status):
    """Return the appropriate color for the status code."""
    if 200 <= status < 300:
        return Fore.GREEN + f"HTTP {status}" + Style.RESET_ALL
    elif 300 <= status < 400:
        return Fore.YELLOW + f"HTTP {status}" + Style.RESET_ALL
    elif 400 <= status < 500:
        return Fore.RED + f"HTTP {status}" + Style.RESET_ALL
    elif 500 <= status < 600:
        return Fore.CYAN + f"HTTP {status}" + Style.RESET_ALL
    else:
        return Fore.WHITE + f"HTTP {status}" + Style.RESET_ALL

def reverse_jutsu(ip_jutsu, proxy=None):
    taiju = f"https://viewdns.info/reverseip/?host={ip_jutsu}&t=1"
    gentu = {
        "User-Agent": fbi.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://viewdns.info/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin"
    }

    session = requests.Session()
    session.headers.update(gentu)

    try:
        response = session.get(taiju, proxies=proxy)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', border="1")

        if not table:
            print("WALANG NAKITA.")
            return []

        rows = table.find_all('tr')[1:]  # Skip the header row
        domains = [row.find_all('td')[0].text.strip() for row in rows]

        return domains

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)
        return []

def filter_domains(domains, keyword):
    """Filter domains based on a keyword."""
    return [domain for domain in domains if keyword.lower() in domain.lower()]

def main():
    wow = input("INPUT THE IP ADDRESS OR DOMAIN : ").strip()
    use_proxy = input("Do you want to use a proxy? (y/n): ").strip().lower()
    proxy = None
    if use_proxy == 'y':
        proxy_url = input("Enter your proxy (e.g., http://127.0.0.1:8080): ").strip()
        proxy = {
            "http": proxy_url,
            "https": proxy_url
        }

    clear()
    print("\nCURSE TECHNIQUE..")
    time.sleep(2)
    clear()
    print("\nLAPSE...")
    domains = reverse_jutsu(wow, proxy)

    if domains:
        clear()
        print("\nBLUE!!")
        print(f"{wow}\n")

        keyword = input("Enter a keyword to filter domains (leave blank to skip): ").strip()
        if keyword:
            domains = filter_domains(domains, keyword)

        save_to_file = input("Do you want to save the results to a file? (y/n): ").strip().lower()
        output_file = f"{wow.replace('.', '_')}.txt" if save_to_file == 'y' else None
        

        print("\nFetching domains, please wait...\n")

        try:
            # Use ThreadPoolExecutor to fetch status codes concurrently
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {executor.submit(get_status_code, domain, proxy): domain for domain in domains}

                # Create a progress bar at the bottom
                results = []
                with tqdm(total=len(domains), desc="Fetching Domains", unit="domain", position=0, leave=True) as pbar:
                    for future in futures:
                        domain = futures[future]
                        try:
                            status_codes = future.result()
                            results.extend(status_codes)  # Store results for later
                        except Exception as e:
                            print(Fore.RED + f"Error fetching status for {domain}: {e}" + Style.RESET_ALL)
                        finally:
                            pbar.update(1)  # Update the progress bar

            # After the progress bar is complete, print all results
            clear()
            print("\nFetching complete! Displaying results:\n")
            for url, status in results:
                print(Fore.LIGHTYELLOW_EX + url + Style.RESET_ALL + " - " + color_status_code(status))
                if output_file:
                    with open(output_file, 'a') as file:
                        file.write(f"{url} - HTTP {status}\n")

            if output_file:
                print(Fore.GREEN + f"\nResults saved to {output_file}" + Style.RESET_ALL)

        except KeyboardInterrupt:
            use = input('do you want to exit?(y/n): ').strip().lower()
            if use == 'y':
                exit()
            if use == 'n':
                main()
    else:
        print(f"\nOUT OF CURSE ENERGY")

if __name__ == "__main__":
    main()