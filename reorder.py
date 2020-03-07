#!/usr/bin/env python3

from PyPDF2 import PdfFileWriter, PdfFileReader
import itertools
import re
import os

def subdiv(iterable, sub_length):
    """Subdivides any iterable into smaller iterables of length `sub_length`"""
    itr = iter(iterable)
    chunk = list(itertools.islice(itr, sub_length))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(itr, sub_length))

def nested_pdf_iter(reader):
    pages_per_section = int(input('8 or 16 pages per gathering/signature?: '))
    if pages_per_section == 8 or 16:
        if pages_per_section % 8 == 0:
            pages = [reader.getPage(x) for x in range(reader.numPages)]
            return list(subdiv(pages, pages_per_section))
        else:
            while pages_per_section % 8 != 0:
                pages_per_section = int(input('Only 8 or 16 page sections are supported at this time. Please re-enter.'))

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
        output = open(title + '-reordered.pdf', 'wb')
    writer.write(output)
    output.close()
    print("Your hot 'n' ready PDF awaits.")
    print("You'll find it this directory with '-reordered' appended to the filename.")

if __name__ == "__main__":
    pdf_path = input('Enter the path to your PDF (e.g. "path/to/your/pdf.pdf"):  ').strip()
    if pdf_path[-1] == '/':
        pdf_path = pdf_path[0:-1]
    regex = r"(?P<filename>[\w\-\_]+)(\.|$)"
    title = re.search(regex, pdf_path).groupdict()['filename']
    reader = PdfFileReader(pdf_path)
    if reader.getIsEncrypted():
        try:
            reader.decrypt('')
        except:
            print("This file was detected as encrypted. Attempted to decrypt with empty password, but failed.")
            print("If this file is not encrypted with a password, you can try decrypting with QPDF.")
            print("Please make sure you have installed QPDF before saying yes to the following prompt...")
            tryWithQPDF = input("Would you like to try decrypting with QPDF?: ")
            if re.match(r"(y|Y|Yes|yes)", tryWithQPDF):
                print("Working...")
                command=f"qpdf --decrypt --replace-input {pdf_path};"
                os.system(command)
                reader = PdfFileReader(pdf_path)
            else:
                sys.exit()
    writer = PdfFileWriter()
    nested_pages = nested_pdf_iter(reader)
    print("Working...")
    reordered = reorderer(nested_pages)
    write_reordered(reordered, title)
