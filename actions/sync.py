# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from base_action import BaseAction
import requests
import log
import re

class Sync(BaseAction):
    def __init__(self, config):
        super(Sync, self).__init__(config)
        
        self.auth = None
        if self.config.USER != '' and self.config.PASS != '':
            self.auth = (self.config.USER, self.config.PASS)
    
    def do(self):
        # descargamos indice
        log.info(u"Descargando indice: '%s'" % str(self.config.URL))
                
        with requests.session(auth=self.auth) as c:
            r = c.get(self.config.URL + '/Magazine/Archive')
            r.raise_for_status()
        
            soup = BeautifulSoup(r.content)
            issues = soup.findAll("a", href=re.compile(u'/issue/\d+'))
        
            # recorremos los números
            for (numero, title, href) in self._iter_numeros(soup):
                print numero, title, href
                r = c.get(self.config.URL + href)
                r.raise_for_status()
                
                print r.content
                
            
    def _iter_numeros(self, soup):
        """
        Iterador sobre los numero de la revista.
        Devuelve la tupla:
            (numero, title, href)
        """
        issues = soup.findAll("a", href=re.compile(u'/issue/\d+'))
        
        for issue in issues:
            numero = issue.string.replace(u'Número ', '')
            href = issue['href']
            title = issue.findParents('tr', limit=1)[0].findAll('td')[2].string.replace(u'Tema de Portada: ', '').strip() 
            
            yield (numero, title, href)
                        
     
"""       
            <tr>
<td><img src="/pix/Full_PDFs.gif" width="12" height="12" alt="PDF Icon" border="0" /></td>
<td valign="bottom"><a name="01"></a><a href="/issue/01">
Número 01</a></td>
<td valign="bottom">Tema de Portada: Redes</td>
<td valign="bottom">
<b class="violet">DVD: Fedora Core3
</b>
</td>
</tr>"""
            
        
         
        
        
