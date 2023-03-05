import json
import sys
import random
import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description='Pick a random CSES problem for a group of people to race on!')
parser.add_argument('-m', '--min_solves', help='The minimum number of passing submissions on the problem (higher = easier)')
parser.add_argument('-x', '--max_solves', help='The maximum number of passing submissions on the problem')
parser.add_argument('-a', '--allow-categories', help='Substrings for categories to include', nargs='+', default=[])
parser.add_argument('-b', '--block-categories', help='Substrings for categories to exclude', nargs='+', default=[])
parser.add_argument('-u', '--users', help='List of user IDs to avoid selecting solved problems', nargs='+', default=[])

with open('problemset.json', 'r') as file:
	problemset = json.load(file)

args = parser.parse_args()

solved = []

for uid in args.users:
	r = requests.get(f'https://cses.fi/problemset/user/{uid}/')
	soup = BeautifulSoup(r.text, 'html.parser')
	for solve in soup.find_all('a', class_="task-score icon full"):
		name = solve['title']
		if name not in solved:
			solved.append(name)

# print(solved)

def usable(problem):
	if problem['name'] in solved: return False
	if args.min_solves is not None and problem['solves'] < int(args.min_solves): return False
	if args.max_solves is not None and problem['solves'] > int(args.max_solves): return False

	if len(args.block_categories) > 0:
		for sub in args.block_categories:
			if sub.lower() in problem['category'].lower(): return False

	if len(args.allow_categories) > 0:
		for sub in args.allow_categories:
			if sub.lower() in problem['category'].lower(): return True
	else: return True	
	
	return False

valid = list(filter(usable, problemset))
# print(list(filter(usable, problemset)))
# print(random.choice(list(filter(usable, problemset))))
if len(valid) > 0:
	print(random.choice(valid))
else:
	print("No valid problems in the filters :(")