# StartUps Extractor

A web scraping tool to extract startup information from CityU HKTech300 website.

## Features
- Extracts startup names, emails, and company websites
- Handles pagination automatically
- Outputs data to Excel format
- Headless browser support

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the extractor:
```bash
python run.py
```

Configure settings in `startups/constants.py`:
- `HEADLESS_MODE`: Set to `False` to see browser window
- `IMPLICIT_WAIT_TIME`: Adjust wait time for page loads
- `CSV_OUTPUT` / `EXCEL_OUTPUT`: Change output file names

## Project Structure
```
bot/
├── startups/          # Main package
│   ├── __init__.py
│   ├── constants.py   # Configuration
│   └── startups.py    # Scraper logic
├── run.py             # Entry point
└── requirements.txt   # Dependencies
```

## Output
- `startups.csv` - Raw CSV data
- `output.xlsx` - Excel formatted output