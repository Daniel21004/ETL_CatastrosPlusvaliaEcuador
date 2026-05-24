from src.extraction.plusvalia.request_plusvalia import (
    request_more_recents_plusvalia_state_html,
)
from src.extraction.plusvalia.beautifulsoup_plusvalia import create_soup
from src.transform.transform_plusvalia import get_data_prices_m2_all_estates
from urllib.parse import urlencode


class PlusvaliaScrapper:
    def __init__(self):
        self.base_url = "https://www.plusvalia.com/venta"

    def build_url(
        self, provincia=None, canton=None, property_type=None, sort="more_recent"
    ):
        # Set base url as path
        path = self.base_url

        # Check provincia
        if provincia:
            path += f"/inmuebles/{provincia.lower().replace(' ', '-')}"

        # Check
        if canton and provincia:
            path += f"/{canton.lower().replace(' ', '-')}"
        else:
            raise ValueError("Debes proporcionar una provincia")
        # Query params
        params = {"sort": sort}

        # Check property_type
        if property_type:
            #             params["propertyType"] = ",".join(map(str, property_type))
            params["propertyType"] = property_type

        return f"{path}?{urlencode(params)}"

    def fetch_html(self, url):
        html = request_more_recents_plusvalia_state_html(url=url)
        return html

    def create_soup_from_html(self, html, file_name):
        soup = create_soup(html, file_name)
        return soup

    def get_data(self, soup):
        data = get_data_prices_m2_all_estates(soup=soup)
        return data

    def pipeline(self, provincia, canton, property_type, file_name):
        url = self.build_url(
            provincia=provincia, canton=canton, property_type=property_type
        )
        print(url)
        html = self.fetch_html(url)
        soup = self.create_soup_from_html(html, file_name)
        data = self.get_data(soup=soup)
        return data
