#!/usr/bin/env python3

"""
This script re-orders the pages of a pdf in preparation for printing and bookbinding.
The print imposition created by this script is appropriate for folded single-sheet 8-leaf signatures
(AKA "gatherings"). If the pdf is not evenly divisable by 16, blank pages are added to fill out
the last signature. 
"""

import PyPDF2
from itertools import islice
import re

def subdiv(iterable, sub_length):
    """Subdivides any iterable into smaller iterables of length <sublength>"""
    itr = iter(iterable)
    chunk = list(islice(itr, sub_length))
    while chunk:
        yield chunk
        chunk = list(islice(itr, sub_length))

def nested_pdf_iter(reader):
    pages_per_section = int(input('8 or 16 pages per section?: '))
    if pages_per_section == 8 or 16:
        if pages_per_section % 8 == 0:
            pages = [reader.getPage(x) for x in range(reader.numPages)]
            return list(subdiv(pages, pages_per_section))
        else:
            while pages_per_section % 8 != 0:
                pages_per_section = int(input('pages_per_section needs to be 8 or 16.'))
                nested_pdf_iter(reader)

def reorderer(nested_pages):
    reordered_pages = []
    if len(nested_pages[0]) == 16:
        order = [0, 15, 12, 3, 7, 8, 11, 4, 2, 13, 14, 1, 5, 10, 9, 6]
    elif len(nested_pages[0]) == 8:
        order = [0, 7, 3, 4, 6, 1, 5, 2]
    for section in nested_pages:
        for e in order:
            try:
                reordered_pages.append(section[e])
            except IndexError:
                reordered_pages.append(None)
    return reordered_pages

def write_reordered(reordered, title):
    for page in reordered:
        if page:
            writer.addPage(page)
        else:
            writer.addBlankPage()
    output = open(title + '.pdf', 'wb')
    writer.write(output)
    output.close()
    print("Your hot 'n' ready pdf awaits")

pdf_path = input('Enter the path to your PDF (e.g. "path/to/your/pdf"):  ').strip()
if pdf_path[-1] == '/':
    pdf_path = pdf_path[0:-1]
regex = r"(?P<filename>[\w\-\_]+)(\.|$)"
title = re.search(regex, pdf_path).groupdict()['filename']
reader = PyPDF2.PdfFileReader(pdf_path)
writer = PyPDF2.PdfFileWriter()
nested_pages = nested_pdf_iter(reader)
reordered = reorderer(nested_pages)
write_reordered(reordered, title)
