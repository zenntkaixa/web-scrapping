from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.select import Select
import time

# Specify website
website = 'https://www.adamchoi.co.uk/overs/detailed'

# Create driver with ChromeDriver (no need to specify path if it's in PATH)
driver = webdriver.Chrome()

# Open the website
driver.get(website)

# Find and click the "All matches" button
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# Locate the dropdown menu for selecting the country by its ID
select_country = Select(driver.find_element(By.ID, 'country'))
select_country.select_by_visible_text('Spain')

# Wait for 3 seconds to allow the page to load the data for Spain
time.sleep(3)

# Find all <tr> elements that have either 'ng-scope isNotHighlightedRow' or 'ng-scope isHighlightedRow' in their class attribute
matches = driver.find_elements(By.XPATH, '//tr[contains(@class, "ng-scope isNotHighlightedRow") or contains(@class, "ng-scope isHighlightedRow")]')

# Initialize empty lists to store match data
date = []
home_team = []
score = []
away_team = []

# Loop through each match row (<tr> element)
for match in matches:
    # Extract the data from the <td> elements in the row and append it to the lists
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home_team.append(match.find_element(By.XPATH, './td[3]').text)
    score.append(match.find_element(By.XPATH, './td[4]').text)
    away_team.append(match.find_element(By.XPATH, './td[5]').text)

# Close the website
driver.quit()

# Create a pandas DataFrame from the extracted data
# Save the DataFrame to a CSV file named 'football_data.csv' without the index column
pd.DataFrame({
    'date': date,
    'home_team': home_team,
    'score': score,
    'away_team': away_team
}).to_csv('football_data.csv', index=False)

# Pause the script to keep the browser open (useful for debugging)
input("Press Enter to close the browser...")
