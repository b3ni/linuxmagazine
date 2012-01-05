# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from base_action import BaseAction
import requests
import log
import re
import os

class Sync(BaseAction):
    def __init__(self, config):
        super(Sync, self).__init__(config)
        
        # autenticacion
        self.auth = None
        if self.config.USER != '' and self.config.PASS != '':
            self.auth = (self.config.USER, self.config.PASS)
            
        # si tenemos autenticacion modificamos el path base de revistas
        self.url_numero_digital = self.config.URL + '/digital/issue'
        self.url_numero_libre = self.config.URL + '/issue'
        self.url_numero = self.url_numero_libre
        if self.auth is not None:
            self.url_numero = self.url_numero_digital
                        
        # creamos directorio base si no existe
        try:
            os.mkdir(self.config.DIR_STORE)
        except:
            pass
        
        # session request
        self.s = requests.session(auth=self.auth)
    
    def do(self, number=None):
        if number is not None:
            # descargamos un numero concreto
            self._sync_number(number)
        else:
            # descargamos indice
            log.info(u"Descargando indice: '%s'" % str(self.config.URL))
            
            r = self.s.get(self.config.URL + '/Magazine/Archive')
            r.raise_for_status()
            
            # recorremos los números
            for (numero, title, href) in self._iter_numeros(r.content):
                self._sync_number(int(numero))
                        
    def _sync_number(self, number):        
        url_numero = self.url_numero + '/%02d' % number        
        log.info(u"Descargando numero [%s] '%s'" % (str(number), str(url_numero)))
        
        # creamos directorio dentro de store
        directorio_numero = os.path.join(self.config.DIR_STORE, "%03d" % number)
        try:
            os.mkdir(directorio_numero)
        except Exception:
            pass
        
        # leemos page
        r = self.s.get(url_numero)
        if r.status_code != requests.codes.ok:
            # número libre
            url_numero = self.url_numero_libre + '/%02d' % number
            log.info(u"Descargando numero [%s] '%s'" % (str(number), str(url_numero)))
            r = self.s.get(url_numero)             
            
        r.raise_for_status()
        
        for index, (title, pdfhref, pdfname, pdfsize, descripcion) in enumerate(self._iter_seccion(r.content)):
            # fichero destino
            path_file = os.path.join(directorio_numero, "%02d_%s_%s.pdf" % (index + 1, title, pdfhref))
            
            # comprobamos si existe
            if os.path.exists(path_file):
                continue
                                
            # descargamos                    
            urlpdf = url_numero + '/' + pdfhref
            log.info(u"Descargando PDF: '%s'" % str(urlpdf))
            
            r = self.s.get(urlpdf)
            r.raise_for_status()
            
            # salvamos pdf
            f = open(path_file, 'wb')
            f.write(r.content)
            f.close()
            
    def _iter_numeros(self, content):
        """
        Iterador sobre los numero de la revista.
        Devuelve la tupla:
            (numero, title, href)
        """
        soup = BeautifulSoup(content)
        issues = soup.findAll("a", href=re.compile(u'/issue/\d+'))
        
        for issue in issues:
            numero = issue.string.replace(u'Número ', '')
            href = issue['href']
            title = issue.findParents('tr', limit=1)[0].findAll('td')[2].string.replace(u'Tema de Portada: ', '').strip() 
            
            yield (numero.strip(), title.strip(), href.strip())
            
    def _iter_seccion(self, content):
        """
        Iterador sobre las secciones de una revista.
        Devuelve:
            (title, pdfhref, pdfname, pdfsize, descripcion)
        """
        soup = BeautifulSoup(content)
        uls = soup.findAll('li')
        
        for ul in uls:
            b = ul.contents[0]
            
            if b.name != 'b':
                continue
            
            title = b.string.strip().replace(':', '')
                
            a = ul.contents[2]
            if a.name != 'a':
                continue
            
            pdfhref = a['href']
            pdf = a.string.split('[')                
            pdfname = pdf[0].strip().replace(':', '')
            pdfsize = pdf[1].split(',')[1].strip().replace(']', '')
                                            
            descripcion = '\n'.join([t.string.strip() for t in ul.contents[3:]])
            
            yield (title, pdfhref, pdfname, pdfsize, descripcion)
        
