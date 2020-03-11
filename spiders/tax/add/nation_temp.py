import re
import time
import random
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.redis_ import r



urls=[]
def parse_detail(html,url):
    alllog.logger.info("国家税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#fontzoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#fontzoom a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="国家税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".list li a").items()
    for item in items:
        url=item.attr("href")
        print(url)
        r.lpush("nation",url)

def main():
    for i in range(7,69):
        print(i)
        url="http://www.chinatax.gov.cn/chinatax/whmanuscriptList/n810755?_isAgg=0&_pageSize=20&_template=index&_channelName=最新文件&_keyWH=wenhao&page=" + str(i)
        print(url)
        headers={"Referer": "http://www.chinatax.gov.cn/chinatax/whmanuscriptList/n810755?_isAgg=0&_pageSize=20&_template=index&_channelName=%E6%9C%80%E6%96%B0%E6%96%87%E4%BB%B6&_keyWH=wenhao&page="+str(i-1),
                 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
        html=get(url,headers=headers)
        parse_index(html)
        time.sleep(random.randint)

    while True:
        url=r.lpop("nation")
        try:
            html = get(url)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)
        time.sleep(random.randint(1, 1))




if __name__ == '__main__':
    main()