#!/usr/bin/env python3
import argparse
import subprocess
import os
import newspaper
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', nargs='+')
    args = parser.parse_args()

    for url in args.urls:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        content = url + '\n\n' + article.text
        lines = content.count('\n')
        if lines <= 20:
            print(url)
            print(article.text)
            
        dir = input('Save to dir: ')
        if dir != '':
            try:
                os.chdir(dir)
            except FileNotFoundError:
                os.chdir('/home/fonzzy/Downloads')    
            if any(x in url for x in ['.pdf','.mp4','.mp3','png','jpeg']):
            	p=subprocess.Popen('wget {}'.format(url),shell = True)
            	p.wait()
            elif 'youtube' in url:
            	p=subprocess.Popen('youtube-dl -f best {}'.format(url),shell = True)
            	p.wait()
            else:
                p=subprocess.Popen('wkhtmltopdf "{}" "{}".pdf > /dev/null 2>&1'.format(url,article.title.replace(' ','_')),shell = True)    
                p.wait()
            
		


if __name__ == '__main__':
    main()
