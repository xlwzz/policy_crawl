import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post

from policy_crawl.common.save import save



def parse_detail(html,url):
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".body").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".body a").items()]
    data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    data["classification"]="河北省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

#https://rst.hebei.gov.cn/a/tongzhi/2019/0531/7451.html
def parse_index(html):
    doc=pq(html)
    items=doc(".typelist li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="https://rst.hebei.gov.cn" + url
        html=get(url)
        parse_detail(html,url)
        time.sleep(random.randint(1,3))



def main():
    for i in range(1,46):
        url="https://rst.hebei.gov.cn/a/tongzhi/list_6_"+ str(i)+".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()