from bs4 import BeautifulSoup
import requests
import datetime
import pytz
from urllib.parse import urlparse
from typing import List
from bs4 import SoupStrainer
import lxml


def get_hostname(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]  # Remove 'www.' from the beginning if present
    # Split the domain into its parts
    domains = []
    domain_parts = domain.split('.')
    # Adding domains to list and detect if the link is form subdomain
    if len(domain_parts) > 2:
        parent_domain = '.'.join(domain_parts[-2:])
        domains.append(parent_domain)
        domains.append(domain)
    else:
        domains.append(domain)
    if len(domains) == 1:
        domains.append(None)
    # Returning the def
    return domains


def convert_timestamp(timestamp):
    # Define the timezone as Asia/Jakarta (GMT+7)
    timezone = pytz.timezone('Asia/Jakarta')
    # Convert the datetime to the desired timezone
    datetime_object = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc).astimezone(timezone)
    # Format the datetime as a string in the expected format if needed
    # formatted_time = datetime_object.strftime("%d %B %Y %H:%M")
    # Returning the def
    return datetime_object


class DetikScrapper:
    def __init__(self, url: List[str], article_target, **kwargs):
        self.url = url
        self.article_target = article_target
        self.print_console = kwargs.get("print", False)

    def detik_crawler(self):
        crawled_response = []
        for url in self.url:
            articles_crawled = 0  # Counter for the number of articles crawled from the current URL
            while articles_crawled < self.article_target:
                # Fetch the URL data using requests.get(url)
                request_result = requests.get(url).text
                # Strainer
                only_article_tag = SoupStrainer('article')
                # Creating soup from the fetched request
                soup = BeautifulSoup(request_result, 'html.parser', parse_only=only_article_tag)
                # Selecting article tag in soup object
                articles = soup.find_all('article')

                # Iterate article in articles and select corresponding tags and attributes
                for article in articles:
                    title = article.find('h3').getText().strip()
                    link = article.find('a')['href']
                    domain = get_hostname(link)[0]
                    subdomain = get_hostname(link)[1]
                    timestamp = int(article.find('span', attrs={'d-time': True}).get('d-time'))
                    time_published = convert_timestamp(timestamp)  # DD-MM-YY HH:MM Format

                    # Structuring selection in dictionary
                    data = {
                        'title': title,
                        'link': link,
                        'domain': domain,
                        'subdomain': subdomain,
                        'time_published': time_published  # DD-MM-YY HH:MM Format
                    }

                    # Testing response in console
                    if self.print_console:
                        print(f'Title: {title}')
                        print(f'Link: {link}')
                        print(f'Domain: {domain}')
                        print(f'Subdomain: {subdomain}')
                        print(f'Time Publish: {time_published}')
                        print('----------')

                    crawled_response.append(data) # Appending to crawled_response list
                    articles_crawled += 1  # Increment the count of crawled articles

                    # Check if the desired number of articles has been reached
                    if articles_crawled >= self.article_target:
                        break

                # Mechanism to find next pagination
                next_page = soup.find('a', text="Next")
                if next_page:
                    next_page_url = next_page.get('href')
                    if next_page_url.startswith('/'):
                        # Append next page URL to the base URL if it's a relative URL
                        next_page_url = url + next_page_url
                    url = next_page_url
                else:
                    break

        # Returning the def
        return crawled_response


class KompasScrapper:
    def __init__(self, url: List[str], article_target, **kwargs):
        self.url = url
        self.article_target = article_target
        self.print_console = kwargs.get("print", False)

    def kompas_crawler(self):
        crawled_response = []
        for url in self.url:
            articles_crawled = 0  # Counter for the number of articles crawled from the current URL
            while articles_crawled < self.article_target:
                # Fetch the URL data using requests.get(url),
                request_result = requests.get(url).text
                # Creating soup from the fetched request
                soup = BeautifulSoup(request_result, 'html.parser')
                # Selecting article tag in soup object
                articles = soup.find_all(class_='article__list')

                # Iterate article in articles and selecting correspondent tag and other attributes
                for article in articles:
                    title = article.find('h3').getText().strip()
                    link = article.find('a')['href']
                    domain = get_hostname(link)[0]
                    subdomain = get_hostname(link)[1]
                    timestamp = article.find(class_="article__date").getText()
                    # Convert the input string to a datetime object
                    time_published = datetime.datetime.strptime(timestamp, "%d/%m/%Y, %H:%M WIB")
                    # Convert the datetime object to the desired format if needed
                    # formatted_time = datetime_object.strftime("%d %B %Y %H:%M")

                    # Structuring selection in dictionary
                    data = {
                        'title': title,
                        'link': link,
                        'domain': domain,
                        'subdomain': subdomain,
                        'time_published': time_published  # DD-MM-YY HH:MM Format
                    }

                    # Testing response in console
                    if self.print_console:
                        print(f'Title: {title}')
                        print(f'Link: {link}')
                        print(f'Domain: {domain}')
                        print(f'Subdomain: {subdomain}')
                        print(f'Time Publish: {time_published}')
                        print('----------')

                    crawled_response.append(data)  # Appending to crawled_response list
                    articles_crawled += 1  # Increment the count of crawled articles

                    # Check if the desired number of articles has been reached
                    if articles_crawled >= self.article_target:
                        break

                # Mechanism to find next pagination
                next_page = soup.find('a', text="Next")
                if next_page:
                    next_page_url = next_page.get('href')
                    if next_page_url.startswith('/'):
                        # Append next page URL to the base URL if it's a relative URL
                        next_page_url = url + next_page_url
                    url = next_page_url
                else:
                    break

        # Returning the def
        return crawled_response
