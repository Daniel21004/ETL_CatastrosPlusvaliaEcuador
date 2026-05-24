from pathlib import Path
from bs4 import BeautifulSoup


# Create the soup with http response request
def create_soup(html, save_file="plusvalia.html"):
    file = Path(f"data/raw/plusvalia/{save_file}")

    if file.exists():
        print("Loanding HTML file... ")
        with open(file, "r", encoding="utf-8") as f:
            resp = f.read()
    else:
        print("Save HTML file... ")
        resp = html.text
        with open(file, "w", encoding="utf-8") as f:
            f.write(resp)

    soup = BeautifulSoup(resp, "lxml")
    return soup
