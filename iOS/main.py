from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# 測試手機相關資訊
devices_dict = {
    "platformName": "IOS",
    "browserName": "safari",
    "appium:platformVersion": "16.0",
    "appium:deviceName": "iPhone 11",
    "appium:automationName": "XCUITest",
    "appium:udid": "CE9F012A-2901-4956-8917-218C163AD7FA",
    "appium:autoWebview": True,
    "appium:safariInitialUrl": "https://www.google.com",
}

br = webdriver.Remote('http://localhost:4723', devices_dict)
handle = br.contexts
# 切換至native
br.switch_to.context(handle[0])

# init
page = True
product_msg = ''
product_price = ''

try:
    # 搜尋pchome
    WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
        (By.XPATH, "//XCUIElementTypeTextField[@name='TabBarItemTitle']"))).click()

    search_input = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//XCUIElementTypeTextField[@name='URL']")))
    search_input.send_keys("pchome")
    br.hide_keyboard('Go')
    time.sleep(1)

    # 點擊第一筆關聯
    first_search = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//XCUIElementTypeOther[@name='廣告, 片段']//XCUIElementTypeLink")))
    first_search.click()

    # 切換至webview
    br.switch_to.context(handle[1])

    # 關閉上方的通知
    WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@class='sb-close']"))).click()

    try:
        # 關閉廣告
        WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='ui-btn b-close']"))).click()
    except:
        print("無顯示廣告")

    check = WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@id='BlockHeader']//a[@class='ico']")))

    if "PChome" not in check.get_attribute('title'):
        print("Fail: 頁面異常")
        print(check.get_attribute('title'))
        page = False
except:
    print("Fail: 開啟PChome頁面失敗")
    page = False

# 頁面正常在往下
if page:
    try:
        # 搜尋商品
        WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@id='icoSearch']"))).click()
        search = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='SearchKeyword']")))
        search.send_keys("Final Fantasy XVI")
        WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@id='btnDoSearch']"))).click()
        time.sleep(1)

        # 切換至native
        br.switch_to.context(handle[0])

        screen = br.get_window_size()
        x1 = screen['width'] * 0.5
        y1 = screen['height'] * 0.75
        y2 = screen['height'] * 0.55

        # 最多往上滑動兩次
        count = 0
        while count < 2:
            try:
                # 切換至native
                br.switch_to.context(handle[0])

                # 點擊一般版
                product = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
                    (By.XPATH, "//XCUIElementTypeLink[contains(@name, '一般版')]")))
                price = WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
                    (By.XPATH, "//XCUIElementTypeLink[contains(@name, '一般版')]/following-sibling::XCUIElementTypeOther//XCUIElementTypeStaticText[2]")))

                if product.is_displayed() and price.is_displayed():
                    product_msg = product.get_attribute('name')
                    product_price = price.get_attribute('name')
                    product.click()
                    time.sleep(1)
                    count = 2
                else:
                    count += 1
            except:
                if count == 2:
                    print("Fail: 找無相關商品")
                    product_msg = False
                else:
                    br.swipe(x1, y1, x1, y2)
                    count += 1
                    time.sleep(1)

        if product_msg and product_price:
            # 商品頁面上滑才可看到價錢
            screen = br.get_window_size()
            x1 = screen['width'] * 0.5
            y1 = screen['height'] * 0.65
            y2 = screen['height'] * 0.55
            br.swipe(x1, y1, x1, y2)
            time.sleep(1)

            product_page = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
                (By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'一般版')]")))
            product_page_price = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
                (By.XPATH, "//XCUIElementTypeStaticText[@name='$']/following-sibling::XCUIElementTypeStaticText")))
            if (product_msg not in product_page.get_attribute('name')) or (product_page_price.get_attribute('name') not in product_price):
                print("Fail: 商品連結顯示異常")
                print(f"搜尋頁商品名稱: {product_msg}")
                print(f"搜尋頁商品價錢: {product_price}")
                print(f"商品頁面標題: {product_page.text}")
                print(f"商品頁面價錢: {product_page_price.text}")

    except:
        print("Fail: 判斷商品失敗")

br.quit()
