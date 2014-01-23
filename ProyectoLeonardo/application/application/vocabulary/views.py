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


# Libraries.
# HTTP mssages.
from django.http import HttpResponse
from django.http import Http404  

# HTML short way for rendering.
from django.shortcuts import render_to_response, get_object_or_404

# HTML rendering libraries.
from django.template import Context, loader

# Cross Site Request Forgery protection
from django.views.decorators.csrf import csrf_exempt

# Data base tables.  
from models import Vocabulary

# Own libraries.
import parserXML

# Create the XML parser.
parser = parserXML.myContentHandler();

# =======================================================================
#                       LOADING DATA METHODS
# =======================================================================

# Name : LOAD VOCABULARY
# This method removes all the words that are in the database and
# reload them from xml files at /data/vocabulary.

def loadVocabulary(request):

    # Remove all the questions.
    Vocabulary.objects.all().delete()

    # Parse the words.
    parser.parseVocabulary()

    # return the template.
    return index(request)

# ============================================================================================
#                                   HANDLE METHODS
# ============================================================================================

# ----------------------------------------------------------------------
# Name : INDEX
# To render correctly the main view (home).
def index(request):
    return render_to_response('home.html')
     
# ----------------------------------------------------------------------
# Name : UNIT
# When the user clicks in a unit, we should render correctly the content
# of the web page with the menu of the words
def unit(request, unit_id):

    # Get all words in the database according the unit selected (if there is no words [])
    try:   
        word_list = Vocabulary.objects.filter(unit=unit_id) 

        # No word selected      
        print_word = False

    except Vocabulary.DoesNotExist:
        raise Http404

    # Return the template
    return render_to_response('word.html', {'print_word': print_word, 'word_list': word_list})

#Desactivation of CSRF
@csrf_exempt

# ----------------------------------------------------------------------
# Name : WORD
# When the user selects a word, we should render correctly the content
# of the web page with the selected word 
def word(request):

    if request.method == "GET":
        # Return the template
        return index(request)

    if request.method == "POST":
        # Get the word pk.
        current_word_pk = request.POST['choosed_word_pk']

        try:
            # Get the word selected
            word_parameter = Vocabulary.objects.get(pk=current_word_pk)	
 
            # Get all words from the database tables   
            word_list = Vocabulary.objects.filter(unit=word_parameter.unit) 

            #There is a word selected
            print_word = True

        except Vocabulary.DoesNotExist:
            raise Http404

        # Return the template
        return render_to_response('word.html', {'print_word': print_word, 'word_list': word_list, 'word_parameter': word_parameter})

