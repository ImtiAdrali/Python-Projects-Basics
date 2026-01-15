# :etch web pages with error handling

import requests
from time import sleep
import random

DEFAULT_HEADER = {
    "User-Agent": "Mozila/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_page(url, timeout = 10, retries = 3):
    """
        Fetch a web page with error handling and retries.

        Args: 
            url (str): URL to fetch
            timeout (int): Request timeout in seconds
            retries (int): Number of retry attempts

        Returns:
            str: HTML content of the page

        Raises:
            requrests.RequestException: if all retries fail 
            ValueError: If URL is invalid
    """

    if not url or not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL: {url}")

    for attempt in range(retries):
        try:
            print(f"Fetching: {url} (attempt {attempt + 1} / {retries})")

            response = requests.get(
                url,
                headers = DEFAULT_HEADER,
                timeout = timeout
            )

            response.raise_for_status()

            print(f"Successfully fetched {url}")
            return response.text 

        except requests.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < retries - 1:
                sleep(2 ** attempt)

        except retries.ConnectionError as e:
            print(f"Connection error: {e}")
            if attempt < retries - 1:
                sleep(2 ** attempt)

        except requests.HTTPError as e:
            print(f"HTTP error {response.status_code}: {e}")
            return
        
        except requests.RequestException as e:
            print(f"Request failed: {r}")
            if attempt >= retries - 1:
                raise
            
    return requests.RequestException(f"Failed to fetch {url} after {retries} attempts.")


def fetch_multiple_pages(urls, delay = 1):
    """
        Fetch multiple pages with polite delays.

        Args:
            urls (list): list of urls to fetch
            delay (int): Delay between requests in seconds

        Returns:
            dict: { url: html_content } for successful fetches  
    """

    results = {}
    
    for i, url in enumerate(urls):
        try:
            html = fetch_page(url)
            results[url] = html

            if i < len(urls) - 1:
                sleep_time = delay + random.uniform(0, 1)
                print(f"Waiting {sleep_time:.1f}s before next request...")
                sleep(sleep_time)

        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            results[url] = None


    return results


def check_robots_txt(domain):
    """
        Check if scraping is allowed (basic check).

        Args:
            domain (str): Domain to check (e.g. 'example.com')

        Returns:
            bool: True if appears to be allowed

    """

    try:
        robot_url = f"https://{domain}/robots.txt"
        response = requrests.get(robot_url, timeout = 5)

        if response.status_code == 200:
            print(f"Found robots.txt for {domain}")
            print("Please review robots.txt befor scraping:")
            print(response.text[:500])
            return True

        print(f"No robots.txt found for {domain}")
        return True

    except Exception as ex:
        print(f"Could not check robots.txt: {ex}")
        return True
