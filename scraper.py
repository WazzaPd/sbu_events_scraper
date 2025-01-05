from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import traceback

# --- SETUP CHROME WEBDRIVER ---
# This section configures the ChromeDriver for web scraping.
# Note: Replace the 'executable_path' with the actual path to your ChromeDriver.
service = Service(executable_path="/usr/local/bin/chromedriver")
options = webdriver.ChromeOptions()

# Comment '--headless' to run while opening the browser.
options.add_argument("--headless")

# Recommended options to avoid sandbox and rendering issues.
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Prevent detection as an automated tool.
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

# Create the Chrome driver instance.
driver = webdriver.Chrome(service=service, options=options)

try:
    # --- NAVIGATE TO PAGE ---
    driver.get("https://stonybrook.campuslabs.com/engage/events")

    # Define timeout settings (30 seconds max for elements to load).
    wait = WebDriverWait(driver, 30)

    # --- LOAD MORE EVENTS ---
    # Many pages load content dynamically as you scroll. This loop simulates scrolling.
    # To Do! : Implement Clicking the load more button on the page
    for _ in range(5):  # Increase or decrease the range to control how many scrolls.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to let content load after each scroll.

    # --- SCRAPE EVENT DATA ---
    # Wait until event cards are loaded.
    events = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'MuiCard-root')]")))

    # Collect event details in a list.
    events_data = []
    for event in events:
        try:
            # Extract the event title.
            title = event.find_element(By.XPATH, ".//h3").text

            # Extract date and time.
            date_time = event.find_element(By.XPATH, ".//div[contains(text(), 'at')]").text

            # Extract location (fallback to 'Not Specified' if missing).
            location = event.find_elements(By.XPATH, ".//div[not(contains(text(), 'at ')) and string-length(text()) > 2]")
            location = location[-1].text if location else "Not Specified"

            # Add the event details to our data.
            events_data.append({
                "Title": title,
                "Date/Time": date_time,
                "Location": location
            })
        except Exception as e:
            # Log errors if specific events cannot be parsed.
            print(f"Error parsing event: {e}")
            continue

    # --- SAVE DATA TO FILE ---
    # Convert the data to a CSV file using pandas for easy analysis.
    df = pd.DataFrame(events_data)
    df.to_csv("events_data.csv", index=False)
    print("Scraping completed. Data saved to 'events_data.csv'.")

except Exception as e:
    # Handle any exceptions during execution and print error details.
    print("An error occurred:")
    traceback.print_exc()

finally:
    # Ensure the browser is closed properly.
    driver.quit()
