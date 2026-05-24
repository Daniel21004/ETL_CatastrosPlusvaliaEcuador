import traceback

from utils.remove_outliers import remove_outliers


# Extract prices and m2 of each estate
def get_data_prices_m2_all_estates(soup):
    if soup.find("h4", class_="postingsNoResults-module__title"):
        return None

    div_cards = soup.find_all("div", class_="postingCard-module__posting-top")

    data = []

    try:
        for card in div_cards:
            price = card.find("h2", class_="postingPrices-module__price")
            if price and price.string:
                txt = price.string
            else:
                txt = price.get_text()

            if "USD" not in txt:
                continue
            price = txt.split("USD")[1].strip()
            price = int(price.replace(".", ""))

            m2 = card.find(
                "span",
                class_="postingMainFeatures-module__posting-main-features-span",
                string=lambda text: text and "m²" in text,
            )
            if not m2:
                continue
            if m2 and m2.string:
                txt = m2.string
            else:
                txt = m2.get_text()

            if "a" in txt:  # Control the m2 as range e.g 107 a 185 m2 tot
                continue

            m2 = txt.split("m²")[0].strip()
            m2 = int(m2.replace(",", ""))

            data.append({"price": price, "m2": m2})
        # remove outliers
        data = remove_outliers(data, "price")
        data = remove_outliers(data, "m2")
        return data
    except Exception as e:
        print(f"OCURRIO UN ERROR. SKIP...\n{e}")
        print(traceback.format_exc())
        exit()
