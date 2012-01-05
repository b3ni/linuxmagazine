# -*- coding: utf-8 -*-

import plac
from actions import sync, search
import config

@plac.annotations(
    action=("action", "positional", None, str, ['sync', 'search']),
    number=("number", "option", "n", int),
)
def main(action, number=None):
    if action == 'sync':
        a = sync.Sync(config)
    else:
        a = search.Search(config)
        
    a.do(number)

if __name__ == '__main__':
    plac.call(main)
