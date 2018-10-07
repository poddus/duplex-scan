#!/usr/bin/env python3

import sys
import os
import itertools
import logging
import pdfrw
from argparse import ArgumentParser

logging.basicConfig(
    format='%(levelname)s:%(message)s',
    level=logging.DEBUG)


def parse_arguments():
    parser = ArgumentParser(description='Sort the pages of a PDF file '
        'which was created by scanning a duplex print.')
    parser.add_argument('inputPath', help='path to a PDF file of a duplex scan.')
    
    return parser.parse_args()

def main(inputPath):
    indata = pdfrw.PdfReader(inputPath)
    
    inputFileBasename = os.path.basename(inputPath)
    outputPath = '{}-sorted{}'.format(
        os.path.splitext(inputFileBasename)[0],
        os.path.splitext(inputFileBasename)[1]
        )
    logging.debug('{} is the output path.'.format(outputPath))

    outdata = pdfrw.PdfWriter(outputPath)

    if len(indata.pages) % 2 != 0:
        raise RuntimeError('There are an uneven number of pages in the PDF file. '
            'Something must have gone wrong during the scan. Please check the '
            'input file and try again.')

    allPages = len(indata.pages)
    halfPages = allPages // 2
    logging.debug('{} is the number of pages.'.format(allPages))
    logging.debug('{} is half the number of pages.'.format(halfPages))


    oddPages = list(range(0, halfPages))    
    logging.debug('{} are the odd pages in order.'.format(oddPages))

    evenPages = list(reversed(range(halfPages, allPages)))
    logging.debug('{} are the even pages in order.'.format(evenPages))

    sortedPages = []
    for page in range(0, halfPages):
        sortedPages.append(oddPages[page])
        sortedPages.append(evenPages[page])

    logging.debug('{} is the list of sorted pages.'.format(sortedPages))

    for page in sortedPages:
        outdata.addpage(indata.pages[page])

    outdata.write()

if __name__ == '__main__':
    args = parse_arguments()
    main(args.inputPath)