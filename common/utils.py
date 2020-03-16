from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_cookie(url,selector,key1="FSSBBIl1UgzbN7N80S",key2="FSSBBIl1UgzbN7N80T"):
    profile = webdriver.FirefoxOptions()
    profile.add_argument('-headless')  # 设置无头模式
    driver=webdriver.Firefox(options=profile)
    driver.get(url)
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
    a=driver.get_cookie(key1)
    b=driver.get_cookie(key2)
    cookies={key1:a["value"],key2:b["value"]}
    driver.quit()
    return cookies