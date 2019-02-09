#!/usr/bin/python
# -*- coding: latin-1 -*-

__author__ = 'Robin Flume'
__license__ = 'MIT'
__version__ = '0.1'

import argparse
import fitz
import re
import codecs
import unicodedata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', help='Path to your PDF file', required=True)
    parser.add_argument('--clippings', help='Path to your "My Clippings.txt" file', required=True)
    parser.add_argument('--title', help='Full book title line as found in the "My Clippings.txt"', required=True)
    parser.add_argument('--outfile', default='highlighted.pdf', help='(Optional) Path for the highlighted PDF file')
    args = parser.parse_args()

    if args.book == args.outfile:
        raise SystemExit('Paths of "--book" and "--outfile" must differ!')

    highlight_pdf(args.book, args.clippings, args.outfile, args.title)


def highlight_pdf(book, clippings, outfile, title):
    # open orig pdf
    doc = fitz.open(book)
    # open empty pdf object
    docHighlighted = fitz.open()

    # helpers
    lineProcessNext = 0
    lineHightlightNext = 0
    pageLastProcessed = -1

    # Read clippings
    with open(clippings) as f:
        clippingLines = f.readlines()

    # process clippings
    for line in clippingLines:

        # line encoding and linefeed elimination
        line.decode('utf-8')
        lineHex = ':'.join(x.encode('hex') for x in line)
        lineHex = lineHex.replace(':0d:0a', '')
        line = ''.join(chr(int(e, 16)) for e in lineHex.split(':'))

        # processing parsed lines
        if title in line:
            lineProcessNext = 1
            continue

        elif lineProcessNext == 0:
            continue

        elif line == '==========':
            lineProcessNext = 0
            continue

        elif lineHightlightNext == 0:
            targetPage = int(re.search(r'\d+', line).group()) - 1
            clippingLines.pop(0)
            lineHightlightNext = 1
            continue

        else:
            if (pageLastProcessed == targetPage):
                page = docHighlighted[-1]   # get page from highlighted doc
                textInstances = page.searchFor(line)
                for inst in textInstances:
                    #highlight = page.addHighlightAnnot(inst)
                    page.addHighlightAnnot(inst)
                lineProcessNext = 0
                lineHightlightNext = 0
                pageLastProcessed = targetPage
                continue

            elif (pageLastProcessed != (targetPage - 1)):
                docHighlighted.insertPDF(doc,
                                        from_page = (pageLastProcessed + 1),
                                        to_page = (targetPage - 1)
                                        )

            page = doc[targetPage]
            textInstances = page.searchFor(line)

            for inst in textInstances:
                #highlight = page.addHighlightAnnot(inst)
                page.addHighlightAnnot(inst)

            docHighlighted.insertPDF(doc,
                                    from_page = targetPage,
                                    to_page = targetPage
                                    )

            # update helper vars
            lineProcessNext = 0
            lineHightlightNext = 0
            pageLastProcessed = targetPage

    # add remaining (unhighlighted) pages after last page
    if (targetPage + 1) < doc.pageCount:
        docHighlighted.insertPDF(doc,
                                from_page = targetPage + 1,
                                to_page = doc.pageCount
                                )

    docHighlighted.save(outfile, garbage=4, deflate=True, clean=True)
    print('\nA copy of your PDF was successfully highlighted and saved at "' + outfile + '".\n')


if __name__=='__main__':
    main()