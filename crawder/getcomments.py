from selenium import webdriver
import time

driver = webdriver.Chrome()  # 或PhantomJs瀏覽器，沒試過
driver.get(r"https://www.google.com.tw/search?hl=zh-TW&source=hp&ei=HefgW7WCOcL7wAO6zrHgCw&q=%E5%92%96%E5%95%A1%E5%BB%B3&oq=%E5%92%96%E5%95%A1%E5%BB%B3&gs_l=psy-ab.3..0l10.1744.2569.0.2874.8.7.0.1.1.0.82.411.7.7.0....0...1c.1j4.64.psy-ab..0.7.370...0i131k1.0.ogkoAELBfr4&npsic=0&rflfq=1&rlha=0&rllag=25035347,121541542,339&tbm=lcl&rldimm=16984361819133688285&ved=2ahUKEwjwiP31x77eAhUaZt4KHT3aAysQvS4wAHoECAEQIQ&rldoc=1&tbs=lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9#rlfi=hd:;si:16984361819133688285;mv:!3m12!1m3!1d4857.541479453436!2d121.53968619999999!3d25.036968849999997!2m3!1f0!2f0!3f0!3m2!1i282!2i258!4f13.1;tbs:lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:9")
time.sleep(5)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='关闭'])[1]").click()
time.sleep(2)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='仁愛路三段92號'])[1]/preceding::div[3]").click()
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='關閉'])[1]/following::div[4]").click()

# driver.close()  # 關閉瀏覽器