import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("浙江省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="浙江省药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall("urls\[i\]='(.+?)';",html)
    print(urls)
    for url in urls:
        url="http://mpa.zj.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,1):
        print(i)
        if i==0:
            url="http://mpa.zj.gov.cn/col/col1228988218/index.html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()