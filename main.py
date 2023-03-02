from argparse import ArgumentParser
import os
import requests
import time
import urllib.parse

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from tqdm import tqdm
import re

# Load environment variables
load_dotenv()

# set up the connection string to the MongoDB Cloud database
# replace <username>, <password>, <dbname>, and <clustername> with your own values
username = urllib.parse.quote_plus(os.getenv('MONGODB_USERNAME'))
password = urllib.parse.quote_plus(os.getenv('MONGODB_PASSWORD'))
dbname = urllib.parse.quote_plus(os.getenv('MONGODB_DBNAME'))
clustername = urllib.parse.quote_plus(os.getenv('MONGODB_CLUSTERNAME'))
conn_str = f'mongodb+srv://{username}:{password}@{clustername}.mongodb.net/{dbname}?retryWrites=true&w=majority'

# create a client object using the connection string
client = MongoClient(conn_str)

# get a reference to the database and forum_collection
db = client[dbname]
forum_collection = db['all_forum']

# Add a unique index to the 'tid' field
forum_collection.create_index('tid', unique=True)


def scrape_forum_by_page(page_no):
	target_url = f'https://ladies.discuss.com.hk/forumdisplay.php?fid=1259&from=2&page={page_no}'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	try:
		response = session.get(target_url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.HTTPError as err:
		print(f'HTTP error occured: {err}')
		return
	except Exception as err:
		print(f'Other error occured: {err}')
		return
	forum = BeautifulSoup(response.content, 'html.parser')
	# Use a CSS selector to find the tbody elements
	thread_list = forum.find_all(id=re.compile("^normalthread"))
	all_forum = [{
		    'tid': tbody.get('id').split('_')[1],
		    'category': tbody.select_one('th em a').text.strip() if tbody.select_one('th em a') else None,
		    'title': tbody.select('th span > a')[0].text.strip(),
		    'date': tbody.select('th span > a')[0]['title'].split(' ')[1] if 'title' in tbody.select('th span > a')[0].attrs else None,
		    'author': tbody.select_one('td cite a').text.strip(),
		    'views': tbody.select_one('td em span').text.strip(),
		    'url_path': tbody.select('th span > a')[0]['href']
		} for tbody in thread_list]

def migrate_all_forum():
	# Create a session object
	session = requests.Session()
	print('Extracting discussion pages')
	for i in tqdm(range(1, 21), total=20):
		scrape_forum_by_page(i)
		time.sleep(0.5)  # Add a 500ms delay between requests
	print('Inserting scraped records to MongoDB')
	for row in tqdm(all_forum, total=len(all_forum)):
		try:
		    forum_collection.insert_one(row)
		except DuplicateKeyError:
		    print('tid already exists in the forum_collection.')

def scrape_discussions_by_forum():
	# find all the documents in the forum_collection
	cursor = forum_collection.find()
	# iterate over the documents
	print('Extracting posts of forum')
	for forum in tqdm(cursor, total=len(list(cursor))):
		target_url = f"https://ladies.discuss.com.hk/{forum['url_path']}"
		with requests.Session() as session:
			response = session.get(target_url)
			# Send a GET request to the website and parse the HTML content
		soup = BeautifulSoup(response.content, 'html.parser')
		post_list = soup.find_all(id=re.compile('^table-pid'))
		all_posts = []
		for post in post_list:
			post_no = post.find_all(id=re.compile('^postnum_'))[0].text.strip()
			datetime = post.find_all(text=re.compile(r'發表於'))[0].split('發表於')[1].strip()
			post_messages = post.find_all(id=re.compile('^postorig_'))
			message_parts = []
			for message in post_messages:
				message_parts.append(message.text)
			whole_message = ''.join(message_parts)
			post_data = {
			    'post_no': post_no,
			    'date': datetime,
			    'message': whole_message
			}
			all_posts.append(post_data)
		forum_collection.update_many({'_id': forum['_id']}, {'$set': {'all_posts': all_posts}})
		time.sleep(0.1)  # Add a 100ms delay between requests


if __name__ =='__main__':
	all_forum = []
	# Create the parser
	parser = ArgumentParser(description='Extract forum or forum')
	# Add an argument
	parser.add_argument('--action', choices=['scrape_forum', 'scrape_discussions', 'export_forum'], help='Specify whether to scrape forum or discussions', required=True)
	# Parse the argument
	args = parser.parse_args()
	# ===== Step 1 =====
	if (args.action == 'scrape_forum'):
		migrate_all_forum()
	# ===== Step 2 =====
	elif(args.action == 'scrape_discussions'):
		scrape_discussions_by_forum()









