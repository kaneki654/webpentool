import httpx  
import os
import re
import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def print_centered(text):
    terminal_width = os.get_terminal_size().columns
    for line in text.split("\n"):
        print(line.center(terminal_width))

banner = """

███    ███  █████  ███████ ███████       ██████  ███████ ██    ██ ███████ ██████  ███████ ███████ 
████  ████ ██   ██ ██      ██            ██   ██ ██      ██    ██ ██      ██   ██ ██      ██      
██ ████ ██ ███████ ███████ ███████ █████ ██████  █████   ██    ██ █████   ██████  ███████ █████   
██  ██  ██ ██   ██      ██      ██       ██   ██ ██       ██  ██  ██      ██   ██      ██ ██      
██      ██ ██   ██ ███████ ███████       ██   ██ ███████   ████   ███████ ██   ██ ███████ ███████ 
                                                                                                  
                                                                                                  by zhen   
"""

def loading_animation(event):
    chars = ["|", "/", "-", "\\"]
    i = 0
    while not event.is_set():
        print(f"\033[1;36mProcessing... {chars[i % len(chars)]}\033[0m", end="\r")
        time.sleep(0.2)
        i += 1
    print(" " * 20, end="\r")  # Clear loading text

async def check_domain_status(domain, client):
    try:
        response = await client.head(domain, timeout=3, follow_redirects=True)
        return response.status_code == 200
    except httpx.RequestError:
        return False

async def process_domains(ip, domains):
    async with httpx.AsyncClient() as client:
        tasks = [check_domain_status(f"http://{domain}", client) for domain in domains]
        results = await asyncio.gather(*tasks)

    live_domains = [f"http://{domains[i]}" for i in range(len(domains)) if results[i]]
    
    with open('rev.txt', 'a') as file:
        file.write(f"IP: {ip}\n")
        file.write("\n".join(live_domains) + '\n\n')
    
    current_time = datetime.now().strftime("%H:%M:%S")
    if live_domains:
        print(f"\033[1;37m[{current_time}] \033[1;32m[✓] \033[1;33mDomains for IP \033[1;32m{ip}:\033[0m")
        for domain in live_domains:
            print(f"\033[1;34m{domain}\033[0m")
    else:
        print(f"\033[1;37m[{current_time}] \033[1;31m[✗] \033[1;33mNo live domains for \033[1;31m{ip}\033[0m")

def fetch_domains(ip):
    headers = {'User-Agent': 'Mozilla/5.0'}
    domains = set()
    
    try:
        res = httpx.get(f'https://rapiddns.io/s/{ip}?full=1&down=1#result/', headers=headers, timeout=8)
        res.raise_for_status()
        domains.update(re.findall(r'<td>([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})</td>', res.text))
    except httpx.RequestError:
        pass
    
    try:
        res = httpx.get(f'https://api.reverseipdomain.com/?ip={ip}', headers=headers, timeout=8)
        res.raise_for_status()
        domains.update(re.findall(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', res.text))
    except httpx.RequestError:
        pass
    
    if domains:
        asyncio.run(process_domains(ip, list(domains)))
    else:
        print(f"\033[1;31mNo domains found for {ip}\033[0m")

def main():
    os.system("cls" if os.name == "nt" else "clear")  
    print_centered(banner) 

    file_path = input("\033[1;37mEnter the file containing IPs\033[0m:\033[1;34m ")
    
    try:
        with open(file_path, 'r') as file:
            ip_list = file.read().splitlines()
        
        num_threads = int(input("\033[1;37mEnter number of threads\033[0m:\033[1;34m "))
        
        stop_event = threading.Event()
        loader_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loader_thread.start()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(fetch_domains, ip_list)
        
        stop_event.set()
        loader_thread.join()

    except FileNotFoundError:
        print(f"\033[1;31mError: File {file_path} not found!\033[0m")
    except ValueError:
        print("\033[1;31mError: Invalid number of threads!\033[0m")
    except Exception as e:
        print(f"\033[1;31mUnexpected error: {e}\033[0m")

if __name__ == '__main__':
    main()
