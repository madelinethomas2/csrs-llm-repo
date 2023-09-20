# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:03:30 2023

@author: Madeline

converts any file type to plain text
handles structured formatting like tables and subsections

"""

# give the method a .dox file to convert to plain text
# https://python.langchain.com/docs/integrations/document_loaders/microsoft_word

from langchain.document_loaders import Docx2txtLoader
import sys
import os

def load_word_docx(filepath: str) -> str:
    
    # Import and load the ms word .docx file
    # Raise an exception if the file can't be found
    #try:
    print(filepath)
    filepath = os.path.abspath(filepath)
    print(filepath)
    loader = Docx2txtLoader(filepath)
    #except:
    print("ERROR - File not found")
        #sys.exit()
    data = loader.load()
    print(data) 
    
    return data