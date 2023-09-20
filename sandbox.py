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

loader = Docx2txtLoader("proposal.docx")

data = loader.load()

print(data)