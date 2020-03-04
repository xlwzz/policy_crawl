import re
from pyquery import PyQuery as pq

from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save

def  parse_detail(html,url):
    doc=pq(html)
    data={}
    data["url"]=url
    data["title"]=doc(".content-article h1").text()
    s=doc(".messge span").text()
    data["publish_time"]= re.search(r"(\d{4}-\d{1,2}-\d{1,2})",s).groups()
    print(data["publish_time"])

    data["content"]=doc(".textbody ").text()
    items=doc(".textbody  a").items()
    data["content_url"]=[]
    for  item in items:
        data["content_url"].append(item.attr("href"))
    # data["content_url"]=[ item.attr("href")  for item in doc(".gxt-xilan-content a").items()]
    data["classification"]="山西省工业和信息化厅"
    print(data)

def  parse_index(html):  ##url
     doc=pq(html)
     items=doc("ul.list-ul li a").items()
     for item in items:
            url=item.attr("href")
            print(url)
            #url="http://gxt.hebei.gov.cn" + url
            # html=get(url)
            # parse_detail(html,url)
            # print(parse_detail(html,url))
            break      

if __name__ == "__main__":
    
    for i in range(1,110):  #####step1
        data={'strId' :  '15598075151552876', 'strParentId': '15598075151552876', 'id': '2', 'PageSizeIndex': i}
        url="http://gxt.shanxi.gov.cn/sxgxtweb/sxgxt/list.jsp"    
        html=post(url,data=data,code="gbk")
        parse_index(html)
        break