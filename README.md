This script fetches books suggested in all top level comments of subreddit r/suggestmeabook.
You can modify parameter **option** to fetch either hot or top posts.
You can also modify the parameter **num_submissions** to set the number of posts parsed.

To run this script:
1. Create a config.ini by following the template config_sample.py
2. Make sure you have *python 3.6+* and *pip* installed.
3. Install requirements: 
	- `pip install praw`
	- `pip install requests`
4. Run script from console: `python main.py`

Once the script completes running, a csv file is created in the project directory, which contains name of a book and number of times it was mentioned by redditors.