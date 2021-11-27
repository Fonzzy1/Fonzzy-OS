#!/usr/bin/env python3
import argparse
import subprocess
import os
import re
import sys
import tempfile
import util


def main():
    EDITOR = os.environ.get('EDITOR','vim')
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', nargs='+')
    args = parser.parse_args()
    for url in args.urls:
        ## If its an image download and display
        if any(x in url for x in ['png','jpeg','jpg','giff','giffv','i.redd']):
            	p=subprocess.Popen('wget -O .tempdownload {};feh --scale-down --bg-color black --auto-zoom  .tempdownload; rm .tempdownload'.format(url),shell = True)
            	p.wait()
        ## If it is a youtube vid download and play        
        elif any(x in url for x in ['youtu','v.redd']):
                p=subprocess.Popen('youtube-dl --output ".youtube_dl" {}; mplayer -really-quiet  .youtube_dl*'.format(url),shell = True)
                p.wait()
                os.system("rm .youtube_dl*")
        ## If it is a pdf
        elif '.pdf' in url:
            	p=subprocess.Popen('wget -O .tempdownload {};mupdf -I  .tempdownload ; rm .tempdownload'.format(url),shell = True)
        else:           	
            subprocess.Popen('google-chrome {}'.format(url),shell = True)
            

if __name__ == '__main__':
    main()
