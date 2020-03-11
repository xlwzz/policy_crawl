import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("浙江省税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".info-cont").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".info-cont a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="浙江省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)" target="_blank"',html)
    for url in urls:
        url = "http://zhejiang.chinatax.gov.cn" + url.replace("%2F","/")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://zhejiang.chinatax.gov.cn/module/web/jpage/morecolumndataproxy.jsp?"
    for i in range(0,1):
        params={'startrecord':str(i*30), 'endrecord': str(i*30+30), 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '15', 'path': '%2F', 'columnid': '8409%2C8414', 'sourceContentType': '3', 'unitid': '95504', 'keyWordCount': '30', 'webname': '%E5%9B%BD%E5%AE%B6%E7%A8%8E%E5%8A%A1%E6%80%BB%E5%B1%80%E6%B5%99%E6%B1%9F%E7%9C%81%E7%A8%8E%E5%8A%A1%E5%B1%80'}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()