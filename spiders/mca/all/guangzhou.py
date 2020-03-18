import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("广州民政局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".content").text()
    data["content_url"]=[item.attr("href") for item in doc(".content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="广州民政局"
    data["url"]=url
    print(data["content"])
    save(data)

def parse_index(html):
    items=json.loads(html)
    for item in items["articles"]:
        url=item["url"]
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,5):
        print(i)
        url="http://mzj.gz.gov.cn/gkmlpt/api/all/344?page="+str(i)+"&sid=200022"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()