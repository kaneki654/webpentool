#updated by goju(1)
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time

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
    "searchya", "sputnik", "teoma", "wow", "yippy", "zapmeta", "zoohoo",
    "blekko", "clusty", "cuil", "faroo", "gazelle", "guruji", "hakia",
    "icerocket", "kosmix", "mamma", "peekyou", "quintura", "scour", "sputnik",
    "surfwax", "trendiction", "wisenut", "yebol"
]

def get_proxyscrape_proxies():
    """Fetches proxies from ProxyScrape."""
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
        print(f"Failed to fetch proxies from ProxyScrape. Error: {e}")
        return []

def get_freeproxylists_proxies():
    """Fetches proxies from FreeProxyLists."""
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
        print(f"Failed to fetch proxies from FreeProxyLists. Error: {e}")
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

def format_dork(query, site=None, engine="google"):
    """
    Formats the dork based on the search engine.
    """
    if engine == "google":
        dork = f"intext:{query}"
    elif engine == "duckduckgo":
        dork = f"{query}"
    elif engine == "bing":
        dork = f"{query}"
    elif engine == "yahoo":
        dork = f"{query}"
    elif engine == "ask":
        dork = f"{query}"
    elif engine == "aol":
        dork = f"{query}"
    elif engine == "yandex":
        dork = f"{query}"
    elif engine == "baidu":
        dork = f"{query}"
    elif engine == "ecosia":
        dork = f"{query}"
    elif engine == "qwant":
        dork = f"{query}"
    elif engine == "startpage":
        dork = f"{query}"
    elif engine == "dogpile":
        dork = f"{query}"
    elif engine == "swisscows":
        dork = f"{query}"
    elif engine == "gibiru":
        dork = f"{query}"
    elif engine == "metager":
        dork = f"{query}"
    elif engine == "searx":
        dork = f"{query}"
    elif engine == "mojeek":
        dork = f"{query}"
    elif engine == "gigablast":
        dork = f"{query}"
    elif engine == "exalead":
        dork = f"{query}"
    elif engine == "lycos":
        dork = f"{query}"
    elif engine == "hotbot":
        dork = f"{query}"
    elif engine == "infospace":
        dork = f"{query}"
    elif engine == "webcrawler":
        dork = f"{query}"
    elif engine == "ixquick":
        dork = f"{query}"
    elif engine == "sogou":
        dork = f"{query}"
    elif engine == "naver":
        dork = f"{query}"
    elif engine == "daum":
        dork = f"{query}"
    elif engine == "rambler":
        dork = f"{query}"
    elif engine == "sapo":
        dork = f"{query}"
    elif engine == "virgilio":
        dork = f"{query}"
    elif engine == "alice":
        dork = f"{query}"
    elif engine == "najdi":
        dork = f"{query}"
    elif engine == "seznam":
        dork = f"{query}"
    elif engine == "biglobe":
        dork = f"{query}"
    elif engine == "goo":
        dork = f"{query}"
    elif engine == "onet":
        dork = f"{query}"
    elif engine == "szukacz":
        dork = f"{query}"
    elif engine == "pchome":
        dork = f"{query}"
    elif engine == "kvasir":
        dork = f"{query}"
    elif engine == "eniro":
        dork = f"{query}"
    elif engine == "arcor":
        dork = f"{query}"
    elif engine == "tiscali":
        dork = f"{query}"
    elif engine == "mynet":
        dork = f"{query}"
    elif engine == "ekolay":
        dork = f"{query}"
    elif engine == "search":
        dork = f"{query}"
    elif engine == "sweetsearch":
        dork = f"{query}"
    elif engine == "millionshort":
        dork = f"{query}"
    elif engine == "searchlock":
        dork = f"{query}"
    elif engine == "givero":
        dork = f"{query}"
    elif engine == "oscobo":
        dork = f"{query}"
    elif engine == "zapmeta":
        dork = f"{query}"
    elif engine == "entireweb":
        dork = f"{query}"
    elif engine == "findwide":
        dork = f"{query}"
    elif engine == "info":
        dork = f"{query}"
    elif engine == "myallsearch":
        dork = f"{query}"
    elif engine == "searchresults":
        dork = f"{query}"
    elif engine == "searchtheweb":
        dork = f"{query}"
    elif engine == "searchya":
        dork = f"{query}"
    elif engine == "sputnik":
        dork = f"{query}"
    elif engine == "teoma":
        dork = f"{query}"
    elif engine == "wow":
        dork = f"{query}"
    elif engine == "yippy":
        dork = f"{query}"
    elif engine == "zoohoo":
        dork = f"{query}"
    elif engine == "blekko":
        dork = f"{query}"
    elif engine == "clusty":
        dork = f"{query}"
    elif engine == "cuil":
        dork = f"{query}"
    elif engine == "faroo":
        dork = f"{query}"
    elif engine == "gazelle":
        dork = f"{query}"
    elif engine == "guruji":
        dork = f"{query}"
    elif engine == "hakia":
        dork = f"{query}"
    elif engine == "icerocket":
        dork = f"{query}"
    elif engine == "kosmix":
        dork = f"{query}"
    elif engine == "mamma":
        dork = f"{query}"
    elif engine == "peekyou":
        dork = f"{query}"
    elif engine == "quintura":
        dork = f"{query}"
    elif engine == "scour":
        dork = f"{query}"
    elif engine == "surfwax":
        dork = f"{query}"
    elif engine == "trendiction":
        dork = f"{query}"
    elif engine == "wisenut":
        dork = f"{query}"
    elif engine == "yebol":
        dork = f"{query}"
    else:
        dork = f"intext:{query}"  # Default to Google-style dork

    if site:
        dork += f" site:{site}"

    return dork

