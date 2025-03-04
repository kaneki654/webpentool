import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import re
from urllib.parse import urlparse, parse_qs

# Initialize fake_useragent
ua = UserAgent()

# List of 70 search engines
SUPPORTED_ENGINES = [
    "google", "duckduckgo", "bing", "yahoo", "ask", "aol", "yandex",
    "baidu", "ecosia", "qwant", "startpage", "dogpile", "swisscows",
    "gibiru", "metager", "searx", "mojeek", "gigablast", "exalead",
    "lycos", "hotbot", "infospace", "webcrawler", "ixquick", "sogou",
    "naver", "daum", "rambler", "sapo", "virgilio", "alice", "najdi",
    "seznam", "biglobe", "goo", "onet", "szukacz", "pchome", "kvasir",
    "eniro", "arcor", "tiscali", "mynet", "ekolay", "search", "sweetsearch",
    "millionshort", "searchlock", "givero", "oscobo", "zapmeta", "entireweb",
    "findwide", "info", "myallsearch", "searchresults", "searchtheweb",
    "searchya", "sputnik", "teoma", "wow", "yippy", "zoohoo", "blekko",
    "clusty", "cuil", "faroo", "gazelle", "guruji", "hakia", "icerocket",
    "kosmix", "mamma", "peekyou", "quintura", "scour", "surfwax", "trendiction",
    "wisenut", "yebol"
]

# Global proxies dictionary
proxies = {
    "proxyscrape": [],
    "freeproxylists": [],
    "file": []
}

# Dork Formats
DORK_FORMATS = {
    "google": "intext:{query} intext:login",
    "duckduckgo": "{query} login",
    "bing": "{query} login",
    "yahoo": "{query} login",
    "ask": "{query} login",
    "aol": "{query} login",
    "yandex": "{query} login",
    "baidu": "{query} login",
    "ecosia": "{query} login",
    "qwant": "{query} login",
    "startpage": "{query} login",
    "dogpile": "{query} login",
    "swisscows": "{query} login",
    "gibiru": "{query} login",
    "metager": "{query} login",
    "searx": "{query} login",
    "mojeek": "{query} login",
    "gigablast": "{query} login",
    "exalead": "{query} login",
    "lycos": "{query} login",
    "hotbot": "{query} login",
    "infospace": "{query} login",
    "webcrawler": "{query} login",
    "ixquick": "{query} login",
    "sogou": "{query} login",
    "naver": "{query} login",
    "daum": "{query} login",
    "rambler": "{query} login",
    "sapo": "{query} login",
    "virgilio": "{query} login",
    "alice": "{query} login",
    "najdi": "{query} login",
    "seznam": "{query} login",
    "biglobe": "{query} login",
    "goo": "{query} login",
    "onet": "{query} login",
    "szukacz": "{query} login",
    "pchome": "{query} login",
    "kvasir": "{query} login",
    "eniro": "{query} login",
    "arcor": "{query} login",
    "tiscali": "{query} login",
    "mynet": "{query} login",
    "ekolay": "{query} login",
    "search": "{query} login",
    "sweetsearch": "{query} login",
    "millionshort": "{query} login",
    "searchlock": "{query} login",
    "givero": "{query} login",
    "oscobo": "{query} login",
    "zapmeta": "{query} login",
    "entireweb": "{query} login",
    "findwide": "{query} login",
    "info": "{query} login",
    "myallsearch": "{query} login",
    "searchresults": "{query} login",
    "searchtheweb": "{query} login",
    "searchya": "{query} login",
    "sputnik": "{query} login",
    "teoma": "{query} login",
    "wow": "{query} login",
    "yippy": "{query} login",
    "zoohoo": "{query} login",
    "blekko": "{query} login",
    "clusty": "{query} login",
    "cuil": "{query} login",
    "faroo": "{query} login",
    "gazelle": "{query} login",
    "guruji": "{query} login",
    "hakia": "{query} login",
    "icerocket": "{query} login",
    "kosmix": "{query} login",
    "mamma": "{query} login",
    "peekyou": "{query} login",
    "quintura": "{query} login",
    "scour": "{query} login",
    "surfwax": "{query} login",
    "trendiction": "{query} login",
    "wisenut": "{query} login",
    "yebol": "{query} login"
}

