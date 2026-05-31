import os
import random
import re
from urllib.parse import urljoin
import textwrap
import requests
from bs4 import BeautifulSoup
import csv

directory = r"templates\frenchcrown\templates\women"
filename = "womensale.csv"
FILEPARAMS = os.path.join(directory, filename)


def create_csv(filename, order):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(order)


def write_data(filename, data):
    with open(filename, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(data.keys()))
        writer.writerow(data)


def safe_text(tag, default=""):
    return tag.get_text(" ", strip=True) if tag else default


def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1", class_="product-title")
    title = safe_text(title_tag, "N/A")
    print("Title:", title)

    brand = "French Crown"
    category = "Womens"
    subcategory = "Womens Sale"
    print("Category:", category)

    compare_price_tag = soup.select_one("compare-at-price.line-through")

    if compare_price_tag:
        price = compare_price_tag.get_text(" ", strip=True)
        price = price.replace("Regular price", "").replace("₹", "").replace(",", "").strip()
    else:
        price = ""

    print("Old price:", price)

    desc_parts = []

    story = soup.find("button", string="Story")
    if story:
        story_text = story.find_next("div", class_="product-tab")
        if story_text:
            text = story_text.get_text(" ", strip=True)
            if text:
                desc_parts.append(text)

    description = soup.find("button", string="Description")
    if description:
        desc_text = description.find_next("div", class_="product-tab")
        if desc_text:
            text = desc_text.get_text(" ", strip=True)
            if text:
                desc_parts.append(text)

    extra_info = soup.select_one(".product-extra-info")
    if extra_info:
        text = extra_info.get_text(" ", strip=True)
        if text:
            desc_parts.append(text)

    # 🔥 ВАЖНО: превращаем список в чистую строку
    full_desc = " ".join(desc_parts).strip() if desc_parts else "N/A"

    print("Descriptions:", full_desc)


    BASE_URL = "https://frenchcrown.in"

    # -----------------------------
    # PRODUCT ID (оставляем твою логику, но улучшаем fallback)
    # -----------------------------
    main_image_element = soup.find("img", class_="Image--lazyLoaded")

    product_id = str(random.randint(10**8, 10**9 - 1))
    print("ID:", product_id)

    # -----------------------------
    # IMAGES (исправлено полностью)
    # -----------------------------
    slideshow_div = soup.find("div", class_="product-gallery__image-list")

    image_urls = []

    if slideshow_div:
        img_elements = slideshow_div.find_all("img")

        for img in img_elements:

            # 1. Пытаемся взять srcset (лучшее качество до 1000px)
            srcset = img.get("srcset")

            selected_url = None

            if srcset:
                candidates = []

                for part in srcset.split(","):
                    url_part = part.strip().split(" ")[0]

                    # убираем протокол
                    if url_part.startswith("//"):
                        url_part = "https:" + url_part
                    elif url_part.startswith("/"):
                        url_part = urljoin(BASE_URL, url_part)

                    # достаем width
                    match = re.search(r"width=(\d+)", url_part)
                    if match:
                        width = int(match.group(1))

                        if width <= 1000:
                            candidates.append((width, url_part))

                if candidates:
                    selected_url = max(candidates, key=lambda x: x[0])[1]

            # 2. fallback на src
            if not selected_url:
                src = img.get("src")
                if src:
                    if src.startswith("//"):
                        src = "https:" + src
                    elif src.startswith("/"):
                        src = urljoin(BASE_URL, src)

                    selected_url = src

            # 3. фильтр мусора
            if selected_url and "data:image" not in selected_url:
                image_urls.append(selected_url)

    print("Images:", image_urls)

    labels = []

    variant_picker = soup.find("variant-picker")

    if variant_picker:
        option_buttons = variant_picker.select(
            'x-listbox button[role="option"]'
        )

        for btn in option_buttons:
            size = btn.get("value", "").strip()

            # пропускаем служебную кнопку
            if size and size != "your-size-not-available":
                labels.append(size)

    print("Sizes:", labels)

    data = {
        "title": title,
        "price": price,
        "brand": brand,
        "category": category,
        "subcategory": subcategory,
        "imageurls": ", ".join(image_urls),
        "size": ", ".join(labels) if labels else "N/A",
        "description": full_desc,
        "id": product_id,
        "product_url": url,
    }

    write_data(FILEPARAMS, data)


def main():
    order = ["title", "price", "brand", "category", "subcategory", "imageurls", "size", "description", "id", "product_url"]
    create_csv(FILEPARAMS, order)

    with open(
            r"C:\Users\Admin\PycharmProjects\mother_pars\templates\frenchcrown\urls_csv\urls_women_sale.csv",
            "r",
            encoding="utf-8"
    ) as file:
        for line in csv.DictReader(file):
            url = line["url"]
            get_data(url)


if __name__ == "__main__":
    main()
