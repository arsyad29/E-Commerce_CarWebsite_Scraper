# E-Commerce_CarWebsite_Scraper

Steps to run

- Setup for Virtual Environment in cmd
```bash
python -m venv venv
.\venv\Script\activate.bat # (for cmd)
.\venv\Script\activate.ps1 # (for vscode)
code .
cd directory_name
```

- Run These commands to run scraper

```bash
scrapy crawl scrap_mobil -o data.json # (if you want to export into json file)
scrapy crawl scrap_mobil -o data.csv # (if you want to export into csv file)
```

- Run These commands in your terminal to get all requirements package
```bash
pip install -r requirements.txt 
```
