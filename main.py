"""
Beautiful soup allows us to use HTML or xml and grab specific types of data - it allows us to parse.
We use it to convert from a string to an object that we can manipulate and use.

Requests allows us to download the HTML

In this case, all we want to grab is any link from Hacker.com that has 100 points (votes) or more.
"""

import requests
from bs4 import BeautifulSoup
import pprint

# web browser without the actual window
res = requests.get("https://news.ycombinator.com/")

# convert from string to something we can use.
soup = BeautifulSoup(res.text, 'html.parser')

# will get body
#print(soup.body)

# finds all div objects in list form
#print(soup.find_all('div'))

# finds all a tags (links) in list form
#print(soup.find_all('a'))

# select uses css selector - a list of ways to grab elements
#print(soup.select('.score'))

article_title = soup.select('.titleline > a')
subtext = soup.select('.subtext')


# function that will organise the output of the articles from highest to lowest.
def sort_stories_by_votes(news_list):
    return sorted(news_list, key=lambda k: k['Votes'], reverse=True)

# will receive links and votes
def create_custom_hacker_news(links, subtext):

    # new hacker news list which is empty - we only want text and no HTML.
    news = []

    # enumerate gives us an index
    # it also allows us to grab the subtext from the links list
    # where we use links within the for loop, we can actually replace with item
    for index, item in enumerate(links):
        # grab the title of each link - getText() gets the text inside of the tag
        title = links[index].getText()
        # grabbing the href. If there are none, or link broken, default to None.
        href = links[index].get('href', None)

        # as this stands, there is a chance that we may encounter a list index out of bounds error.
        # this is due to the fact that some articles may not have any points (rare, but possible).
        # therefore, our programme can think there are more article links than article points.
        # the vote variable and the if statement below fixes this.
        # instead of grabbing points, we are going to get the class subtext from Hacker News page.
        # Within this subtext class on the Hacker News page is the score. We are able to check if there is a score
        vote = subtext[index].select('.score')
        if len(vote):

            # we convert votes to an int and replace the text with an empty string
            points = int(vote[0].getText().replace(' points', ""))

            # only display articles with 100 points or more
            if points > 99:
                # use a dictionary to append title and href link to new list
                news.append({'Article Title': title, "Article Link": href, 'Votes': points})

    return sort_stories_by_votes(news)

# pprint is a module that makes the output easier to reade
pprint.pprint(create_custom_hacker_news(article_title, subtext))





