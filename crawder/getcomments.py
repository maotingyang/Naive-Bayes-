from selenium import webdriver
import time

driver = webdriver.Chrome()  # PhantomJs
driver.get(r"https://www.google.com.tw/search?rlz=1C1PRFI_enTW779TW779&ei=HmDgW_POKY_q8wXY0ZzIDQ&q=google%E5%92%96%E5%95%A1%E5%BB%B3&oq=google%E5%92%96%E5%95%A1%E5%BB%B3&gs_l=psy-ab.3...1743.4918.0.5193.13.13.0.0.0.0.125.771.12j1.13.0....0...1c.1j4.64.psy-ab..1.4.232...0j0i131i67k1j0i131k1j0i67k1.0.bwQQP0ZGd-c&npsic=0&rflfq=1&rlha=0&rllag=25026734,121523497,250&tbm=lcl&rldimm=16148179717813685624&lqi=Cg9nb29nbGXlkpbllaHlu7MiA4gBAVoTChFnb29nbGUg5ZKW5ZWhIOW7sw&ved=2ahUKEwiJxuqgx73eAhVGErwKHbrUAokQvS4wC3oECAIQHA&rldoc=1&tbs=lrf:!2m4!1e17!4m2!17m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:4#rldoc=1&rlfi=hd:;si:16148179717813685624,l,Cg9nb29nbGXlkpbllaHlu7MiA4gBAVoTChFnb29nbGUg5ZKW5ZWhIOW7sw;mv:!3m12!1m3!1d2974.995991089583!2d121.52441559999998!3d25.027791399999998!2m3!1f0!2f0!3f0!3m2!1i324!2i158!4f13.1")
time.sleep(4)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
time.sleep(2)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='無法新增這個檔案，請確認這張相片是有效的檔案。'])[4]/following::div[20]").click()
time.sleep(2)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='規劃路線'])[1]/following::div[2]").click()
time.sleep(2)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='儲存'])[1]/following::span[6]").click()
time.sleep(2)
driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='無法新增這個檔案，請確認這張相片是有效的檔案。'])[4]/following::div[20]").click()