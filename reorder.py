#!/home/zach/anaconda3/bin/python3
# -*- coding: utf-8 -*-

"""
This script re-orients(*not yet*) and re-orders the pages of a pdf in preparation for printing.
The print imposition created by this script is appropriate for folded single-sheet 8-leaf signatures
(AKA "gatherings"). If the pdf is not evenly divisable by 16, blank pages are added to fill out
the last signature.

To do: - make 4-leaf signature option.
       - default to which imposition requires least blank pages, but allow user to choose if desired
       - re-orient and collate pages to single sheet of 8 pages (per side, 2 x 4) 
"""

import PyPDF2
from itertools import islice

def subdiv(iterable, sub_length):
    """Subdivides any iterable into smaller iterables of length <sublength>"""
    itr = iter(iterable)
    chunk = list(islice(itr, sub_length))
    while chunk:
        yield chunk
        chunk = list(islice(itr, sub_length))

def create_pdf_reader(pdf=None):
    if not pdf:
        pdf = open('pdfs/category-theory.pdf', 'rb')
        return PyPDF2.PdfFileReader(pdf)
    else:
        pdf = open(pdf, 'rb')
        return PyPDF2.PdfFileReader(pdf)

def create_pdf_writer():
    return PyPDF2.PdfFileWriter()

def create_nested_pdf_iterable(pdf_reader):
    pages_per_section = int(input('8 or 16 pages per section?: '))
    if pages_per_section == 8 or 16:
        if pages_per_section % 8 == 0:
            pages = [pdf_reader.getPage(x) for x in range(pdf_reader.numPages)]
            return list(subdiv(pages, pages_per_section))
        else:
            while pages_per_section % 8 != 0:
                pages_per_section = int(input('pages_per_section needs to be 8 or 16.'))
                create_nested_pdf_iterable(pdf_reader)

def pdf_reorderer(nested_pdf_iterable):
    reordered_pages = []
    if len(nested_pdf_iterable[0]) == 16:
        order = [0, 15, 12, 3, 7, 8, 11, 4, 2, 13, 14, 1, 5, 10, 9, 6]
    elif len(nested_pdf_iterable[0]) == 8:
        order = [0, 7, 3, 4, 6, 1, 5, 2]
    for section in nested_pdf_iterable:
        for e in order:
            try:
                reordered_pages.append(section[e])
            except IndexError:
                reordered_pages.append(None)
    return reordered_pages

def write_reordered_pdf(reordered_pages):
    for page in reordered_pages:
        if page:
            pdf_writer.addPage(page)
        else:
            pdf_writer.addBlankPage()
    pdf_output = open('pdfs/cat-theory-reordered.pdf', 'wb')
    pdf_writer.write(pdf_output)
    pdf_output.close()
    print(f'Your hot \'n\' ready pdf awaits')


pdf_reader = create_pdf_reader()
pdf_writer = create_pdf_writer()
nested_pdf_iterable = create_nested_pdf_iterable(pdf_reader)
reordered_pages = pdf_reorderer(nested_pdf_iterable)
write_reordered_pdf(reordered_pages)
