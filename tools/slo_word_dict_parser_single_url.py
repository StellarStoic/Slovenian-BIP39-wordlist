# Single dict URL handling for fran. Useful if need to check words in all dictionaries
# For choosing only a selected few dictionaries, use slo_word_dict_parser_multi_url.

import json
import random
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# List of User-Agent strings to rotate through
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366",
    "Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:41.0) Gecko/20100101 Firefox/41.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 10.0; ARM; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/534.34 (KHTML, like Gecko) Safari/534.34",
    "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0.4389.82",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; ARM64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Linux; Android 10; SM-N975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.14977",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.0.818.66",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edge/90.1.961.38",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 13904.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.167 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS arm64 13904.77.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.167 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; CrOS x86_64 13597.94.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.3 Safari/537.86.7",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/534.34 (KHTML, like Gecko) Safari/534.34",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
]

# File paths
WORD_LIST_FILE = 'slovenian.txt'
JSON_OUTPUT_FILE = 'tools/SLO_BIP39_word_definitions_from_all_dictionaries.json'

# URL of the dictionaries website
url = 'https://www.fran.si/iskanje?View=1&Query=*&All=*' # All dictionaries in FRAN.si

# Flag to control whether to resume from the last point or start over
resume_from_last_point = True

# Function to initialize the WebDriver in headless mode with a random user-agent
def init_driver():
    chrome_options = Options()
    
    # Enable headless mode
    chrome_options.add_argument('--headless')
    
    # Set window size for headless mode
    chrome_options.add_argument('--window-size=1920x1080')
    
    # Randomly select a user-agent
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.implicitly_wait(10)  # Implicit wait
    return driver

# Function to simulate human-like delays
def human_like_delay(min_delay=5, max_delay=15):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to clean and format HTML content, excluding unnecessary parts
def clean_html_content(html_content):
    # Use BeautifulSoup to clean and format HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements, such as citations
    for citation in soup.find_all('p', class_='entry-citation'):
        citation.decompose()
    
    text = soup.get_text(separator=' ', strip=True)
    return text

# Read the word list from a file
word_list = []
with open(WORD_LIST_FILE, 'r') as file:
    word_list = file.readlines()

word_list = [word.strip() for word in word_list]

# Check if there is an existing JSON file to resume from
word_definitions = {}
if os.path.exists(JSON_OUTPUT_FILE) and resume_from_last_point:
    try:
        with open(JSON_OUTPUT_FILE, 'r', encoding='utf-8') as json_file:
            word_definitions = json.load(json_file)
    except json.JSONDecodeError:
        print("JSON file is empty or invalid. Starting from scratch.")
        word_definitions = {}
else:
    print("No existing JSON file found or resume flag is set to False. Starting from scratch.")
    word_definitions = {}

# Determine the starting point for the script
start_index = len(word_definitions)

print(f"Starting from word index: {start_index}")

# Iterate over each word in the word list starting from the last processed index
for index, word in enumerate(word_list[start_index:], start=start_index):
    # Initialize the driver for each word to use a different user-agent
    driver = init_driver()
    driver.get(url)
    
    # Handle the cookie consent prompt
    try:
        # Click the radio button to accept cookies
        cookie_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/form/div[1]/label/input'))
        )
        cookie_radio_button.click()
        
        # Click the "Shrani" button to save the preference
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/form/div[2]/button'))
        )
        save_button.click()
        
        print("Cookie consent accepted.")
    except TimeoutException:
        print("No cookie prompt found or timed out waiting for it.")

    try:
        # Wait until the input field is present
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/form/div/span[1]/input[2]'))
        )
        
        # Clear any existing text in the input field using multiple methods
        search_input.clear()
        time.sleep(0.5)
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)
        
        # Enter the word into the search field
        search_input.send_keys(word)

        # Human-like delay
        human_like_delay()

        # Locate and click the search button
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/form/div/span[2]/button[2]/i'))
        )
        search_button.click()

        # Wait for the search results to load
        human_like_delay(min_delay=2, max_delay=5)

        # Find all entry elements using the correct class for the whole entry
        dictionary_results = []
        unique_dictionaries = set()  # To store unique dictionaries
        entry_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "list-group-item entry")]')

        if not entry_elements:
            print(f"No results found for word '{word}'.")
        else:
            for entry in entry_elements:
                try:
                    # Extract dictionary info and entire entry content as HTML
                    dictionary_info = entry.find_element(By.XPATH, './/span[contains(@class, "dictionary-name")]').text
                    word_example = entry.find_element(By.XPATH, './/span[contains(@class, "font_xlarge")]/a').text
                    complete_content = entry.find_element(By.XPATH, './/div[contains(@class, "entry-content")]').get_attribute('innerHTML')
                    
                    # Clean the content to make it more readable and exclude unnecessary parts
                    readable_content = clean_html_content(complete_content)
                    
                    # Add dictionary info to the set of unique dictionaries
                    unique_dictionaries.add(dictionary_info)
                    
                    dictionary_results.append({
                        'dictionary': dictionary_info,
                        'word': word_example,
                        'meaning': readable_content
                    })
                    
                    print(f"Extracted meaning for word '{word}': {readable_content[:50]}...")

                except NoSuchElementException as e:
                    print(f"An element was not found for word '{word}': {e}")
                    continue

        # If no results found, set the word entry to None
        if not dictionary_results:
            word_definitions[word] = {
                'index': index,
                'number_of_results': 0,
                'number_of_dictionaries': 0,
                'results': [{'dictionary': None, 'word': None, 'meaning': None}]
            }
        else:
            # Store the word and its dictionary results in the JSON object
            word_definitions[word] = {
                'index': index,
                'number_of_results': len(dictionary_results),
                'number_of_dictionaries': len(unique_dictionaries),  # Use length of unique_dictionaries set
                'results': dictionary_results
            }

        # Print progress
        print(f"Extracted {len(dictionary_results)} results for word: {word}")

    except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
        print(f"An error occurred for word '{word}': {e}")
        # Take a screenshot for debugging
        driver.save_screenshot(f'screenshot_{word}.png')
        
        # Store the word with None values for dictionary and meaning
        word_definitions[word] = {
            'index': index,
            'number_of_results': 0,
            'number_of_dictionaries': 0,
            'results': [{'dictionary': None, 'word': None, 'meaning': None}]
        }

    # Write to the JSON file after processing each word
    with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(word_definitions, json_file, ensure_ascii=False, indent=4)

    # Close the web driver after each word search to start fresh with a new user-agent next time
    driver.quit()

    # Random delay between requests to avoid detection
    human_like_delay(min_delay=3, max_delay=10)

print("Scraping completed and saved to json file.")