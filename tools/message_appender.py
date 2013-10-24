import argparse
import re
import os

def get_parser():
    parser = argparse.ArgumentParser(description='Search for all instances of <search_text> and append <append_text> while maintaining the same indentation.')
    parser.add_argument('--prepend',
                       action='store_false',
                       dest='append',
                       default=True,
                       help='prepend \'append_text\' before all instances of \'search_text\' rather than after'
                       )
    parser.add_argument('--stdout',
                       action='store_true',
                       default=False,
                       help='print changes to stdout rather than modifying the file on disk'
                       )

    parser.add_argument('search_text',
                       help='text to search for'
                       )
    parser.add_argument('append_text',
                       help='text to append after all instances of \'search_text\''
                       )

    parser.add_argument('file',
                       nargs='+',
                       help='files to search'
                       )
    return parser

whitespace_re = re.compile(r'^([ \t]*)')
def search_and_append(text, search_text, append_text, append=True):
    lines = text.split('\n')
    output_lines = []
    for line in lines:
        if append is True:
            output_lines.append(line)

        if search_text in line:
            m = whitespace_re.match(line)
            indentation_whitespace = m.group(1)
            output_lines.append('%s%s' % (indentation_whitespace, append_text))

        if append is False:
            output_lines.append(line)
    return '\n'.join(output_lines)

def get_back_up_filename(filename):
    i = 0
    backup_filename = filename + '.bkup'
    while os.path.isfile(backup_filename):
        i += 1
        backup_filename = filename + '.bkup(%i)' % i
    return backup_filename

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    
    for file in args.file:
        with open(file, 'r') as fp:
            text = fp.read()
        text = search_and_append(text, args.search_text, args.append_text, args.append)
        if args.stdout:
            print text
        else:
            os.rename(file, get_back_up_filename(file))
            with open(file, 'w') as fp:
                fp.write(text)

