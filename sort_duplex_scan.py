#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import pypdf


def parse_arguments():
    parser = ArgumentParser(
        description='Sort the pages of a PDF file '
        'which was created by scanning a duplex print. '
        'output path is the path of the PDF file containing the odd pages'
    )
    parser.add_argument(
        'input_paths',
        nargs='+',
        help='Paths to two PDF files to be processed. '
             'Input odd pages first, even pages second.'
    )
    parser.add_argument(
        '-k', '--keep',
        action='store_true',
        help='keep input files and create a new file as output.'
    )
    return parser.parse_args()


def main(args):

    if len(args.input_paths) != 2:
        raise ValueError('program only accepts 2 files')

    input_file_basename = os.path.basename(args.input_paths[0])

    output_data = pypdf.PdfWriter()

    if len(args.input_paths) == 2:
        input_data_odd = pypdf.PdfReader(args.input_paths[0])
        input_data_even = pypdf.PdfReader(args.input_paths[1])

        if len(input_data_odd.pages) != len(input_data_even.pages):
            raise RuntimeError(
                'The number of pages in the input files are unequal. '
                'Something must have gone wrong during the scan. '
                'Please check the input files and try again.'
            )

        output_data.append(input_data_odd)
        position = 1
        for page in reversed(list(range(0, len(input_data_even.pages)))):
            output_data.merge(
                position=position,
                fileobj=input_data_even,
                pages=([page]))
            position += 2

    if args.keep:
        output_path = '{}-sorted{}'.format(
            os.path.splitext(input_file_basename)[0],
            os.path.splitext(input_file_basename)[1]
        )
    else:
        output_path = 'sorted.pdf'

    output_data.write(output_path)

    if not args.keep:
        for path in args.input_paths:
            os.remove(path)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
