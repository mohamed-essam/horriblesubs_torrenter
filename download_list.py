import sys
from selenium.webdriver import PhantomJS
import scrapy
from os import mkdir
import os
import urllib2
from time import sleep

def downloadNonBatch(urlData):
    result = []
    for i in urlData.xpath('//div[re:test(@class, "release-links")]'):
        if(i.css("div::attr(class)").extract()[0].find("1080p") != -1):
            result.append(i.xpath('.//table').xpath('.//tbody').xpath('.//tr').xpath('.//td[re:test(@class, "hs-torrent-link")]').css("a::attr(href)").extract()[0])
    return result

def downloadBatch(urlData):
    return downloadNonBatch(urlData)[0]

def isBatch(urlData):
    return len(urlData.xpath('//div[re:test(@class, "hs-batches")]').css("div")) > 1

def getData(link):
    driver = PhantomJS()
    driver.get(link)
    sleep(5)
    content = driver.page_source
    response = scrapy.http.HtmlResponse(url=link, body=content, encoding="UTF-8")
    title = response.selector.xpath('//title/text()').extract()[0].split(u'\xbb')[0]
    print(title)
    if(isBatch(response)):
        print("yay")
        return [downloadBatch(response)], title
    print("nay")
    return downloadNonBatch(response), title

def download(link, path):
    listData, title = getData(link)
    print(listData)
    if(len(listData) > 1):
        mkdir(title)
        for link in listData:
            res = urllib2.urlopen(link)
            f = open(os.path.join(os.path.curdir, title, res.headers['Content-Disposition'].split('"')[1]), 'w')
            f.write(res.read())
            f.close()
    else:
        res = urllib2.urlopen(listData[0])
        f = open(os.path.join(os.path.curdir, res.headers['Content-Disposition'].split('"')[1]), 'w')
        f.write(res.read())
        f.close()

def main():
    args = sys.argv
    if(len(args) != 2 and len(args) != 3):
        print "Invalid Arguments!"
        return
    if(args[1] == "--help"):
        print "download_list file_name"
        return
    f = None
    try:
        f = open(args[1], "r")
    except:
        print "Invalid file name!"
        return
    links = f.readlines()
    folder_path = os.path.curdir
    if(len(args) == 3):
        folder_path = args[2]
    for link in links:
        torrents = download(link, folder_path)



if __name__ == "__main__":
    main()
