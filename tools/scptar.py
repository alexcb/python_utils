#!/usr/bin/env python2.7
import argparse
import subprocess


def get_parser():
	parser = argparse.ArgumentParser(description='pre-compressed scp.')
	parser.add_argument('local_path', nargs='+', help='local file/dir to copy')
	parser.add_argument('remote_path', help='remote path')
	return parser

def main():
	parser = get_parser()
	args = parser.parse_args()
	host, remote_path = args.remote_path.split(':', 1)
	cmd = 'tar czf - %s | ssh %s "cd %s; tar xvzf -"' % (
		' '.join(['"%s"' % x for x in args.local_path]),
		host,
		remote_path,
		)
	print 'Running: %s' % cmd
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
	main()
