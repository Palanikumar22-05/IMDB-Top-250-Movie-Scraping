 🎬 IMDb Top 250 Movie Scraper

A Python + Selenium project that automatically scrapes the Top 250 Movies from [IMDb](https://www.imdb.com/chart/top/), collecting each movie’s rank, title, release year, and IMDb rating.  
The data is then exported into a timestamped CSV file for easy analysis or dataset creation.

 📖 Project Overview

This project uses Selenium WebDriver to extract structured movie data from IMDb’s Top 250 Movies list.  
It intelligently handles both IMDb’s classic table and modern list layouts, ensuring long-term compatibility.

Once executed, the script:
1. Launches a headless Chrome browser
2. Scrapes all 250 movies with details
3. Saves results to `imdb_top_250_<timestamp>.csv`
4. Prints a preview of the top 15 movies in the terminal

🧠 Features

✅ Scrapes IMDb’s **Top 250** movies automatically  
✅ Works for both classic and new IMDb layouts  
✅ Exports data to a **CSV** file with timestamp  
✅ Displays a **Top 15 preview** in the console  
✅ Built using **Selenium**, **Pandas**, and **WebDriver Manager**

 🛠️ Tech Stack

- Python 3.x
- Selenium
- Pandas
- Webdriver-Manager
- Chrome WebDriver

---

📦 Installation

1. Clone this repository
   ```bash
   git clone https://github.com/Palanikumar22-05/IMDB-Top-250-Movie-Scraping.git
   cd IMDB-Top-250-Movie-Scraping
   
2.  Install dependencies

pip install -r requirements.txt

