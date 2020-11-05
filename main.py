import praw
from praw.models import MoreComments
import configparser
from requests import Session
import logging
import requests
from datetime import datetime, timedelta
from xml.etree import ElementTree
import csv


num_submissions = None
api_key = None
option = None


def is_book(word):
	# Assuming people write words that are unique enough to identify the book
	params = [('key', api_key), ('q', word)]
	response = requests.get("https://www.goodreads.com/search/index.xml", params=params)
	if response.status_code == 404:
		return None

	tree = ElementTree.fromstring(response.content)
	books = tree.findall("search/results/work/best_book")
	if books is None or len(books) == 0:
		return None

	return books[0].find("title").text


def perform_query(reddit):
	books_count = {}
	subreddit = reddit.subreddit('suggestmeabook')
	submissions = subreddit.hot(limit=num_submissions) if option == 'hot' else subreddit.top(limit=num_submissions)
	for submission in submissions:
		comments = submission.comments
		for comment in comments:
			if isinstance(comment, MoreComments):
				continue
			# Look for XYZ by ABC in this comment
			for sentence in comment.body.split('.'):
				parts = [part.strip() for part in sentence.split('by')]
				book_name = is_book(parts[0])
				if book_name:
					if book_name in books_count:
						books_count[book_name] += 1
					else:
						books_count[book_name] = 1

	# sort the dictionary by count
	books_count = {k: v for k, v in sorted(books_count.items(), key=lambda item: item[1], reverse=True)}

	with open(f'book_mentions_{option}_{num_submissions}_submissions.csv', 'w') as handle:
		fieldnames = ['book_name', 'mentions']
		mentions_writer = csv.DictWriter(handle, fieldnames=fieldnames)
		mentions_writer.writeheader()
		for key in books_count:
			mentions_writer.writerow({'book_name': key, 'mentions': books_count[key]})
	


if __name__ == '__main__':
	config = configparser.ConfigParser()
	config.read('config.ini')
	client_id = config.get('REDDIT','client_id')
	client_secret = config.get('REDDIT', 'client_secret')
	password = config.get('REDDIT', 'password')
	user_agent = config.get('REDDIT', 'user_agent')
	username = config.get('REDDIT', 'username')
	num_submissions = int(config.get('REDDIT', 'num_submissions'))
	option = config.get('REDDIT', 'option')
	reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)

	api_key = config.get('GOODREADS', 'key')

	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	for logger_name in ("praw", "prawcore"):
	   logger = logging.getLogger(logger_name)
	   logger.setLevel(logging.DEBUG)
	   logger.addHandler(handler)

	perform_query(reddit)
	


