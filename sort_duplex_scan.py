#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import pdfrw


def parse_arguments():
    parser = ArgumentParser(
        description='Sort the pages of a PDF file '
        'which was created by scanning a duplex print. '
        'output path is the path of the PDF file containing the odd pages'
    )
    parser.add_argument(
        'input_paths',
        nargs='+',
        help='Path(s) to PDF file(s) to be processed. Input either two files, odd pages first, even pages second '
             'or a single file with both.'
    )
    return parser.parse_args()


def main(input_paths):
    if len(input_paths) > 2:
        raise ValueError('program only accepts 1 or 2 files')

    input_file_basename = os.path.basename(input_paths[0])
    output_path = '{}-sorted{}'.format(
        os.path.splitext(input_file_basename)[0],
        os.path.splitext(input_file_basename)[1]
    )
    out_data = pdfrw.PdfWriter(output_path)

    if len(input_paths) == 2:
        odd_data = pdfrw.PdfReader(input_paths[0])
        even_data = pdfrw.PdfReader(input_paths[1])

        if len(odd_data.pages) != len(even_data.pages):
            raise RuntimeError(
                'The number of pages in the input files are unequal. '
                'Something probable went wrong during the scan. Please check the '
                'input files and try again.'
            )

        current_even_page = list(range(0, len(even_data.pages)))
        for current_odd_page in range(0, len(odd_data.pages)):
            out_data.addpage(odd_data.pages[current_odd_page])
            out_data.addpage((even_data.pages[current_even_page.pop()]))  # in practice .pop() reverses the list

        out_data.write()
    elif len(input_paths) == 1:
        in_data = pdfrw.PdfReader(input_paths[0])

        if len(in_data.pages) % 2 != 0:
            raise RuntimeError(
                'There are an uneven number of pages in the PDF file. '
                'Something must have gone wrong during the scan. Please check the '
                'input file and try again.'
            )

        all_pages = len(in_data.pages)
        half_pages = all_pages // 2
        odd_pages = list(range(0, half_pages))

        even_pages = list(reversed(range(half_pages, all_pages)))

        sorted_pages = []
        for page in range(0, half_pages):
            sorted_pages.append(odd_pages[page])
            sorted_pages.append(even_pages[page])

        for page in sorted_pages:
            out_data.addpage(in_data.pages[page])

        out_data.write()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.input_paths)