# Search Engine URLs
SEARCH_URLS = {
    "google": "https://www.google.com/search?q={dork}",
    "duckduckgo": "https://html.duckduckgo.com/html/?q={dork}",
    "bing": "https://www.bing.com/search?q={dork}",
    "yahoo": "https://search.yahoo.com/search?p={dork}",
    "ask": "https://www.ask.com/web?q={dork}",
    "aol": "https://search.aol.com/aol/search?q={dork}",
    "yandex": "https://yandex.com/search/?text={dork}",
    "baidu": "https://www.baidu.com/s?wd={dork}",
    "ecosia": "https://www.ecosia.org/search?q={dork}",
    "qwant": "https://www.qwant.com/?q={dork}",
    "startpage": "https://www.startpage.com/do/search?q={dork}",
    "dogpile": "https://www.dogpile.com/serp?q={dork}",
    "swisscows": "https://swisscows.com/web?query={dork}",
    "gibiru": "https://gibiru.com/results.html?q={dork}",
    "metager": "https://metager.org/meta/meta.ger3?eingabe={dork}",
    "searx": "https://searx.me/search?q={dork}",
    "mojeek": "https://www.mojeek.com/search?q={dork}",
    "gigablast": "https://www.gigablast.com/search?q={dork}",
    "exalead": "https://www.exalead.com/search/web/results/?q={dork}",
    "lycos": "https://search.lycos.com/web/?q={dork}",
    "hotbot": "https://www.hotbot.com/search/web/?q={dork}",
    "infospace": "https://www.infospace.com/serp?q={dork}",
    "webcrawler": "https://www.webcrawler.com/serp?q={dork}",
    "ixquick": "https://www.ixquick.com/do/search?q={dork}",
    "sogou": "https://www.sogou.com/web?query={dork}",
    "naver": "https://search.naver.com/search.naver?query={dork}",
    "daum": "https://search.daum.net/search?q={dork}",
    "rambler": "https://nova.rambler.ru/search?query={dork}",
    "sapo": "https://pesquisa.sapo.pt/?q={dork}",
    "virgilio": "https://ricerca.virgilio.it/ricerca?q={dork}",
    "alice": "https://www.alice.it/search?q={dork}",
    "najdi": "https://www.najdi.si/search?q={dork}",
    "seznam": "https://search.seznam.cz/?q={dork}",
    "biglobe": "https://search.biglobe.ne.jp/cgi-bin/search?q={dork}",
    "goo": "https://search.goo.ne.jp/web.jsp?q={dork}",
    "onet": "https://szukaj.onet.pl/?q={dork}",
    "szukacz": "https://www.szukacz.pl/?q={dork}",
    "pchome": "https://ecshweb.pchome.com.tw/search/v3.3/?q={dork}",
    "kvasir": "https://www.kvasir.no/sok?q={dork}",
    "eniro": "https://www.eniro.se/search?q={dork}",
    "arcor": "https://www.arcor.de/suche/?q={dork}",
    "tiscali": "https://search.tiscali.it/?q={dork}",
    "mynet": "https://www.mynet.com/arama?q={dork}",
    "ekolay": "https://www.ekolay.net/arama?q={dork}",
    "search": "https://www.search.com/search?q={dork}",
    "sweetsearch": "https://www.sweetsearch.com/search?q={dork}",
    "millionshort": "https://millionshort.com/search?q={dork}",
    "searchlock": "https://www.searchlock.com/search?q={dork}",
    "givero": "https://www.givero.com/search?q={dork}",
    "oscobo": "https://www.oscobo.com/search?q={dork}",
    "zapmeta": "https://www.zapmeta.com/search?q={dork}",
    "entireweb": "https://www.entireweb.com/search?q={dork}",
    "findwide": "https://www.findwide.com/search?q={dork}",
    "info": "https://www.info.com/serp?q={dork}",
    "myallsearch": "https://www.myallsearch.com/search?q={dork}",
    "searchresults": "https://www.searchresults.com/search?q={dork}",
    "searchtheweb": "https://www.searchtheweb.com/search?q={dork}",
    "searchya": "https://www.searchya.com/search?q={dork}",
    "sputnik": "https://www.sputnik.ru/search?q={dork}",
    "teoma": "https://www.teoma.com/web?q={dork}",
    "wow": "https://www.wow.com/search?q={dork}",
    "yippy": "https://www.yippy.com/search?q={dork}",
    "zoohoo": "https://www.zoohoo.com/search?q={dork}",
    "blekko": "https://www.blekko.com/search?q={dork}",
    "clusty": "https://www.clusty.com/search?q={dork}",
    "cuil": "https://www.cuil.com/search?q={dork}",
    "faroo": "https://www.faroo.com/search?q={dork}",
    "gazelle": "https://www.gazelle.com/search?q={dork}",
    "guruji": "https://www.guruji.com/search?q={dork}",
    "hakia": "https://www.hakia.com/search?q={dork}",
    "icerocket": "https://www.icerocket.com/search?q={dork}",
    "kosmix": "https://www.kosmix.com/search?q={dork}",
    "mamma": "https://www.mamma.com/search?q={dork}",
    "peekyou": "https://www.peekyou.com/search?q={dork}",
    "quintura": "https://www.quintura.com/search?q={dork}",
    "scour": "https://www.scour.com/search?q={dork}",
    "surfwax": "https://www.surfwax.com/search?q={dork}",
    "trendiction": "https://www.trendiction.com/search?q={dork}",
    "wisenut": "https://www.wisenut.com/search?q={dork}",
    "yebol": "https://www.yebol.com/search?q={dork}"
}

