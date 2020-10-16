#!/usr/bin/python
# encoding: utf-8

import sys 
import requests 
import urllib3
import json
from urllib import quote
from workflow import (Workflow3, ICON_INFO, ICON_WARNING, ICON_ERROR, ICON_WEB,
                      ICON_SETTINGS, ICON_SYNC)
from bs4 import BeautifulSoup

# =================================================================================== #
# change this to the name of the wiki you want to query, e.g. 'lyrics', 'witcher'...
DEFAULT_WIKI = "dragonage"
# =================================================================================== #


# =================================================================================== #
# DO NOT CHANGE BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING :)
# =================================================================================== #
DEFAULT_URL = "https://%s.fandom.com/api/v1/Search/List"

class AlfredFandomSearch(object):
    """Workflow controller."""
    
    def __init__(self):
        self.wf = Workflow3(update_settings={'github_slug': 'manavortex/alfred-fandom-search'})

    def search(self):
        S = requests.Session()
        PARAMS = {
            "action": sys.argv[1],
            "format": "json",
            "limit": "10",
            "batches": "1",
            "minArticleQuality": "5", 
            "namespace": "0%2C14",
            "query": self.query
        }

        R = S.get(url=self.url, params=PARAMS)
        try:
            return R.json()["items"]
        except:
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
        
        for result in searchResults:

            title=result["title"]
            soup = BeautifulSoup(result["snippet"])
            snipText = (soup.get_text()[:75] + "..")            
            subtitle=snipText
            
            url=result["url"]
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
