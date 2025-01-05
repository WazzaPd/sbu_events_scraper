# Event Scraper for SB Engaged

## Overview

This Python script uses Selenium to scrape event details—titles, dates, and locations—from the SB Engaged website and saves the data to a CSV file.

## Requirements

Install dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup

1. **ChromeDriver (Chrome itself is also required)**: Download and install the correct version from [here](https://chromedriver.chromium.org/downloads).
2. **Update Script**: Replace ChromeDriver path to location of your ChromeDriver:

```python
service = Service(executable_path="/usr/local/bin/chromedriver")
```

3. **Run Script**:

```bash
python scraper.py
```

## Output

Data is saved in `events_data.csv`.

## Troubleshooting

- **ChromeDriver Version Error**: Ensure ChromeDriver matches your browser version.
- **Missing Elements**: Update XPath selectors in the script if the website structure changes.