# Proxy functions (with retry mechanism)
def get_proxyscrape_proxies(retries=3):
    """Fetches proxies from ProxyScrape with retries."""
    for attempt in range(retries):
        try:
            response = requests.get(
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
                timeout=10
            )
            response.raise_for_status()
            proxies = response.text.strip().split("\r\n")
            print(f"Fetched {len(proxies)} proxies from ProxyScrape.")
            return proxies
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to fetch proxies from ProxyScrape. Error: {e}")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                print("Max retries reached. Giving up on ProxyScrape.")
                return []

def get_freeproxylists_proxies(retries=3):
    """Fetches proxies from FreeProxyLists with retries."""
    for attempt in range(retries):
        try:
            response = requests.get("https://free-proxy-list.net/", headers={'User-Agent': ua.random}, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"id": "proxylisttable"})
            proxies = []
            for row in table.find_all("tr")[1:]:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    ip = cells[0].text.strip()
                    port = cells[1].text.strip()
                    proxies.append(f"{ip}:{port}")
            print(f"Fetched {len(proxies)} proxies from FreeProxyLists.")
            return proxies
        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to fetch proxies from FreeProxyLists. Error: {e}")
            if attempt < retries - 1:
                time.sleep(5)
            else:
                print("Max retries reached. Giving up on FreeProxyLists.")
                return []

def get_proxies_from_file(filepath="proxies.txt"):
    """Loads proxies from a text file."""
    try:
        with open(filepath, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(proxies)} proxies from file {filepath}.")
        return proxies
    except FileNotFoundError:
        print(f"Proxy file not found: {filepath}")
        return []
    except Exception as e:
        print(f"Error reading proxy file: {e}")
        return []

def get_random_proxy(proxy_source="proxyscrape"):
    """
    Fetches a random proxy from the specified source.
    """
    global proxies  # Access the global proxies list

    if proxy_source == "proxyscrape":
        if not proxies["proxyscrape"]:  # Refetch if empty
            proxies["proxyscrape"] = get_proxyscrape_proxies()
        proxy_list = proxies["proxyscrape"]
    elif proxy_source == "freeproxylists":
        if not proxies["freeproxylists"]:  # Refetch if empty
            proxies["freeproxylists"] = get_freeproxylists_proxies()
        proxy_list = proxies["freeproxylists"]
    elif proxy_source == "file":
        if not proxies["file"]:  # Refetch if empty
            proxies["file"] = get_proxies_from_file()
        proxy_list = proxies["file"]
    else:
        print("Invalid proxy source specified.")
        return None

    if proxy_list:
        return random.choice(proxy_list)
    else:
        print(f"No proxies available from {proxy_source}.")
        return None

