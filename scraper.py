import requests
import sys
from bs4 import BeautifulSoup
import pprint

def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
	hn = []
	for idx, item in enumerate(links):
		title = item.getText()
		href = item.get('href', None)
		vote = subtext[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			if points >= 100:
				hn.append({'title': title, 'link': href, 'votes': points})
	return hn

def get_pages(num_pages):
	results = []
	for i in range(1, num_pages+1):
		res = requests.get('https://news.ycombinator.com/news?p=' + str(i))
		soup = BeautifulSoup(res.text, 'html.parser')
		links = soup.select('.storylink')
		subtext = soup.select('.subtext')
		results += create_custom_hn(links, subtext)
	return sort_stories_by_votes(results)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Please provide the number of pages you wish to scrape.")
	else:
		pprint.pprint(get_pages(int(sys.argv[1])))
