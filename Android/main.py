from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# 測試手機相關資訊
devices_dict = {
    "platformName": "Android",
    "appium:platformVersion": "11",
    "appium:deviceName": "emulator-5554",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.android.chrome",
    "appium:appActivity": "com.google.android.apps.chrome.Main",
    "appium:noReset": False,
}

br = webdriver.Remote('http://localhost:4723', devices_dict)

# init
page = True
product_msg = ''
product_price = ''

try:
    # 接受並繼續
    agree_btn = WebDriverWait(br, 10, 1).until(EC.visibility_of_element_located(
        (By.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/terms_accept']")))
    agree_btn.click()

    # 不開啟同步
    no_btn = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/negative_button']")))
    no_btn.click()

    # 搜尋pchome
    input_btn = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.EditText[@resource-id='com.android.chrome:id/search_box_text']")))
    input_btn.send_keys("pchome")
    br.press_keycode(66)
    time.sleep(1)

    # 點擊第一筆關聯
    first_search = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[@resource-id='rso']/android.view.View[1]")))
    first_search.click()

    # 首次會有要求通知
    accept_btn = WebDriverWait(br, 10, 1).until(EC.visibility_of_element_located(
        (By.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/positive_button']")))
    accept_btn.click()

    handle = br.contexts
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

    # 切換至native
    br.switch_to.context(handle[0])

    check = WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
        (By.XPATH, "//android.view.View[@resource-id='BlockHeader']/android.view.View")))

    if "PChome" not in check.text:
        print("Fail: 頁面異常")
        print(check.text)
        page = False
except:
    print("FaiL: 開啟PChome頁面失敗")
    page = False

# 頁面正常在往下
if page:
    try:
        # 搜尋商品
        WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//android.widget.EditText[@resource-id='Keyword']"))).click()
        search = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//android.widget.EditText[@resource-id='SearchKeyword']")))
        search.send_keys("Final Fantasy XVI")
        WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "//android.view.View[@resource-id='btnDoSearch']"))).click()
        time.sleep(1)

        screen = WebDriverWait(br, 10, 1).until(EC.visibility_of_element_located(
            (By.XPATH, "//android.view.View[@resource-id='WRAPPER']/..")))
        x1 = screen.size['width'] * 0.5
        y1 = screen.size['height'] * 0.75
        y2 = screen.size['height'] * 0.45

        # 最多往上滑動兩次
        count = 0
        while count < 2:
            try:
                # 點擊一般版
                product = WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[contains(@content-desc, '一般版')]")))
                price = WebDriverWait(br, 10, 1).until(EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[contains(@content-desc, '一般版')]/following-sibling::android.widget.ListView/android.view.View")))

                if product.is_displayed() and price.is_displayed():
                    product_msg = product.get_attribute('content-desc')
                    product_price = price.text
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
            screen = WebDriverWait(br, 10, 1).until(EC.visibility_of_element_located(
                (By.XPATH, "//android.view.View[@resource-id='ProdContainer']/..")))
            x1 = screen.size['width'] * 0.5
            y1 = screen.size['height'] * 0.75
            y2 = screen.size['height'] * 0.55
            br.swipe(x1, y1, x1, y2)
            time.sleep(1)

            product_page = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
                (By.XPATH, "//android.view.View[@resource-id='ProdNick']")))
            product_page_price = WebDriverWait(br, 10, 1).until(EC.element_to_be_clickable(
                (By.XPATH, "//android.widget.TextView[@text='$']/following-sibling::android.widget.TextView")))
            if (product_msg not in product_page.text) or (product_page_price.text not in product_price):
                print("Fail: 商品連結顯示異常")
                print(f"搜尋頁商品名稱: {product_msg}")
                print(f"搜尋頁商品價錢: {product_price}")
                print(f"商品頁面標題: {product_page.text}")
                print(f"商品頁面價錢: {product_page_price.text}")

    except:
        print("Fail: 判斷商品失敗")

br.quit()
