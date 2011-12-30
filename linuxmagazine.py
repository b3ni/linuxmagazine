# -*- coding: utf-8 -*-
import plac
import actions
import config

@plac.annotations(
    action=("action", "positional", None, str, ['sync', 'search']),
)
def main(action):
    if action == 'sync':
        a = actions.sync.Sync(config)
    else:
        a = actions.search.Search(config)
        
    a.do()

if __name__ == '__main__':
    plac.call(main)