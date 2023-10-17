#!/bin/bash/env python3

echo "Installing external libraries..."
# get exact versions for these, especially langchain
!pip install langchain 
!pip install unstructured
!pip install openai
!pip install chromadb
!pip install blosc2~=2.0.0
!pip install Cython
!pip install img2table
!pip install img2table pytesseract
!pip install sqlalchemy