import time
import random
import requests
from my_fake_useragent import UserAgent

headers={"Useragent":UserAgent().random()}

def get(url,params=None,headers=headers,code="utf-8",**kwargs):
    try:
        res=requests.get(url,params=params,headers=headers,**kwargs)
        if res.status_code in [200,201,301]:
                return res.content.decode(code)
        else:
            time.sleep(random.randint(1,5))
            ret=get(url,params=None,headers=headers,code="utf-8",**kwargs)
            return ret
    except ConnectionError:
        time.sleep(random.randint(1, 5))
        ret = get(url, params=None, headers=headers, code="utf-8", **kwargs)
        return ret


def post(url,data=None,headers=headers,code="utf-8",**kwargs):
    try:
        res=requests.get(url,data=data,headers=headers,**kwargs)
        if res.status_code in [200,201,301]:
                return res.content.decode(code)
        else:
            time.sleep(random.randint(1,5))
            ret=get(url,data=None,headers=headers,code="utf-8",**kwargs)
            return ret
    except ConnectionError:
        time.sleep(random.randint(1, 5))
        ret = get(url, params=None, headers=headers, code="utf-8", **kwargs)
        return ret