def search_dorks(query, site=None, engine="google", use_proxy=True, proxy_source="proxyscrape", retries=3):
    """
    Searches for dorks using the specified search engine, with optional proxy support.
    """
    dork = format_dork(query, site, engine)
    search_urls = {
        "google": f"https://www.google.com/search?q={dork}",
        "duckduckgo": f"https://html.duckduckgo.com/html/?q={dork}",
        "bing": f"https://www.bing.com/search?q={dork}",
        "yahoo": f"https://search.yahoo.com/search?p={dork}",
        "ask": f"https://www.ask.com/web?q={dork}",
        "aol": f"https://search.aol.com/aol/search?q={dork}",
        "yandex": f"https://yandex.com/search/?text={dork}",
        "baidu": f"https://www.baidu.com/s?wd={dork}",
        "ecosia": f"https://www.ecosia.org/search?q={dork}",
        "qwant": f"https://www.qwant.com/?q={dork}",
        "startpage": f"https://www.startpage.com/do/search?q={dork}",
        "dogpile": f"https://www.dogpile.com/serp?q={dork}",
        "swisscows": f"https://swisscows.com/web?query={dork}",
        "gibiru": f"https://gibiru.com/results.html?q={dork}",
        "metager": f"https://metager.org/meta/meta.ger3?eingabe={dork}",
        "searx": f"https://searx.me/search?q={dork}",
        "mojeek": f"https://www.mojeek.com/search?q={dork}",
        "gigablast": f"https://www.gigablast.com/search?q={dork}",
        "exalead": f"https://www.exalead.com/search/web/results/?q={dork}",
        "lycos": f"https://search.lycos.com/web/?q={dork}",
        "hotbot": f"https://www.hotbot.com/search/web/?q={dork}",
        "infospace": f"https://www.infospace.com/serp?q={dork}",
        "webcrawler": f"https://www.webcrawler.com/serp?q={dork}",
        "ixquick": f"https://www.ixquick.com/do/search?q={dork}",
        "sogou": f"https://www.sogou.com/web?query={dork}",
        "naver": f"https://search.naver.com/search.naver?query={dork}",
        "daum": f"https://search.daum.net/search?q={dork}",
        "rambler": f"https://nova.rambler.ru/search?query={dork}",
        "sapo": f"https://pesquisa.sapo.pt/?q={dork}",
        "virgilio": f"https://ricerca.virgilio.it/ricerca?q={dork}",
        "alice": f"https://www.alice.it/search?q={dork}",
        "najdi": f"https://www.najdi.si/search?q={dork}",
        "seznam": f"https://search.seznam.cz/?q={dork}",
        "biglobe": f"https://search.biglobe.ne.jp/cgi-bin/search?q={dork}",
        "goo": f"https://search.goo.ne.jp/web.jsp?q={dork}",
        "onet": f"https://szukaj.onet.pl/?q={dork}",
        "szukacz": f"https://www.szukacz.pl/?q={dork}",
        "pchome": f"https://ecshweb.pchome.com.tw/search/v3.3/?q={dork}",
        "kvasir": f"https://www.kvasir.no/sok?q={dork}",
        "eniro": f"https://www.eniro.se/search?q={dork}",
        "arcor": f"https://www.arcor.de/suche/?q={dork}",
        "tiscali": f"https://search.tiscali.it/?q={dork}",
        "mynet": f"https://www.mynet.com/arama?q={dork}",
        "ekolay": f"https://www.ekolay.net/arama?q={dork}",
        "search": f"https://www.search.com/search?q={dork}",
        "sweetsearch": f"https://www.sweetsearch.com/search?q={dork}",
        "millionshort": f"https://millionshort.com/search?q={dork}",
        "searchlock": f"https://www.searchlock.com/search?q={dork}",
        "givero": f"https://www.givero.com/search?q={dork}",
        "oscobo": f"https://www.oscobo.com/search?q={dork}",
        "zapmeta": f"https://www.zapmeta.com/search?q={dork}",
        "entireweb": f"https://www.entireweb.com/search?q={dork}",
        "findwide": f"https://www.findwide.com/search?q={dork}",
        "info": f"https://www.info.com/serp?q={dork}",
        "myallsearch": f"https://www.myallsearch.com/search?q={dork}",
        "searchresults": f"https://www.searchresults.com/search?q={dork}",
        "searchtheweb": f"https://www.searchtheweb.com/search?q={dork}",
        "searchya": f"https://www.searchya.com/search?q={dork}",
        "sputnik": f"https://www.sputnik.ru/search?q={dork}",
        "teoma": f"https://www.teoma.com/web?q={dork}",
        "wow": f"https://www.wow.com/search?q={dork}",
        "yippy": f"https://www.yippy.com/search?q={dork}",
        "zoohoo": f"https://www.zoohoo.com/search?q={dork}",
        "blekko": f"https://www.blekko.com/search?q={dork}",
        "clusty": f"https://www.clusty.com/search?q={dork}",
        "cuil": f"https://www.cuil.com/search?q={dork}",
        "faroo": f"https://www.faroo.com/search?q={dork}",
        "gazelle": f"https://www.gazelle.com/search?q={dork}",
        "guruji": f"https://www.guruji.com/search?q={dork}",
        "hakia": f"https://www.hakia.com/search?q={dork}",
        "icerocket": f"https://www.icerocket.com/search?q={dork}",
        "kosmix": f"https://www.kosmix.com/search?q={dork}",
        "mamma": f"https://www.mamma.com/search?q={dork}",
        "peekyou": f"https://www.peekyou.com/search?q={dork}",
        "quintura": f"https://www.quintura.com/search?q={dork}",
        "scour": f"https://www.scour.com/search?q={dork}",
        "surfwax": f"https://www.surfwax.com/search?q={dork}",
        "trendiction": f"https://www.trendiction.com/search?q={dork}",
        "wisenut": f"https://www.wisenut.com/search?q={dork}",
        "yebol": f"https://www.yebol.com/search?q={dork}"
    }
    url = search_urls.get(engine, search_urls["google"])

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
                        results.append(href)
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

