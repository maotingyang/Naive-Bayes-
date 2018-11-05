from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome() 
driver.get(r"https://www.tripadvisor.com.tw/Search?q=%E5%92%96%E5%95%A1&sid=37B87F3EAA43331583A4565120991E701541430260855&ssrc=e&geo=297908&rf=2")
window_before = driver.window_handles[0]   # 處理主頁
windowCounts = 1  # 視窗指標

for shop in range(1,10):    
    time.sleep(6)
    # 點進第一家餐廳
    try:
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='餐廳'])[" + str(shop) + "]/following::span[1]").click()  # 不按看更多只能查到第8家
    except:
        continue
    time.sleep(3)
    window_after = driver.window_handles[windowCounts]  # 第一個新視窗
    driver.switch_to_window(window_after)
    time.sleep(7)

    driver.find_element_by_id('taplc_location_review_filter_controls_0_filterRating_1').click()
    time.sleep(2)
    driver.find_element_by_id('taplc_location_review_filter_controls_0_filterRating_2').click()
    time.sleep(2)
    driver.find_element_by_id('taplc_location_review_filter_controls_0_filterRating_3').click()
    time.sleep(3)

    # 爬下負評
    badComment = []
    for page in range(2,7):   #預設抓一到五頁，一開始就在第一頁了
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for comment in soup.select('.partial_entry',limit=6):        
            print(comment.get_text())
            badComment.append(comment.get_text())
        try:
            driver.find_element_by_link_text(str(page)).click()
            time.sleep(3)
            print('=============================================')
        except:   # 如果頁數不足則終止爬取
            break    
    with open('../data/negative.txt', 'at', encoding='utf-8') as badtxt:
        for comment in badComment:
            print(comment, file=badtxt)

    driver.switch_to_window(window_before)
    driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='餐廳'])[" + str(shop) + "]/following::span[1]").click()
    time.sleep(3)
    windowCounts += 1
    window_third = driver.window_handles[windowCounts]  #第二個新視窗
    driver.switch_to_window(window_third)
    time.sleep(7)    
    driver.find_element_by_id("taplc_location_review_filter_controls_0_filterRating_1").click()
    time.sleep(2)
    driver.find_element_by_id('taplc_location_review_filter_controls_0_filterRating_2').click()
    time.sleep(2)
    driver.find_element_by_id("taplc_location_review_filter_controls_0_filterRating_3").click()
    time.sleep(2)
    driver.find_element_by_id("taplc_location_review_filter_controls_0_filterRating_4").click()
    time.sleep(2)
    driver.find_element_by_id("taplc_location_review_filter_controls_0_filterRating_5").click()
    time.sleep(2)
    # 爬下正評
    goodComment = []
    for page in range(2,7):
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for comment in soup.select('.partial_entry',limit=6):
            print(comment.get_text())
            goodComment.append(comment.get_text())
        try:
            driver.find_element_by_link_text(str(page)).click()
            time.sleep(3)
            print('=============================================')
        except:
            break
    with open('../data/positive.txt', 'at', encoding='utf-8') as goodtxt:
        for comment in goodComment:
            print(comment, file=goodtxt)
    driver.switch_to_window(window_before)
    windowCounts += 1
# driver.close()  # 關閉瀏覽器

print('=' * 50)
print('爬完了')

