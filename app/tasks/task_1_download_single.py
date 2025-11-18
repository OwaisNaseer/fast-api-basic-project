from app.utils.http_helpers import fetch_page
from app.utils.file_helpers import save_to_file

def run_task():
    url = "https://example.com"
    html = fetch_page(url)
    save_to_file(html, "downloads/example.html")
    print("Page downloaded successfully!")

if __name__ == "__main__":
    run_task()
