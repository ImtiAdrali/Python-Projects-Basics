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