# Dork formatting and search functions
def format_dork(query, site=None, engine="google"):
    """Formats the dork based on the search engine."""
    dork = DORK_FORMATS.get(engine, "intext:{query} intext:login").format(query=query)
    if site:
        dork += f" site:{site}"
    return dork

def search_dorks(query, site=None, engine="google", use_proxy=True, proxy_source="proxyscrape", retries=3):
    """Searches for dorks using the specified search engine, with optional proxy support."""
    dork = format_dork(query, site, engine)
    url = SEARCH_URLS.get(engine, SEARCH_URLS["google"]).format(dork=dork)

    headers = {
        "User-Agent": ua.random
    }

    for attempt in range(retries):
        proxy = None
        proxies = None

        if use_proxy:
            proxy = get_random_proxy(proxy_source)
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None

        try:
            print(
                f"Fetching results from {engine.capitalize()} (Attempt {attempt + 1}), using proxy: {proxy if use_proxy else 'No Proxy'}")
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
            response.raise_for_status()

            if "captcha" in response.text.lower() or "sorry" in response.text.lower():
                print(f"{engine.capitalize()} is showing a CAPTCHA.")
                return None

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            if engine == "duckduckgo":
                for link in soup.find_all('a', class_='result__url'):
                    href = link.get('href')
                    if href:
                        # Extract the actual URL from the uddg parameter
                        parsed_url = urlparse(href)
                        query_params = parse_qs(parsed_url.query)
                        if 'uddg' in query_params:
                            actual_url = query_params['uddg'][0]
                            results.append(actual_url)
            elif engine == "google":
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and "url?q=" in href and not "webcache" in href:
                        results.append(href.split("url?q=")[1].split("&")[0])
            elif engine == "bing":
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and "http" in href and not "bing.com" in href:
                        if "go.microsoft.com" not in href:
                            results.append(href)
            elif engine in ["yahoo", "ask", "aol", "yandex", "baidu", "ecosia", "qwant", "startpage", "dogpile", "swisscows", "gibiru", "metager", "searx", "mojeek", "gigablast", "exalead", "lycos", "hotbot", "infospace", "webcrawler", "ixquick", "sogou", "naver", "daum", "rambler", "sapo", "virgilio", "alice", "najdi", "seznam", "biglobe", "goo", "onet", "szukacz", "pchome", "kvasir", "eniro", "arcor", "tiscali", "mynet", "ekolay", "search", "sweetsearch", "millionshort", "searchlock", "givero", "oscobo", "zapmeta", "entireweb", "findwide", "info", "myallsearch", "searchresults", "searchtheweb", "searchya", "sputnik", "teoma", "wow", "yippy", "zoohoo", "blekko", "clusty", "cuil", "faroo", "gazelle", "guruji", "hakia", "icerocket", "kosmix", "mamma", "peekyou", "quintura", "scour", "surfwax", "trendiction", "wisenut", "yebol"]:
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and "http" in href:
                        results.append(href)

            return results
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)
            else:
                print("Max retries reached. Giving up.")
                return None

