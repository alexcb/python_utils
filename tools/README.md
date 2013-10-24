message_appender.py
===================

    input file: sample_code.py

    for _ in xrange(10):
        print textwrap.dedent('''
        hello world
        ''')


    $ python2.7 message_appender.py 'hello world' "please to meet" sample_code.py --stdout
    for _ in xrange(10):
        print textwrap.dedent('''
        hello world
        please to meet
        ''')

scptar
======

tars up a directory, sends it over ssh, then uncompresses it on the other side.
This is useful for copying a large number of files for instances where scp is too
slow.

This tool simply prints out a command to run:

    tar czf - <input_path> | ssh user@hostname "cd path; tar xvzf -"
