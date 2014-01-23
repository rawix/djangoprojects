#!/usr/bin/python

##########################################################################
# @Author : Bernard Hernandez Perez                                      #
# @Date : 30/07/2012.                                                    #
# @Description : Views that handle the urls selected.                    #
##########################################################################

##########################################################################
# Modified by: Rawan Nazmi-Issa Khozouz                                  #
# @Date : 16/08/2012.                                                    #
# @Description : Handle the vocabulary words                             #
##########################################################################

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

# Libraries
import os        # System library.
from datetime import datetime

#Vocabulary app
from vocabulary.models import Vocabulary

# Handler
class myContentHandler(ContentHandler):

    ## 
    # Method that is called when the object is created.
    ##
    def __init__ (self):

        #General variables.
        self.DEBUG = True

        # Create the sax parser.
        self.theParser = make_parser()
        self.theParser.setContentHandler(self)

		# Folder where the vocabulary are stored
        self.vocabularyFolder = '/data/vocabulary'

        # Getting paths.  
        self.filePath = os.path.abspath(__file__)
        self.rootPath = "/".join(self.filePath.split("/")[0:-1])
        self.vocabularyPath = self.rootPath + self.vocabularyFolder

        # Print information
        if self.DEBUG:
            print("The absolute path for vocabulary is " + self.vocabularyPath)
    
        # Vocabulary's Variables.    
        self.word = ""
        self.in_word = False

        self.acronym = ""
        self.in_acronym = False

        self.description = ""
        self.in_description = False

        self.link = ""
        self.in_link = False

        self.image = ""
        self.in_image = False

        #In 'Vocabulary' it means inside a vocabulary element
        self.in_vocabulary = False        

    ##
    # Method called when an element starts.
    ##
    def startElement (self, name, attrs):
                
       # Vocabulary
        if name == 'contents':
            self.unitNumber = attrs["number"]
            self.unitTitle = attrs["title"]
 
        if name == 'vocabulary':
            self.in_vocabulary = True

        elif self.in_vocabulary:
            if name == 'word': 
                self.in_word = True
            elif name == "acronym":
                self.in_acronym = True
            elif name == "description":   
                self.in_description = True
            elif name == "link":   
                self.in_link = True
            elif name == "image":   
                self.in_image = True

    ##
    # Method called when an element ends.
    ##
    def endElement (self, name):
        
        # Vocabulary
        if name == 'vocabulary':
            self.in_vocabulary = False
      
            # Add the new to the database.
            self.addVocabulary()

            # Reset the values.
            self.word = ""            # Word.
            self.acronym = ""        # acronym.
            self.description = ""     # Description.
            self.link = ""            # Link.
            self.image = ""           # Image.

        elif self.in_vocabulary:
            if name == "word":
                self.in_word = False
            elif name == "acronym":
                self.in_acronym = False
            elif name == "description":
                self.in_description = False
            elif name == "link":
                self.in_link = False
            elif name == "image":
                self.in_image = False

    ##
    # Method called when we are inside an element.
    ##
    def characters (self, chars):
        
        # Vocabulary.
        if self.in_word:
            self.word = self.word + chars

        if self.in_acronym:
            self.acronym = self.acronym + chars

        if self.in_description:
            self.description = self.description + chars

        if self.in_link:
            self.link = self.link + chars

        if self.in_image:
            self.image = self.image + chars

    ##
    # Method that parse the vocabulary.
    ##
    def parseVocabulary(self):

        # Print information.
        if self.DEBUG:
            print ("Parsing File")
        
        # Parse forlder recursively.
        self.parseFolder(self.vocabularyPath)

    ##
    # Method that list the content of the folder.
    ##
    def parseFolder(self, path):

        # List files in root.
        filesList = os.listdir(path)

        # Check if is a file or a directory
        for file in filesList:
            abspath = path + "/" + file

            if (os.path.isdir(abspath) == True):
                self.parseFolder(abspath)
            else:
                self.parseFile(abspath)

    ##
    # Method that parse one file.
    ##
    def parseFile(self, path):

        #Print nformation.
        if self.DEBUG:
            print(path)

        self.theParser.parse(path)

    ##
    # Add Vocabulary
    ##
    def addVocabulary(self):
        record = Vocabulary(unit=self.unitNumber, \
                            title=self.unitTitle, \
                            word=self.word, \
                            acronym=self.acronym, \
                            description=self.description, \
                            link=self.link, \
                            image=self.image)
        try:
            record.save()  	
        except:
            print "Word: " + self.word + " is duplicated."

