#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from xml.sax.handler import ContentHandler
from xml.sax import make_parser,parseString

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from MiResumen.models import usuarios,micronotas

from email.utils import parsedate
from datetime import datetime


class myContentHandler(ContentHandler):

    def __init__ (self):
       self.inItem = False
       self.inTitle = False 
       self.inLink = False
       self.inGuid = False 
       self.inPubDate = False

       self.theTitle = ""
       self.theLink = ""
       self.theGuid= ""
       self.thePubDate = ""
       self.notero=""
       self.texto=""

    def startElement (self, name, attrs):
       if name == 'item':
          self.inItem = True
       elif self.inItem:
          if name == 'title':
             self.inTitle = True
             self.inNotero=True
          elif name == 'pubDate':
             self.inPubDate = True
          elif name == 'guid':
             self.inGuid = True
          elif name == 'link':
             self.inLink = True
    
    def endElement (self, name):
       if name == 'item':
          self.inItem = False
       elif self.inItem:

          if name == 'title':
             separausuario=self.theTitle.partition(':')
             self.notero = separausuario[0]
             self.texto = separausuario[2]
             self.inTitle = False

          elif name == 'pubDate':
             self.fecha = self.thePubDate
             self.inPubDate = False

          elif name == 'guid':
             ID=self.theGuid.partition('http://identi.ca/notice/')
             self.IDmicronota=ID[2]
             self.inGuid = False

          elif name == 'link':
             enlace = 'http://identi.ca/notice/'+self.IDmicronota
             try:
                nota=micronotas.objects.get(guid=self.IDmicronota)
             except:
                dbDate = datetime(*(parsedate(self.fecha)[:6]))
                nota=micronotas(title=self.texto,notero=self.notero,link=enlace,guid=self.IDmicronota,pubdate=dbDate)
                nota.save()        
             self.inLink = False
             
          self.theTitle=""
          self.thePubDate=""
          self.theGuid=""
          self.theLink=""
            
    def characters (self, chars):
       if self.inTitle:
          self.theTitle = self.theTitle + chars
       if self.inPubDate:
          self.thePubDate = self.thePubDate + chars
       if self.inGuid:
          self.theGuid= self.theGuid +chars
       if self.inLink:
          self.theLink = self.theLink + chars

