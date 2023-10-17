# -*- coding: utf-8 -*-

import pdfkit
# This code comes directly from adobe - https://www.adobe.com/acrobat/hub/how-to-convert-pdf-to-html.html
# So presumably, this extracts in the same way as acrobat's html export option.

def pdf2html(file):
    
    # Read the PDF file
    pdf_file = open(file, "rb")
    
    # Convert the PDF to HTML
    html_file = pdfkit.from_pdf(pdf_file, "%shtml" % file[:-3])
    # error here, module 'pdfkit' has no attribute 'from_pdf'
    
    # Close the PDF file
    pdf_file.close()
    
file = './RCIP.pdf'
pdf2html(file)