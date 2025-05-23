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
h5_page = True

try:
    # 接受並繼續
    agree_btn = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/terms_accept']")))
    agree_btn.click()

    # 不開啟同步
    no_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/negative_button']")))
    no_btn.click()

    # 關閉chrome操作體驗說明
    operate_alert = wait.until(EC.element_to_be_clickable(
        (AppiumBy.XPATH, "//android.widget.Button[@resource-id='com.android.chrome:id/negative_button']")))
    operate_alert.click()
except:
    print("Fail: 開啟chrome 失敗")
    chrome_page = False

if chrome_page:
    try:
        driver.get("https://h5.xin-stars.com/")

        # wait
        wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, "//android.widget.Button[@text='登入']/preceding-sibling::android.view.View")))

        # 勾選不在提示
        not_alert = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, "//android.widget.CheckBox[@text='下次不再提示']")))
        not_alert.click()
        time.sleep(1)
        is_checked = not_alert.get_attribute('checked')
        if is_checked != 'true':
            not_alert.click()
            time.sleep(1)

        # 點擊確定
        wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, "//android.widget.Button[@text='確定']"))).click()
        time.sleep(1)

        # 隱私權確認
        wait.until(EC.element_to_be_clickable(
            (AppiumBy.XPATH, "//android.widget.Button[@text='接受']"))).click()
        time.sleep(3)
    except:
        print("Fail: 開啟h5網頁失敗")
        h5_page = False

    if h5_page:
        try:
            live_all_button = wait.until(EC.visibility_of_element_located(
                (AppiumBy.XPATH, "//android.widget.TextView[@text='真人Live']/following-sibling::android.widget.Button[@text='探索全部']")))
            live_all_button.click()
            time.sleep(2)
            try:
                hot_slot = wait.until(EC.presence_of_element_located(
                    (AppiumBy.XPATH, "//android.widget.TextView[@text='熱門電子']")))
                if hot_slot:
                    live_all_button.click()
                    time.sleep(1)
            except:
                pass

            # 排序
            sort_text = wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, "//android.view.View[@text='排序依據']/following-sibling::android.widget.TextView"))).text

            game_name_list = []
            game_info_xpath = "//android.view.View[@resource-id='gameIndex']//android.widget.TextView[@text='info']"
            game_name_xpath = f"{game_info_xpath}/preceding-sibling::android.widget.TextView"

            # 取得遊戲展示框
            screen = wait.until(EC.visibility_of_element_located(
                (AppiumBy.XPATH, "//android.view.View[@resource-id='gameIndex']")))
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
                    (By.XPATH, game_name_xpath)))[-1].text

                # 滑動頁面
                driver.swipe(x1, y1, x1, y2, duration=2000)
                time.sleep(1)
                swipe_count += 1

                # 滑動後page
                # 取最後一筆遊戲名稱
                after_swipe = wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, game_name_xpath)))[-1].text

                # 判斷是否到達底部
                if before_swipe == after_swipe:
                    reached_bottom = True
                    break
                else:
                    # 取得遊戲名稱
                    game_ele_list = wait.until(EC.presence_of_all_elements_located(
                        (AppiumBy.XPATH, game_name_xpath)))
                    for i in game_ele_list:
                        if i.text and i.text not in game_name_list:
                            game_name_list.append(i.text)

            if not reached_bottom:
                print("Fail：超過滑動次數，還未到底部")

            print(sort_text, game_name_list)

        except:
            print("Fail: 取得遊戲清單失敗")

driver.quit()