# New functions for DebugBar and sensitive data extraction
def fetch_page_content(url):
    """Fetch the HTML content of the page."""
    headers = {
        "User-Agent": ua.random
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page content. Error: {e}")
        return None

def parse_debugbar_data(html):
    """Parse the HTML to extract DebugBar data."""
    soup = BeautifulSoup(html, "html.parser")

    # Look for DebugBar-specific elements (adjust selectors as needed)
    debugbar = soup.find("div", class_="phpdebugbar")
    if not debugbar:
        print("DebugBar not found in the HTML.")
        return None

    # Extract DebugBar content
    debugbar_content = debugbar.get_text(strip=True)
    print("DebugBar Content:")
    print(debugbar_content)
    return debugbar_content

def detect_login_endpoints(html):
    """Detect /login endpoints in the HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Look for forms with action containing /login
    login_forms = []
    for form in soup.find_all("form"):
        action = form.get("action", "").lower()
        if "/login" in action or "login" in action:
            login_forms.append(form)

    # Look for links pointing to /login
    login_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        if "/login" in href or "login" in href:
            login_links.append(link)

    return login_forms, login_links

def extract_sensitive_data(html):
    """Extract sensitive data (e.g., passwords, emails, usernames) from the HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Look for input fields related to authentication
    sensitive_data = {}
    for input_tag in soup.find_all("input"):
        input_name = input_tag.get("name", "").lower()
        input_type = input_tag.get("type", "").lower()
        input_value = input_tag.get("value", "")

        if "password" in input_name or input_type == "password":
            sensitive_data["password"] = input_value
        elif "email" in input_name or input_type == "email":
            sensitive_data["email"] = input_value
        elif "username" in input_name or "user" in input_name:
            sensitive_data["username"] = input_value

    # Use regular expressions to find patterns resembling emails, usernames, and passwords
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    username_pattern = r'\b[A-Za-z0-9_-]{3,16}\b'
    password_pattern = r'\b(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}\b'  # Example pattern: min 8 chars, 1 letter, 1 number

    # Find all matches in the HTML source
    emails = re.findall(email_pattern, html)
    usernames = re.findall(username_pattern, html)
    passwords = re.findall(password_pattern, html)

    # Add the found patterns to the sensitive_data dictionary
    if emails:
        sensitive_data["emails_found"] = emails
    if usernames:
        sensitive_data["usernames_found"] = usernames
    if passwords:
        sensitive_data["passwords_found"] = passwords

    return sensitive_data

# Main function
def main():
    global proxies
    query = "php debugbar"  # Base query without dork syntax
    site = input("Enter site (optional): ").strip()

    # Choose proxy source
    print("\nChoose a proxy source:")
    print("1. ProxyScrape (default)")
    print("2. FreeProxyLists")
    print("3. Load from file (proxies.txt)")
    print("4. No proxy")

    proxy_choice = input("Enter your choice (1-4): ").strip()

    use_proxy = True
    proxy_source = "proxyscrape"  # Default
    if proxy_choice == "2":
        proxy_source = "freeproxylists"
    elif proxy_choice == "3":
        proxy_source = "file"
    elif proxy_choice == "4":
        use_proxy = False
        print("Proxy usage disabled.")
    else:
        print("Using ProxyScrape as default.")

    if use_proxy:
        # Initial fetch of proxies
        if proxy_source == "proxyscrape":
            proxies["proxyscrape"] = get_proxyscrape_proxies()
        elif proxy_source == "freeproxylists":
            proxies["freeproxylists"] = get_freeproxylists_proxies()
        elif proxy_source == "file":
            proxies["file"] = get_proxies_from_file()

    # Try each search engine in order
    for engine in SUPPORTED_ENGINES:
        print(f"\nTrying {engine.capitalize()}...")
        results = search_dorks(query, site, engine, use_proxy, proxy_source)
        if results:
            print(f"Found {len(results)} results on {engine.capitalize()}.")
            break
        else:
            print(f"No results found on {engine.capitalize()} or request blocked.")
        time.sleep(5)

    else:
        print("All search engines failed. Exiting.")
        return

    # Display search results
    print("\nSearch results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")

    # Let the user select a site
    try:
        choice = int(input("Enter the number of the site you want to explore: ")) - 1
        selected_url = results[choice]
        print(f"\nSelected URL: {selected_url}")
    except (IndexError, ValueError):
        print("Invalid choice. Exiting.")
        return

    # Fetch and parse the selected URL
    html = fetch_page_content(selected_url)
    if not html:
        return

    # Parse DebugBar data
    debugbar_data = parse_debugbar_data(html)
    if debugbar_data:
        print("\nDebugBar data extracted successfully.")

    # Detect /login endpoints
    login_forms, login_links = detect_login_endpoints(html)
    if login_forms:
        print("\nDetected login forms:")
        for form in login_forms:
            print(f"Form action: {form.get('action')}")
    if login_links:
        print("\nDetected login links:")
        for link in login_links:
            print(f"Link href: {link['href']}")

    # Extract sensitive data
    sensitive_data = extract_sensitive_data(html)
    if sensitive_data:
        print("\nExtracted sensitive data:")
        for key, value in sensitive_data.items():
            print(f"{key}: {value}")
    else:
        print("\nNo sensitive data found.")

if __name__ == "__main__":
    main()
