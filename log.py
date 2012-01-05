# -*- coding: utf-8 -*-

__all__=["info", "debug", "error"]

def _log(level, m):
    print "[%s]: %s" % (str(level), str(m))

info = lambda m: _log("INFO", m)
debug = lambda m: _log("DEBUG", m)
error = lambda m: _log("ERROR", m)
    
    
    

