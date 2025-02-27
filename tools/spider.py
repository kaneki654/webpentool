import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def choice():
    er = input('Enter a domain (include http:// or https://): ')
    return er  # Return the user input

class AdvancedCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.vulnerabilities = []
        self.crawled_urls = []  # To store crawled URLs for logging

    def crawl(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        self.crawled_urls.append(url)  # Log the URL being crawled
        print(f"Crawling: {url}")  # Print the URL being crawled

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.analyze_content(url, response.text)
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    if self.base_url in full_url and full_url not in self.visited_urls:
                        self.crawl(full_url)
        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")

    def analyze_content(self, url, content):
        self.detect_sql_injection(url, content)
        self.detect_xss(url, content)
        self.detect_sensitive_data_exposure(url, content)
        self.detect_insecure_forms(url, content)

    def detect_sql_injection(self, url, content):
        # Look for common SQL injection patterns in forms or URLs
        if re.search(r"select\s.*from|insert\s.*into|update\s.*set|delete\s.*from", content, re.IGNORECASE):
            self.vulnerabilities.append(f"Potential SQL Injection vulnerability detected at {url}")

    def detect_xss(self, url, content):
        # Look for potential XSS vulnerabilities in forms or scripts
        if re.search(r"<script>|javascript:|onerror=|onload=", content, re.IGNORECASE):
            self.vulnerabilities.append(f"Potential XSS vulnerability detected at {url}")

    def detect_sensitive_data_exposure(self, url, content):
        # Look for sensitive data like API keys, passwords, etc.
        if re.search(r"api_key|password|secret|token", content, re.IGNORECASE):
            self.vulnerabilities.append(f"Potential Sensitive Data Exposure detected at {url}")

    def detect_insecure_forms(self, url, content):
        # Look for forms without CSRF tokens or using HTTP
        if re.search(r"<form.*action=\"http://", content, re.IGNORECASE):
            self.vulnerabilities.append(f"Insecure form detected at {url} (HTTP instead of HTTPS)")
        if not re.search(r"csrf_token|csrfmiddlewaretoken", content, re.IGNORECASE):
            self.vulnerabilities.append(f"Potential CSRF vulnerability detected at {url} (Missing CSRF token)")

    def report_vulnerabilities(self):
        if self.vulnerabilities:
            print("Potential vulnerabilities found:")
            for vuln in self.vulnerabilities:
                print(f"- {vuln}")
        else:
            print("No vulnerabilities detected.")

    def report_crawled_urls(self):
        print("\nCrawled URLs:")
        for url in self.crawled_urls:
            print(f"- {url}")


if __name__ == "__main__":
    target_url = choice()  # Get the target website from user input
    crawler = AdvancedCrawler(target_url)
    crawler.crawl(target_url)
    crawler.report_vulnerabilities()
    crawler.report_crawled_urls()  # Display all crawled URLs