# -*- coding: utf-8 -*-

class Action(object):
    def __init__(self, config):
        self.config = config
        
    def do(self):
        raise NotImplementError()