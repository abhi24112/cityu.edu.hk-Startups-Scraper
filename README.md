# CityU HKTech300 StartUps Extractor 🚀

A powerful web scraping tool to extract startup information from the CityU HK Tech 300 program website. This tool automatically collects company names, websites, and contact emails from multiple pages.

## 📋 Features

- ✅ Extracts startup names, emails, and company websites
- ✅ Handles both Angel Fund and Seed Fund startup types
- ✅ Automatic pagination support
- ✅ Headless browser mode for faster scraping (90% speed improvement)
- ✅ Outputs data to both CSV and Excel formats
- ✅ Smart email domain extraction for missing websites
- ✅ Robust error handling
- ✅ Progress tracking with real-time console updates

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser installed

### Setup Steps

1. **Clone or download this project**
   ```bash
   cd C:\Users\YourName\Desktop\bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python --version
   pip list
   ```

## 🚀 Usage

### Basic Usage

Run the scraper from your terminal:

```bash
python run.py
```

You'll be prompted to enter the number of pages to scrape:
```
Enter the number of pages: 5
```

### Output Files

The scraper generates two files in the project directory:
- `startups.csv` - Raw CSV data
- `output.xlsx` - Excel formatted output with proper columns

### Output Format

| Company Name | CityU URL | Company Website | Email                        |
|-------------|-----------|-----------------|-------------------------------|
| Company A   | https://... | https://company-a.com | contact@company-a.com |
| Company B   | https://... | No Info Found | info@company-b.com            |


## ⚙️ Configuration

Edit `startups/constants.py` to customize settings:

```python
# Browser settings
HEADLESS_MODE = True  # Set to False to see browser window
IMPLICIT_WAIT_TIME = 15  # Page load timeout in seconds

# Output file names
CSV_OUTPUT = "startups.csv"
EXCEL_OUTPUT = "output.xlsx"

# Target website
WEBSITE_URL = "https://www.cityu.edu// filepath: c:\Users\Abhishek\Desktop\bot\README.md
