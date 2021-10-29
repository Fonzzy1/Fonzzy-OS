#!/usr/bin/env python3
import argparse
import subprocess
import os
import newspaper
import re
import sys
import tempfile
from bs4  import BeautifulSoup
import util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', metavar='URL', nargs='+')
    args = parser.parse_args()
    for url in args.urls:
        link = [url]
        cur_url = url
        ext = False
        while link and not ext:
            (text,link) = [*link_loop(cur_url)]
            index = util.fuzzy_loop('links',text)
            if index == 'exit':
                ext = True
                os.system('clear')
            else:
                cur_url = link[index[0]]
		
def link_loop(url):
        link_list = []
        text_list = []
        base_url = '/'.join(url.split('/')[0:3]) 
        ## If its an image download and display
        if any(x in url for x in ['png','jpeg','jpg','giff','giffv']):
            	p=subprocess.Popen('wget -O .tempdownload {};cacaview .tempdownload; rm .tempdownload'.format(url),shell = True)
            	p.wait()
        ## If it is a youtube vid download and play        
        elif any(x in url for x in ['youtu','v.redd']):
                p=subprocess.Popen('youtube-dl --output ".youtube_dl" {}; mplayer -really-quiet -vo caca .youtube_dl'.format(url),shell = True)
                p.wait()
                os.system("rm .youtube_dl")
        ## If it is a pdf
        elif '.pdf' in url:
            	p=subprocess.Popen('wget -O .tempdownload {};pdftotext -layout .tempdownload - | vim -; rm .tempdownload'.format(url),shell = True)
        else:           	
            article = newspaper.Article(url)
            article.download()
            article.parse()
            link_list.append(url)
            text_list.append(article.title)
            htmlpage = article.html
            article.nlp()
            content = ''
            content += '**' + article.title +  '**\n* ' + ', '.join(article.authors)  + '*\n\n'
            content +=  article.summary + '\n\n'
            content += '#url \n' + url + '\n\n'
            content += '#KeyWords \n' + '\n'.join([*article.keywords]) + '\n\n'
            content += '#Contents\n' + article.text + '\n\n'
            content += '#Images\n' + '\n'.join(article.images) + '\n\n'
            content += '#Videos \n' + '\n'.join(article.movies) + '\n\n'
            content += '#Links \n\n'
            paras = BeautifulSoup(htmlpage, features="lxml").find_all('p')
            for para in paras:
                for link in para.find_all('a',attrs={'href': re.compile("/")}):
                    link_url =  str(link.get('href'))
                    if 'http' not in link_url:
                        link_url = base_url+link_url
                    content += '[' + link.text + '](' + link_url + ')\n'
                    link_list.append(link_url)
                    text_list.append(link.text)
            
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                tf.write(str.encode(content))
                tf.flush()
                subprocess.run("vim -c 'set filetype=rmd' {} ".format(tf.name), shell= True) 
                tf.seek(0)
                edited_message = tf.read()

            for j,linkset in enumerate([article.images, article.movies]):
                for i,x in enumerate(linkset):
                   text_list.append(['img','vid'][j] + str(i))
                   link_list.append(x) 
        return text_list,link_list 


if __name__ == '__main__':
    main()
