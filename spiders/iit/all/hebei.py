import re

from pyquery import PyQuery as pq

from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save



def  parse_detail(html,url):
    doc=pq(html)
    data={}
    data["url"]=url
    data["title"]=doc("title").text()
    data["content"]=doc(".gxt-xilan-content ").text()
    s=doc(".gxt-xilan-date span").text()
    data["publish_time"]= re.search(r"(\d{4}-\d{1,2}-\d{1,2})",s).groups()
     #print(data["publish_time"])
    data["classification"]="河北工业和信息化厅"
    items=doc(".gxt-xilan-content  a").items()
    data["content_url"]=[]
    for  item in items:
        data["content_url"].append(item.attr("href"))
    # data["content_url"]=[ item.attr("href")  for item in doc(".gxt-xilan-content a").items()]
    #print(data["content_url"])
    print(data)
    # save(data)


def  parse_index(html):
     doc=pq(html)
     items=doc("ul.clear li a").items()
     for item in items:
            url=item.attr("href")
            url="http://gxt.hebei.gov.cn" + url
            html=get(url)
            parse_detail(html,url)
            #break         


if __name__ == "__main__":
    data={"filter_LIKE_TITLE":""}
    for i in range(1,12):
        url="http://gxt.hebei.gov.cn/hbgyhxxht/zcfg30/snzc/8743fba2-"+ str(i) +".html"    
        html=post(url,data=data)
        parse_index(html)
        #break