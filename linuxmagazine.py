# -*- coding: utf-8 -*-

import plac
from actions import sync, search
import config

@plac.annotations(
    action=("action", "positional", None, str, ['sync', 'search']),
)
def main(action):
    if action == 'sync':
        a = sync.Sync(config)
    else:
        a = search.Search(config)
        
    a.do()

if __name__ == '__main__':
    plac.call(main)