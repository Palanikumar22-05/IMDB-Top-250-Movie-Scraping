from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import re, time
from datetime import datetime

IMDB_TOP_250_URL = "https://www.imdb.com/chart/top/"

def make_chrome():
    options = webdriver.ChromeOptions()
    # Comment out the below line if you want to see the browser window
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1366, 768)
    return driver

def safe_text(el, css):
    try:
        return el.find_element(By.CSS_SELECTOR, css).text.strip()
    except:
        return None

def parse_classic_table(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.lister-list tr")
    movies = []
    for idx, row in enumerate(rows, start=1):
        title = safe_text(row, "td.titleColumn a")
        year_raw = safe_text(row, "td.titleColumn span.secondaryInfo")
        year = None
        if year_raw:
            m = re.search(r"\((\d{4})\)", year_raw)
            year = m.group(1) if m else None
        rating = safe_text(row, "td.imdbRating strong")
        movies.append({"Rank": idx, "Title": title, "Year": year, "IMDb Rating": rating})
    return movies

def parse_modern_list(driver):
    items = driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
    movies = []
    for item in items:
        h3 = safe_text(item, "h3.ipc-title__text")  # e.g. "1. The Shawshank Redemption"
        rank, title = None, None
        if h3 and ". " in h3:
            parts = h3.split(". ", 1)
            if parts[0].isdigit():
                rank = int(parts[0])
                title = parts[1].strip()
        else:
            title = h3

        # year extract
        block_text = item.text
        year = None
        m = re.search(r"(19|20)\d{2}", block_text)
        if m:
            year = m.group(0)

        # rating
        rating = safe_text(item, "[class*='ipc-rating-star--rating']")
        movies.append({"Rank": rank, "Title": title, "Year": year, "IMDb Rating": rating})

    # Rank assign if missing
    if any(m["Rank"] is None for m in movies):
        for i, m in enumerate(movies, start=1):
            if m["Rank"] is None:
                m["Rank"] = i

    return movies

def scrape_top_250():
    driver = make_chrome()
    try:
        driver.get(IMDB_TOP_250_URL)

        # Wait until either layout loads
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tbody.lister-list tr, ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
            )
        )

        # Try classic table
        data = parse_classic_table(driver)
        if not data:  # fallback modern layout
            data = parse_modern_list(driver)

        if not data:
            raise RuntimeError("No movies found. IMDb page layout may have changed.")

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["Rank", "Title", "Year", "IMDb Rating"])
        df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df["IMDb Rating"] = pd.to_numeric(df["IMDb Rating"], errors="coerce")

        df = df.sort_values("Rank").reset_index(drop=True)

        # Save to CSV
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"imdb_top_250_{ts}.csv"
        df.to_csv(out_path, index=False, encoding="utf-8")

        return out_path, df.head(15)   # Preview top 15
    finally:
        driver.quit()

if __name__ == "__main__":
    out_csv, preview = scrape_top_250()
    print(f"✅ Data saved to: {out_csv}")
    print("\nTop Movies Preview:")
    print(preview.to_string(index=False))
