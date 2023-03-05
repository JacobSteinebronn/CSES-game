import requests
from bs4 import BeautifulSoup
import json

r = requests.get('https://cses.fi/problemset/list')
soup = BeautifulSoup(r.text, 'html.parser')

problemset = []

content = soup.find("div", class_="content")
for tag in content.find_all('h2'):
	if(tag.text == 'General'): continue
	print(tag.name, tag.text)
	items = tag.findNext('ul')
	for prob in items.find_all('li'):
		a = prob.findNext('a')
		details = prob.findNext('span').text.split(' / ')
		print('\t', a['href'], a.text, details)
		problemset.append({'category': tag.text, 'name': a.text, 'link': 'https://cses.fi'+a['href'], 'solves': int(details[0]), 'submits': int(details[1])})

print(problemset)

with open('problemset.json', 'w') as file:
	file.write(json.dumps(problemset, indent=3))