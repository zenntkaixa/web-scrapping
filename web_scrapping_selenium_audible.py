from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Uncomment the following lines to run Chrome in headless mode (without opening a browser window)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless=new')  # Run in headless mode
# options.add_argument('window-size=1920x1080')  # Set window size for headless mode
# driver = webdriver.Chrome(options=options)  # Initialize Chrome with options

# Specify the website URL to scrape
website = 'https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&pf_rd_p=bb0efe44-14ef-41cc-91b0-c1b40e66ffe2&pf_rd_r=HRV7JWQJEF2HCETZ7YAV&plink=X53mmKHYuHHNlQOg&pageLoadId=yHq3T8cnkzt77LMQ&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482&ref=a_search_t1_navTop_pl0cg1c0r0'

# Create driver with ChromeDriver (no need to specify path if it's in PATH)
driver = webdriver.Chrome()

# Open the website
driver.get(website)
driver.maximize_window() # Maximize the browser window for better visibility

# Find the pagination element to determine the total number of pages
pagination = driver.find_element(By.XPATH, './/ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li') # Get all pagination elements
last_page = int(pages[-2].text) # Extract the last page number (second-to-last element)

current_page = 1 # Initialize the current page counter

# Initialize empty lists to store book details
book_title =[]
book_author = []
book_length = []

# Loop through all pages
while current_page <= last_page:
    # Wait for the container holding the book products to load
    container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "adbl-impression-container"))
    )
    # Wait for all book product elements to load
    products = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//li[contains(@class, 'productListItem')]"))
    )

    # Loop through each product and extract details
    for product in products:
        book_title.append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_length.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    current_page += 1 # Move to the next page
    try:
        # Find and click the "Next" button to navigate to the next page
        next_page_button = driver.find_element(By.XPATH, './/span[contains(@class, "nextButton")]')
        next_page_button.click()
    except:
        # If the "Next" button is not found, exit the loop
        pass

# Close the website
driver.quit()

# Create a pandas DataFrame from the extracted book details
# Save the DataFrame to a CSV file named 'books.csv' without the index column
pd.DataFrame({
    'title': book_title,
    'author': book_author,
    'length': book_length
}).to_csv('books.csv', index=False)

# Pause the script to keep the browser open (useful for debugging)
input("Press Enter to close the browser...")

