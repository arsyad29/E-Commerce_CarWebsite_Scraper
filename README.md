# E-Commerce_CarWebsite_Scraper

Information
<br>Here's the base link: https://mobilbaru.mobil123.com/price-list
<br>What data you get is:
- Links
- Name of car
- Capacity engine
- Transmission
- Type of fuel
- Count of seats
- Price

Steps to run

- Setup for Virtual Environment in cmd
```bash
python -m venv venv
.\venv\Script\activate.bat # (for cmd)
.\venv\Script\activate.ps1 # (for vscode)
code .
cd directory_name
```

- Run These commands in your terminal to get all requirements package
```bash
pip install -r requirements.txt 
```

- Run These commands to run scraper
```bash
# Make sure before you run this command that your terminal is in directory with scrapy.cfg
scrapy crawl scrap_mobil -o data.json # (if you want to export into json file)
scrapy crawl scrap_mobil -o data.csv # (if you want to export into csv file)
```
