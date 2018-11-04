from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome() 
driver.get(r"https://www.tripadvisor.com.tw/Search?q=%E5%92%96%E5%95%A1%E5%BB%B3&sid=2B33191C1E183F198CCC38239F06192C1541319676274&ssrc=a&geo=13811269&rf=1")
window_before = driver.window_handles[0]
time.sleep(3)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='咖啡廳'])[2]/following::span[1]").click()
time.sleep(3)
window_after = driver.window_handles[1]
driver.switch_to_window(window_after)
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(1)
driver.find_element_by_id('taplc_location_review_filter_controls_sur_0_filterRating_1').click()
time.sleep(1)

# soup = BeautifulSoup(driver.page_source, 'lxml')
# badComment = []
# for comment in soup.select('.partial_entry',limit=10):
#     print(comment.get_text())
#     badComment.append(comment.get_text())
# with open('../data/negative.txt', 'at', encoding='utf-8') as badtxt:
#     for comment in badComment:
#         print(comment, file=badtxt)

driver.find_element_by_id("taplc_location_review_filter_controls_sur_0_filterRating_1").click()
time.sleep(2)
driver.find_element_by_id("taplc_location_review_filter_controls_sur_0_filterRating_5").click()
time.sleep(2)
goodComment = []
for page in range(2,6):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for comment in soup.select('.partial_entry',limit=6):
        print(comment.get_text())
        goodComment.append(comment.get_text())
    driver.find_element_by_link_text(str(page)).click()
    time.sleep(3)
    print('=============================================')

with open('../data/positive.txt', 'at', encoding='utf-8') as goodtxt:
    for comment in goodComment:
        print(comment, file=goodtxt)

# driver.close()  # 關閉瀏覽器

