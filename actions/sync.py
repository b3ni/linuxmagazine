# -*- coding: utf-8 -*-

from action import Action

class Sync(Action):
    def do(self):
        print self.config.URL