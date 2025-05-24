from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# 測試手機相關資訊
devices_dict = {
    "platformName": "Android",
    "appium:platformVersion": "13",
    "appium:deviceName": "emulator-5554",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.android.chrome",
    "appium:appActivity": "com.google.android.apps.chrome.Main",
    "appium:noReset": False,
}

app_options = UiAutomator2Options().load_capabilities(devices_dict)
driver = webdriver.Remote('http://localhost:4723', options=app_options)

# init
wait = WebDriverWait(driver, 10, 1)
chrome_page = True
page = True

try:
    try:
        # 接受並繼續
        agree_btn = wait.until(EC.visibility_of_element_located(
            (AppiumBy.ID, "com.android.chrome:id/terms_accept")))
        agree_btn.click()
        time.sleep(1)

        # 不開啟同步
        no_btn = wait.until(EC.visibility_of_element_located(
            (AppiumBy.ID, "com.android.chrome:id/negative_button")))
        no_btn.click()
        time.sleep(1)
    except:
        no_acc = wait.until(EC.visibility_of_element_located(
            (AppiumBy.ID, "com.android.chrome:id/signin_fre_dismiss_button")))
        no_acc.click()
        time.sleep(1)

    # 關閉chrome操作體驗說明
    operate_alert = wait.until(EC.element_to_be_clickable(
        (AppiumBy.ID, "com.android.chrome:id/negative_button")))
    operate_alert.click()
except:
    print("Fail: 開啟chrome 失敗")
    chrome_page = False

if chrome_page:
    try:
        driver.get("https://dlg8888.com/")

        # 關閉最新公告
        wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//android.widget.TextView[@text='今日不再顯示']/preceding-sibling::android.widget.TextView")))
        time.sleep(1)

        # 關閉公告
        wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//android.widget.TextView[@text='最新公告']/preceding-sibling::android.widget.TextView"))).click()
        time.sleep(1)
    except:
        print("Fail: 開啟網頁失敗")
        page = False

    if page:
        try:
            # 預設切到電子
            button = "//android.widget.TextView[@text='電子']"
            wait.until(EC.element_to_be_clickable(
                (AppiumBy.XPATH, button))).click()
            time.sleep(2)

            # 稍微往上滑動來顯示遊戲
            driver.swipe(380, 1048, 380, 480, duration=1000)
            time.sleep(1)

            _xpath = f"//android.view.View[./android.view.View[.{button[1:]}]]/following-sibling::android.view.View[1]"

            # vendor xpath
            vendor_xpath = f"{_xpath}/android.view.View[1]"
            vendor_xpath = f"{vendor_xpath}//android.widget.TextView"

            # game xpath
            screen_xpath = f"{_xpath}/android.view.View[2]"
            game_xpath = f"{screen_xpath}//android.widget.TextView"

            vendor_name = ""
            vendor_list = wait.until(EC.presence_of_all_elements_located(
                (AppiumBy.XPATH, vendor_xpath)))
            for i in vendor_list:
                if i.text == "":
                    i.click()
                    time.sleep(1)
                    vendor_name = i.text
                else:
                    vendor_name = i.text

                game_name_list = []
                # 取得遊戲名稱
                game_ele_list = wait.until(EC.presence_of_all_elements_located(
                    (AppiumBy.XPATH, game_xpath)))
                for i in game_ele_list:
                    if i.text and i.text not in game_name_list:
                        game_name_list.append(i.text)

                # 取得遊戲展示框
                screen = wait.until(EC.visibility_of_element_located(
                    (AppiumBy.XPATH, screen_xpath)))
                x1 = screen.size['width']
                y1 = screen.size['height'] * 0.95
                y2 = screen.size['height'] * 0.05

                swipe_count = 0
                reached_bottom = False

                # 最大滑動10次
                while swipe_count < 10:
                    # 滑動前page
                    # 取最後一筆遊戲名稱
                    before_swipe = wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, game_xpath)))[-1].text

                    # 滑動頁面
                    driver.swipe(x1, y1, x1, y2, duration=2000)
                    time.sleep(1)
                    swipe_count += 1

                    try:
                        # 滑動後page
                        # 取最後一筆遊戲名稱
                        after_swipe = wait.until(EC.presence_of_all_elements_located(
                            (By.XPATH, game_xpath)))[-1].text
                    except:
                        # 如滑過頭需要往下拉
                        driver.swipe(380, 1580, 380, 1980, duration=1000)
                        time.sleep(1)
                        # 滑動後page
                        # 取最後一筆遊戲名稱
                        after_swipe = wait.until(EC.presence_of_all_elements_located(
                            (By.XPATH, game_xpath)))[-1].text

                    # 判斷是否到達底部
                    if before_swipe == after_swipe:
                        reached_bottom = True
                        break
                    else:
                        # 取得遊戲名稱
                        game_ele_list = wait.until(EC.presence_of_all_elements_located(
                            (AppiumBy.XPATH, game_xpath)))
                        for i in game_ele_list:
                            if i.text and i.text not in game_name_list:
                                game_name_list.append(i.text)

                if not reached_bottom:
                    print("Fail：超過滑動次數，還未到底部")

                print(f"遊戲商：{vendor_name}")
                print(f"遊戲清單：{game_name_list}")

        except:
            print("Fail: 取得遊戲清單失敗")

driver.quit()