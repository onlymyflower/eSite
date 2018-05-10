# encoding=utf-8
# Author: onlymyflower
# Date: May 9, 2018

# The codes do something that disobey FBI warning
# so be carefull
# if it occurs site unreachable error, open your VPN, set global proxy
from download_page import download_page
from download_benzi import download_benzi


import requests
from bs4 import BeautifulSoup
import urllib# filename: test_ubuntu.py

from download_benzi import download_benzi
import requests
import os
import time
# from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Pool as ThreadPool
import argparse
import sys

MY_THREAD_NUM = 16

# Bug collection part
# 1 Content Warning
# handle the warning window


# URL config part

# QUERY = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=%E3%82%86%E3%82%8B%E3%82%86%E3%82%8A&f_apply=Apply+Filter&inline_set=dm_t"
# QUERY = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=yuruyuri&f_apply=Apply+Filter"
# "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=yuruyuri&f_apply=Apply+Filter"
QUERY1 = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=yuruyuri&f_apply=Apply+Filter&inline_set=dm_t"
QUERY1_NAME = "YuruYuri"
QUERY2 = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=Honkai+3&f_apply=Apply+Filter&inline_set=dm_t"
QUERY2_NAME = "Honkai 3"
# QUERY2 = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=Honkai+3&f_apply=Apply+Filter&inline_set=dm_t"
# QUERY2_NAME = "hatsune miku"
# QUERY2 = "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=Honkai+3&f_apply=Apply+Filter&inline_set=dm_t"
# QUERY2_NAME = "umaru"

# queries list
# "YuruYuri"
# "Honkai 3"
# Asuna
# Kantai Collection



QUERIES_TUPLE = [(QUERY2_NAME, QUERY2)] # , (QUERY1_NAME, QUERY1)

# "https://e-hentai.org/?f_doujinshi=on&f_manga=on&f_artistcg=on&f_gamecg=on&f_western=on&f_non-h=on&f_imageset=on&f_cosplay=on&f_asianporn=on&f_misc=on&f_search=%E3%82%86%E3%82%8B%E3%82%86%E3%82%8A&f_apply=Apply+Filter"
# get query

# ROOTPATH = os.getcwd()





def run_func(args):
    download_benzi(args[0], args[1])

def __main__():

    rootpath = os.environ['HOME'] + "/" +"weiyun/benzi" # /Users/HuangKan/GoogleDrive
    test_thread_num = MY_THREAD_NUM
    # var
    sourceUrls = []
    benzi_store_paths = []
    url_local_map = []

    for (query_name, query) in QUERIES_TUPLE: # QUERIES_TUPLE = [(QUERY_NAME, QUERY)]
        print(query_name)
        print(query)
        query_result = download_page(query).decode('utf-8')
        root_soup = BeautifulSoup(query_result,"lxml")

        thumbnails = root_soup.find_all("div", {"class", "id1"})

        # debug
        with open("debug.html","w") as f:
            print(query_result,file=f)

        for thumbnail in thumbnails:
            title = thumbnail.find("div", {"class", "id2"}) # title
            cover = thumbnail.find("div", {"class", "id3"}) # cover
            coverImg = cover.find("img")
            coverUrl = coverImg["src"]
            comment = thumbnail.find("div", {"class", "id4"}) # comment, todo
            a = title.find("a") # (C87) [Suzume Holic (Ryamu, Fon)] Endless Relation (YuruYuri)
            titleText = a.text
            sourceUrl = a["href"]
            benzi_store_path = rootpath + "/" + query_name + "/" + titleText
            print("mapping " + sourceUrl + " to " + benzi_store_path)

            # TODO, multithread
            url_local_map.append((sourceUrl,benzi_store_path))
            sourceUrls.append(sourceUrl)
            benzi_store_paths.append(benzi_store_path)

            # before, download one by one, too slow
            # download_benzi(sourceUrl,benzi_store_path)

            # another TODO, handle timeout and skip

        # Multithread
        # pool = ThreadPool(test_thread_num)
        # tasks = [(x, y) for x in sourceUrls for y in benzi_store_paths]
        # tasks = [(sourceUrls, benzi_store_paths) for sourceUrl, benzi_store_path in enumerate(url_local_map)]
        # with open("debug_tasks.txt", "w") as f:
            # print(tasks,file=f)
        # print(tasks)
        # results = pool.map(run_func, tasks)
        for (x, y) in url_local_map:
            download_benzi(x, y)


if __name__ == '__main__':
    __main__()
