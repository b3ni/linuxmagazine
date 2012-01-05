# -*- coding: utf-8 -*-

class BaseAction(object):
    def __init__(self, config):
        self.config = config
        
    def do(self, number=None):
        raise NotImplementError()