def extract_form_data(url, retries=3):
    """
    Extracts form data from a given URL without using a proxy.
    """
    headers = {
        "User-Agent": ua.random  # Randomize User-Agent
    }

    for attempt in range(retries):
        try:
            print(f"Fetching form data from {url} (Attempt {attempt + 1})...")
            response = requests.get(url, headers=headers, timeout=15)  # Increased timeout
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the login form
            form = soup.find('form')
            if not form:
                print("No form found on the page.")
                return None

            # Extract form action URL
            action = form.get('action')
            if not action:
                action = url  # If no action, use the current URL

            # Extract form fields
            inputs = form.find_all('input')
            form_data = {}
            for input_tag in inputs:
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    form_data[name] = value

            return action, form_data
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)  # Increased delay before retrying
            else:
                print("Max retries reached. Giving up.")
                return None


def submit_login_form(action_url, form_data, retries=3):
    """
    Submits the login form without using a proxy.
    """
    headers = {
        "User-Agent": ua.random,  # Randomize User-Agent
        "Referer": action_url     # Set Referer to the form URL
    }

    for attempt in range(retries):
        try:
            print(f"Submitting form to {action_url} (Attempt {attempt + 1})...")
            response = requests.post(action_url, data=form_data, headers=headers, timeout=15)  # Increased timeout
            response.raise_for_status()

            print(f"Response from POST {action_url}: {response.status_code}")
            print("Response Content:")
            print(response.text)
            return
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)  # Increased delay before retrying
            else:
                print("Max retries reached. Giving up.")
                return

# Global variable to store proxies from different sources
proxies = {
    "proxyscrape": [],
    "freeproxylists": [],
    "file": []  # Proxies loaded from a file
}

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

    # Extract form data from the selected site
    result = extract_form_data(selected_url)  # Proxy is NOT used here
    if not result:
        return

    action_url, form_data = result

    # Display form data
    print("\nForm Data:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    # Update form data with user input
    for key in form_data:
        if key.lower() not in ['csrf', 'token', '_token']:  # Skip CSRF tokens
            form_data[key] = input(f"Enter value for {key}: ")

    # Submit the form
    print("\nSubmitting the form...")
    submit_login_form(action_url, form_data)  # Proxy is NOT used here

if __name__ == "__main__":
    main()
