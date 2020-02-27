#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3
# To use Alfred 3+ feedback mechanism:
# from workflow import Workflow3
UPDATE_SETTINGS = {'github_slug': 'manavortex/alfred-fandom-search'}

__version__ = '1.0'

def main(wf):
    
  args = wf.args # check for magic args
  wiki = "community" if len(args) == 0 else args[0]
  wf.settings['url'] = wiki
  wf.settings.save
  wf.add_item(title="Default wiki set", subtitle="%s.fandom.com" % wiki)            
  wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))

