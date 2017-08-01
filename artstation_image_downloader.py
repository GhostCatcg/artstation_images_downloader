
# coding: utf-8

import sys
import os
import urllib
from bs4 import BeautifulSoup

# url to parse
#url_to_parse = 'https://rocjoker0120.artstation.com/'
# in this directory will be created folder where all images will be saved
#dir_for_save = 'C:\\Users\\Michael\\Desktop\\Collages'


def image_downloader(url_to_parse, dir_for_save=os.getcwd()):
    sauce = urllib.request.urlopen(url_to_parse)
    soup = BeautifulSoup(sauce, 'lxml')

    artist_dir = url_to_parse.split('//')[1].split('.')[0]
    new_cwd = dir_for_save + '\\' + artist_dir
    if not os.path.exists(new_cwd):
        os.makedirs(new_cwd)
    os.chdir(new_cwd)

    # will print image number
    img_number = 1
    for url in soup.find_all('a'):
        #print(url.get('href'))
        # get artist projects page and collect links
        cur_url = url.get('href')
        if cur_url.find('projects') != -1:
            if url_to_parse.find('projects') == -1:
                project_url = url_to_parse + cur_url
            else:
                project_url = url_to_parse + '/' + cur_url.split('/')[-1]
            print(project_url)
            try:
                sauce = urllib.request.urlopen(project_url)
            except urllib.error.HTTPError as err:
                print(err.code)
            soup = BeautifulSoup(sauce, 'lxml')
            imgs = soup.find_all("img") 
            for img in imgs:
                #print(img.get('src'))
                img_url = img.get('src')
                if img_url.find('large') != -1:
                    img_name = project_url.split('/')[-1] + '-' + img_url.split("/")[-1].split("?")[0]
                    print(str(img_number) + '. ' + img_name)
                    try:
                        urllib.request.urlretrieve(img_url, img_name)
                        img_number = img_number + 1
                    except urllib.error.HTTPError as err:
                        print(err.code)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        url_to_parse = sys.argv[1]
        image_downloader(url_to_parse)
    elif len(sys.argv) > 2:
        url_to_parse = sys.argv[1]
        dir_for_save = sys.argv[2]
        image_downloader(url_to_parse, dir_for_save)
    else:
        print('\nPlease specify two arguments:\n1. URL to artist projects page\n2. Path to directory where you want to save folder with downloaded images\n *if only URL is given folder with images will be created in current directory')

