from selenium import webdriver
import time

driver = webdriver.Chrome()  # PhantomJs
driver.get("https://www.google.com/")
time.sleep(1)
driver.find_element_by_id("lst-ib").click()
time.sleep(1)
driver.find_element_by_id("lst-ib").clear()
driver.find_element_by_id("lst-ib").send_keys(u"咖啡廳")
time.sleep(1)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='登入'])[1]/following::div[6]").click()
time.sleep(3)
driver.find_element_by_name("btnK").click()
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[@class='yyjhs'])[1]/following::div[4]").click()
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
time.sleep(1)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='排序依據：'])[1]/following::span[1]").click()
time.sleep(1)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='最新'])[1]/following::div[1]").click()
time.sleep(1)
driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='-'])[18]/following::span[1]").click()
pageSource = driver.page_source  # 取得網頁原始碼
print(pageSource)

# driver.close()  # 關閉瀏覽器