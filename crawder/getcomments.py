from selenium import webdriver
import time

driver = webdriver.Chrome()  # PhantomJs
driver.get("https://www.google.com.tw/search?sa=X&q=%E5%92%96%E5%95%A1%E5%BB%B3")
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='下午11:00'])[1]/following::span[1]").click()
time.sleep(3)
# driver.find_element_by_class_name('rlfl__tls rl_tls r-ixkt1eZV9HQA').click()
driver.find_elements_by_css_selector("div.cXedhc")[5].click() # 餐廳關鍵字：cXedhc 評分關鍵字：Fam1ne EBe2gf
time.sleep(3)
# driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
# time.sleep(3)
# driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='仁愛路四段91巷23-1號'])[1]/preceding::div[3]").click()
# time.sleep(3)
# driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
# time.sleep(3)
# driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='關閉'])[1]/following::div[4]").click()
# driver.close()
print("The End")