
# Question 2 - Group 3
# 📊 CIS 9650 Project: Web Scraping & API Integration

## 🧾 Project Title
**S&P 500 Data Enrichment via Web Scraping and API Calls**


## 📘 Overview

This project demonstrates a multi-step data pipeline that includes:
- Web scraping tabular data from Wikipedia
- Using scraped values to query a public API
- Merging and analyzing data
- Exporting the final dataset to CSV and a SQL database

---

## 🧠 Project Workflow

### 🔹 Step 1: Web Scraping (DF1)
We scraped the list of **S&P 500 companies** from the following Wikipedia page:
> [List of S&P 500 Companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)

The extracted data includes:
- Ticker symbol
- Company name
- Sector
- Sub-industry
- Headquarters location
- Date first added to index
- CIK and other metadata

### 🔹 Step 2: API Querying (DF2)
Using the company **ticker symbols**, we queried a relevant API to fetch additional financial data.

Each API call returns **at least 5 data points per company**, such as:
- Market cap
- Current price
- P/E ratio
- 52-week high
- Dividend yield  
(Exact metrics depend on the API used)

### 🔹 Step 3: Merge (DF3)
We horizontally merged DF1 and DF2 to form DF3:
- This combines DataFrame includes all columns from the original table and API responses.

### 🔹 Step 4: Analysis & Export
We then:
- Displayed DF3
- Printed descriptive statistics (`df.describe()`)
- Exported the combined DataFrame to:
  - A **CSV file**
  - A **SQLite database**

---

## 🛠️ Tools & Libraries

- `pandas` – data processing
- `requests` – API communication
- `BeautifulSoup` – web scraping
- `sqlite3` – database storage
- `time`, `re`, `json`, `urllib` – utility modules

---


