# reddit_api_app #

## About ##
As a Reddit user, I had realised that when coming across a post I liked while browsing, I would often save it for later viewing, but never actually got around to doing so. 

This became particularly apparent when looking for new content on r/moviesuggestions and r/suggestmeabook, which both have a plethora of enthusiasts willing
to help match content with your tastes. 

This app, built with Django, accesses the Reddit API, collects my saved posts and the top-level comments from each, and displays them in the browser -
avoiding time consuming manual filtering, and eliminating the clutter of unnecessary replies from legitimate suggestion comments. 

**Project currently under construction**

## Features ##
* Authentication via the Reddit API using PRAW. 
* Saved posts retrieved from selected subreddits only. 
* Displays saved posts in easy-to-use index. 
	* Top level comments and number of upvotes displayed in table for each post. 
		* Bootstrap CSS used for styling. 
		* JavaScript allows filtering of saved comments by number of upvotes. 