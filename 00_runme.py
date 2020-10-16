#!/usr/bin/python
# encoding: utf-8

import sys 
import requests 
import urllib3
import json
from urllib import (quote, urlencode)
from workflow import (Workflow3, ICON_INFO, ICON_WARNING, ICON_ERROR, ICON_WEB,
                      ICON_SETTINGS, ICON_SYNC)
from bs4 import BeautifulSoup

# =================================================================================== #
# change this to the name of the wiki you want to query, e.g. 'lyrics', 'witcher'...
DEFAULT_WIKI = ""
# =================================================================================== #


# =================================================================================== #
# DO NOT CHANGE BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING :)
# =================================================================================== #
DEFAULT_URL = "https://%s.fandom.com/api.php?"

class AlfredFandomSearch(object):
    """Workflow controller."""
    
    def __init__(self):
        self.wf = Workflow3(update_settings={'github_slug': 'manavortex/alfred-fandom-search'})

    

    def search(self):
        S = requests.Session()
        PARAMS = {
            "action": 'query',
            "list": 'search',            
            "format": "json",
            'prop': 'snippet',
            #"limit": "10",
            #"batches": "1",
            #"redirects": "resolve",
            #"minArticleQuality": "5", 
            "namespace": "0%2C14",
            "srsearch": self.query,
        }
        URL = url=self.url+urlencode(PARAMS)
        #print(URL)        
        R = requests.get(url=URL)
        #print(R.json())
        try:
            return R.json()['items']
        except Exception as e:
            try:
                return R.json()['query']['search']
            except Exception as e:
                print("\n\nException!!")
                print(e)
                print(R.json())
        return []

    def run(self, wf):
        """Run workflow."""
        
        args = self.wf.args # check for magic args
        
        if DEFAULT_WIKI == "": 
            self.wf.add_item(
                "Error: DEFAULT_URL in script filter not set", 
                subtitle="press enter to see readme", 
                arg="https://github.com/manavortex/alfred-fandom-search/blob/master/README.md", 
                valid=True
            )
            self.wf.send_feedback()
            return

        searchResults = {}
        try: 
            query = self.wf.decode(args[0])            
            self.query = quote(query)
            self.url = DEFAULT_URL % DEFAULT_WIKI
            searchResults = self.search()
        except IndexError: 
            searchResults = {}
        
        #print('\nresults')
        for result in searchResults:
           
            #print(result)
            
            title=result['title']
            soup = BeautifulSoup(result["snippet"], features="html.parser")
            snipText = (soup.get_text()[:75] + "..")            
            subtitle=snipText.encode('utf-8')
            
            url=''
            try:
                url = result['arg']
            except: 
                url = ('https://%s.fandom.com/wiki/' % DEFAULT_WIKI) + title.encode('utf-8')

            self.wf.add_item(
                title,
                subtitle=subtitle,
                arg=url,
                valid=True
            )#, icon=header_image_url, icontype='path')
            
        self.wf.send_feedback()
        


if __name__ == '__main__':

    search = AlfredFandomSearch()
    sys.exit(search.run(search.wf.run))
