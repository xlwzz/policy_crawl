import re
import time
import json
import random
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_detail(html,url):
    alllog.logger.info("证监会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("#tdLawName").text()
    data["content"]=doc("#zhengwen").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zhengwen a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[1]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="证监会"
    data["url"]=url
    print(data)
    save(data)


def parse_index(html):
    data=json.loads(html)
    items=data["pageUtil"]["pageList"]
    for item in items:
        url="https://neris.csrc.gov.cn/falvfagui/rdqsHeader/mainbody?navbarId=1&secFutrsLawId=" + item["secFutrsLawId"]
        print(url)
        html = get(url,verify=False)
        parse_detail(html,url)
        time.sleep(random.randint(10,20))

def main():
    url="https://neris.csrc.gov.cn/falvfagui/rdqsHeader/informationController"
    for i in range(13,131):
        print(i)
        data={'pageNo': str(i), 'lawType': '1'}
        html=post(url,data=data,verify=False)
        parse_index(html)

if __name__ == '__main__':
    main()