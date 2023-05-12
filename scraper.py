# Scrape data from pages for demo

# Import required packages
import urllib3
from bs4 import BeautifulSoup

base_page_url = "http://localhost:8888"

# Create a urllib3 PoolManager instance in order to make HTTP requests. 
# This object handles all of the details of connection pooling and thread safety so that we don't have to.
http = urllib3.PoolManager()

# Read the 'base' page web page
response = http.request('GET', base_page_url)

# Turn the returned HTML into an in-memory data structure that we can query/crawl.
soup = BeautifulSoup(response.data, 'html.parser')

# Take a look at the data structre, pretty-printed
print(soup.prettify())

pages_soup = soup.find_all('a')
len(pages_soup)


# Helper function
def crawl_page(a_tag):
	station_name = a_tag.contents[0]
	page_url = base_page_url + '/' + a_tag['href']
	resp =	http.request('GET', page_url)
	soup = BeautifulSoup(resp.data, 'html.parser')
	service_details_div = soup.find('div', class_='service_details')
	div_with_history = service_details_div.find_next_sibling('div')
	list_of_lis = div_with_history.find_all('li')
	last_history_item = list_of_lis[len(list_of_lis)-1].string
	print(station_name + ' : ' + last_history_item)
#

# Main processing loop
for page in pages_soup:
	# print('Processing ' + page.contents[0])
	crawl_page(page)
# 
