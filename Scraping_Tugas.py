from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import json

def scraper(url):
    print('>Scraping... ', url)
    try:
        # Configure WebDriver to use headless Firefox
        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        # Get the URL given
        driver.get(url)

        # Wait for the element to be present
        print('>Checking... "Game List" availability...')
        try:
            wait = WebDriverWait(driver, timeout=10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c-productListings')))
            print('>Element present')
        except:
            raise LookupError("There is no element specified")

        # Parse the page source with BeautifulSoup
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        # Prepare the variable for JSON data
        games = []

        # Find the game containers
        for game in soup.find_all('div', class_='c-finderProductCard c-finderProductCard-game'):
            # Safely extract data from each element
            game_name = game.find('h3', class_='c-finderProductCard_titleHeading').text if game.find('h3', class_='c-finderProductCard_titleHeading') else 'N/A'
            release_date = game.find_all('span', {'class': 'u-text-uppercase'})[0].text if game.find_all('span', {'class': 'u-text-uppercase'}) else 'N/A'
            age_rating = game.find_all('div', class_='c-finderProductCard_meta')[0].find_all('span')[2].contents[1].strip() if game.find_all('div', class_='c-finderProductCard_meta')[0].find_all('span')[2].contents[1].strip() else 'N/A'
            Summary = game.find_all('div', class_='c-finderProductCard_description')[0].find_all('span')[0].contents[0] if game.find_all('div', class_='c-finderProductCard_description')[0].find_all('span')[0].contents[0] else 'N/A'
            Metascore = game.find_all('div', class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall')[0].find_all('span')[0].contents[0] if game.find_all('div', class_='c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall')[0].find_all('span')[0].contents[0] else 'N/A'

            # Append the scraped data into games variable for JSON data
            games.append(
                {
                    'Game Name': game_name,
                    'Release Date': release_date.strip(),
                    'age_rating': 'Rated' + ' ' + age_rating,
                    'Game Summary': Summary,
                    'Metascore': Metascore,
                }
            )

        print('Scraping Successful')
        # Close the WebDriver
        driver.quit()
        return games

    except Exception as e:
        print('error', e)


if __name__ == '__main__':
    print('Starting scraper...')
    url = 'https://www.metacritic.com/browse/game/'

    data = scraper(url)

    # Save data to JSON file
    with open('games.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)