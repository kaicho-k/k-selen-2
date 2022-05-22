from selenium import webdriver
from selenium.webdriver.chrome import service as fs
import time
from discordwebhook import Discord
import os
from aa import key

import shutil
import stat
from pathlib import Path
#========================================================================
global driver


def add_execute_permission(path: Path, target: str = "u"):
    """Add `x` (`execute`) permission to specified targets."""
    mode_map = {
        "u": stat.S_IXUSR,
        "g": stat.S_IXGRP,
        "o": stat.S_IXOTH,
        "a": stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    }

    mode = path.stat().st_mode
    for t in target:
        mode |= mode_map[t]

    path.chmod(mode)


#def settingDriver():
def kakaku_check(event,context):
    print("driver setting")
    global driver

    driverPath = "/tmp" + "/chromedriver" #"/tmp" + "/chromedriver"
    headlessPath = "/tmp" + "/headless-chromium" #"/tmp" + "/headless-chromium"

    # copy and change permission
    print("copy headless-chromium")
    shutil.copyfile(os.getcwd() + "/headless-chromium", headlessPath)
    add_execute_permission(Path(headlessPath), "ug")

    print("copy chromedriver")
    shutil.copyfile(os.getcwd() + "/chromedriver", driverPath)
    add_execute_permission(Path(driverPath), "ug")

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')

    #https://teratail.com/questions/238003
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--start-maximized')
    

    chrome_options.binary_location = headlessPath

    print("get driver")
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=chrome_options)


#========================================================================
#def kakaku_check(event,context):

    #global driverPath
    #global headlessPath
    #global chrome_options

    discord = Discord(url=key)
    driver = webdriver.Chrome(executable_path=driverPath, options=chrome_options)
    driver.get('https://kakaku.com/item/K0001362645/?lid=20190108pricemenu_hot');
    time.sleep(1.5) # Let the user actually see something!

    price_list = []
    shopname_list = []
    stock_list = []
    shoplink_list = []


    #前週比
    while True:
        try:
            previous_price = driver.find_element_by_class_name('priceUp').text
            print(previous_price)
        except:
            previous_price = driver.find_element_by_class_name('priceDown').text
            print(previous_price)
            break

    #価格
    for prices in driver.find_elements_by_css_selector(' td.p-priceTable_col.p-priceTable_col-priceBG > div'):
        price = prices.find_element_by_class_name('p-PTPrice_price').text
        price_list.append(str(price))

    #ショップ名
    for shops in driver.find_elements_by_class_name('p-PTShopData_name'):
        shop_name = shops.find_element_by_class_name('p-PTShopData_name_link').text
        shopname_list.append(shop_name)

    #ショップリンク
    shop_links = driver.find_elements_by_css_selector(' td.p-priceTable_col.p-priceTable_col-shopInfo > div.p-PTShop > div.p-PTShop_btn > a')
    print(shop_links)
    for shop_link in shop_links:
        link = shop_link.get_attribute('href')
        shoplink_list.append(link)

    for i in range(len(price_list)):
        if int(price_list[i].replace('¥','')) <= int(77000):
            #print(shopname_list[i] + '\n' + price_list[i] +'\n'+ shoplink_list[i])
            discord.post(content=shopname_list[i] + '\n' + price_list[i] +'\n'+ shoplink_list[i])
    time.sleep(2)
    driver.close()

