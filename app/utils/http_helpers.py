import requests

def fetch_page(url: str, timeout: int = 10) -> str:
    """
    Fetch HTML content from a URL.
    
    Args:
        url (str): URL of the page to fetch
        timeout (int): timeout in seconds for the request

    Returns:
        str: HTML content
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}")
