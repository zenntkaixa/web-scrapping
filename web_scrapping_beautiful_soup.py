from bs4 import BeautifulSoup
import requests
import os
import re

# Create the transcript folder if it doesn't exist
os.makedirs('transcript', exist_ok=True)
# root URL
root = 'https://subslikescript.com'
# set movies URL
website = f'{root}/movies_letter-A' # link to movie links starting with "A"
# call URL by HTTP request
response = requests.get(website)
# get HTML content from website request
content = response.text

# format HTML content with BeautifulSoup
soup = BeautifulSoup(content, 'lxml')

pagination = soup.find('ul', class_="pagination")
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

#  init links list
links = []

for page in range(1, int(last_page)+1)[:2]: # range(1, 92) # optional for short case: range(1, 3)
    # {page} = page number 1 to n
    response = requests.get(f'{website}?page={page}')
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    # get article
    box = soup.find('article', class_="main-article")
    # find all <a> tags and do a loop
    for link in box.find_all('a', href=True):
        # append href links in the links list
        links.append(link['href'])

    for link in links:
        try:
            # call URL by HTTP request
            response = requests.get(f'{root}{link}')
            # get HTML content from website request
            content = response.text
            # format HTML content with BeautifulSoup
            soup = BeautifulSoup(content, 'lxml')
            # get article
            box = soup.find('article', class_="main-article")
            # get title
            title = box.find('h1').get_text()
            title = re.sub(r'[<>:"/\\|?*]', '_', title)  # Replace invalid characters with underscores due to OS not allowed special characters in filename
            #  get transcript
            transcript = box.find('div', class_="full-script").get_text(strip=True, separator='\n')
            # create a new file with Title as filename, and write transcript in it
            with open(f'transcript/{title}.txt', 'w', encoding='utf-8') as file:
                file.write(transcript)
        except Exception as e:
            # skip scrapping if BS has fetching error, e.g. null title, null transcript
            print(f'[ERROR] Link {link} is not working! Error: {e}')
            pass