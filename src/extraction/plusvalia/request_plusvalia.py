# cloudscrapper para saltar la protección de cloudfare
import cloudscraper
from config import BASE_URL


# Download HTML plusvalia (more recents posts)
def request_more_recents_plusvalia_state_html(url=BASE_URL):
    scraper = cloudscraper.create_scraper()
    html = scraper.get(url)
    return html
