# 🧠 Crypto Insight Dashboard

An educational FastAPI project for exploring cryptocurrency metadata, 7-day trends, and recent news headlines — presented through a sleek HTML dashboard and powered by real-time data.

> ⚠️ This project is **not intended for speculation, trading, or financial advice**. It was built for learning purposes, using public APIs and open data, with help from AI.

---

## 🚀 Features

- 🔍 Fetches metadata for top 10 cryptocurrencies via the [CoinGecko API](https://www.coingecko.com/en/api)
- 📈 Shows 7-day trend (% change) for each coin
- 📰 Scrapes recent crypto news from four open-access news sources
- 🖥️ Interactive frontend built with HTML + Jinja2 templates
- 🧠 FastAPI-based backend with full CRUD API (extendable)
- 🔄 “Refresh” button pulls new data directly into the dashboard
- 🛠 Built with modular, testable Python code and Alembic migrations

---

## 🧪 Screenshots

Webpage:

<img src="https://github.com/mblystad/CryptoFastApiEDUVER/blob/master/htmlscgrab.png" width="600" alt="Html preview">

Logo:

<img src="https://github.com/mblystad/CryptoFastApiEDUVER/blob/master/app/static/logo.png" width="100" alt="logo">
---

## 📦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/crypto-insight-dashboard.git
cd crypto-insight-dashboard
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy the `.env.example` file and configure it with your own PostgreSQL connection string.

```bash
cp .env.example .env
```

Your connection string should look something like:

```
postgresql://neondb_owner:YOUR_SECRET@ep-cool-fire.neon.tech/neondb?sslmode=require
```

You can get this by signing up for a free database at [Neon.tech](https://neon.tech).

### 4. Apply database migrations

```bash
alembic upgrade head
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Then open your browser at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔄 6. Updating the Dashboard

You can update the dashboard by clicking the **"Refresh Data"** button.

This will:

* Fetch updated crypto metadata from CoinGecko
* Scrape new headlines from open news sources
* Update the database records automatically

---

## 📂 Project Structure

```text
app/
├── api/                # FastAPI endpoints
├── core/               # Logging & config
├── db/                 # SQLAlchemy base/session
├── models/             # ORM models
├── services/           # Business logic
├── scripts/            # Metadata fetching/scraping
├── static/             # CSS, images, logo
├── templates/          # HTML (Jinja2)
```

---

## 🎓 Educational Context

This project was developed:

* As an experiment in **AI-assisted software creation**
* To as a tool to learn **backend + frontend integration**
  

> 🔐 No private keys, wallet access, tokens, or speculative functionality involved.

---

## 🤖 Built With Help From

* [ChatGPT](https://chat.openai.com) — guidance, architecture, debugging
* [CoinGecko API](https://www.coingecko.com/en/api) — metadata and trends
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) — HTML scraping
* [FastAPI](https://fastapi.tiangolo.com/) — API framework
* [Neon.tech](https://neon.tech/) — PostgreSQL database hosting

---

## 📜 License

**MIT License**
Free to use, modify, and extend.
If you build on this, consider linking back to the original author 🙏

---

## ✉️ Contact

Made with curiosity by **Magnus Helgheim Blystad**.
If you’re a student or educator and want to build on this, fork it and make it better 💡

```

---
