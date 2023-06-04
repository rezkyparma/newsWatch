from bs4 import BeautifulSoup
import requests
import _get_domain
import _time_convertor

# List of publisher index page
DETIK_NEWS = "https://news.detik.com/indeks"
DETIK_SPORT = "https://sport.detik.com/indeks"
detik_index_page = [DETIK_NEWS, DETIK_SPORT]


def detik_crawler(list_index):
    crawled_response = []
    for index in list_index:
        # Fetch the URL data using requests.get(url),
        request_result = requests.get(index).text
        # Creating soup from the fetched request
        soup = BeautifulSoup(request_result, 'html.parser')
        # Selecting article tag in soup object
        articles = soup.find_all('article')
        # Iterate article in articles
        for article in articles:
            # Selecting correspondent tag and other attributes
            title = article.find('h3').getText().strip()
            link = article.find('a')['href']
            domain = get_domain.get_hostname(link)[0]
            subdomain = get_domain.get_hostname(link)[1]
            timestamp = int(article.find('span', attrs={'d-time': True}).get('d-time'))
            time_published = time_convertor.convert_timestamp(timestamp)  # DD-MM-YY HH:MM Format
            # Structuring selection in dictionary
            data = {
                'title': title,
                'link': link,
                'domain': domain,
                'subdomain': subdomain,
                'time_published': time_published  # DD-MM-YY HH:MM Format
            }
            # Appending to crawled_response list
            crawled_response.append(data)
            # Testing response in console
            # print(f'Title: {title}')
            # print(f'Link: {link}')
            # print(f'Domain: {domain}')
            # print(f'Subdomain: {subdomain}')
            # print(f'Time Publish: {time_published}')
            # print('----------')
    # Returning the def
    return crawled_response

def kumparan_crawler(list_index):
    crawled_response = []
    for index in list_index:
        # Fetch the URL data using requests.get(url),
        request_result = requests.get(index).text
        # Creating soup from the fetched request
        soup = BeautifulSoup(request_result, 'html.parser')
        # Selecting article tag in soup object
        articles = soup.find_all('article')
        # Iterate article in articles
        for article in articles:
            # Selecting correspondent tag and other attributes
            title = article.find('h3').getText().strip()
            link = article.find('a')['href']
            domain = get_domain.get_hostname(link)[0]
            subdomain = get_domain.get_hostname(link)[1]
            timestamp = int(article.find('span', attrs={'d-time': True}).get('d-time'))
            time_published = time_convertor.convert_timestamp(timestamp)  # DD-MM-YY HH:MM Format
            # Structuring selection in dictionary
            data = {
                'title': title,
                'link': link,
                'domain': domain,
                'subdomain': subdomain,
                'time_published': time_published  # DD-MM-YY HH:MM Format
            }
            # Appending to crawled_response list
            crawled_response.append(data)
            # Testing response in console
            # print(f'Title: {title}')
            # print(f'Link: {link}')
            # print(f'Domain: {domain}')
            # print(f'Subdomain: {subdomain}')
            # print(f'Time Publish: {time_published}')
            # print('----------')
    # Returning the def
    return crawled_response


print(len(detik_crawler(detik_index_page)))
