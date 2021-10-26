#!/usr/bin/env python3
import argparse
import subprocess
import os
import newspaper
import re
import sys
import tempfile

def main():
    EDITOR = os.environ.get('EDITOR','vim')  
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', nargs='+')
    args = parser.parse_args()
    for url in args.urls:
        ## If its an image download and display
        if any(x in url for x in ['png','jpeg','jpg','giff']):
            	p=subprocess.Popen('wget -O .tempdownload {};cacaview .tempdownload; rm .tempdownload'.format(url),shell = True)
            	p.wait()
        ## If it is a youtube vid download and play        
        elif 'youtu' in url:
                p=subprocess.Popen('youtube-dl -f  worst --output ".youtube_dl" {}; mplayer -really-quiet -vo caca .youtube_dl'.format(url),shell = True)
                p.wait()
                os.system("rm .youtube_dl")
        ## If it is a pdf
        elif '.pdf' in url:
            	p=subprocess.Popen('wget -O .tempdownload {};pdftotext -layout .tempdownload - | vim -; rm .tempdownload'.format(url),shell = True)
        else:           	
            article = newspaper.Article(url)
            article.download()
            article.parse()
            content = article.title  + '\n\n' + url + '\n\n' + article.text
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                tf.write(str.encode(content))
                tf.flush()
                subprocess.call([EDITOR, tf.name])
                tf.seek(0)
                edited_message = tf.read()

		


if __name__ == '__main__':
    main()
