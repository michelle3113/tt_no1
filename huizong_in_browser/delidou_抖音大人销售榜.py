from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://dy.delidou.com/login')
    browser.implicitly_wait(20)
    # browser.execute_script("document.body.style.zoom='0.5'")

    # login
    # browser.find_element_by_id('switch_login').click()
    browser.execute_script("document.getElementById('switch_login').click()")
    # input account and passwd
    browser.find_element_by_id('txt-input').send_keys('shiyan')
    browser.find_element_by_id('pw-input').send_keys('shiyan')
    # click login
    # browser.find_element_by_id('btnLogin').click()
    browser.execute_script("document.getElementById('btnLogin').click()")
    browser.implicitly_wait(7)
    browser.execute_script("document.body.style.zoom='0.5'")
    # time.sleep(2)

    # select
    # e = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/nav/ul/li[4]/a/span")))
    # e.click()
    # e = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]/ul/li[4]/ul/li[10]/a')))
    # e.click()
    # browser.find_element_by_xpath('/html/body/nav/ul/li[4]/a/span').click()
    # browser.find_element_by_link_text('抖音电商').click()
    browser.execute_script("$('#sidebar > ul > li:nth-child(4) > a > span').click()")
    browser.implicitly_wait(7)
    # time.sleep(2)
    browser.find_element_by_xpath('//*[@id="sidebar"]/ul/li[4]/ul/li[10]/a').click()
    # time.sleep(2)
    main_handle = browser.current_window_handle
    print(main_handle)

    cols = ['排名',
            '姓名', '性别', '地区', '分类', '达人指数',
            '粉丝总量', '作品总数', '点赞总数', '平均点赞', '平均评论', '平均转发',
            '粉丝增量(w)', '视频数', '新增直播数', '点赞增量(w)', '评论增量(w)', '转发增量(w)',
            '观看总人数(w)', '峰值人数(w)', '送礼UV(w)', '新增关注数(w)', '新增粉丝团(w)',
            '商品数', '销售额(w)', '销量(w)', '音浪收入(w)', '总佣金(w)']
    tt = pd.DataFrame(columns=cols)
    # start collection
    for idx in range(5):
        browser.find_element_by_xpath(f'//*[@id="sku_seller_rank"]/tr[{idx + 1}]/td[2]/div/div[2]/div[1]/a').click()
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(20)

        cur = {}
        # 基本信息
        cur['排名'] = idx + 1
        cur['姓名'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dt').text.split('\n')[0]
        print(cur['姓名'])
        cur['性别'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[2]').text.split('：')[1]
        cur['地区'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[3]/span').text.split(
            '：')[1]
        cur['分类'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[4]/span').text

        cur['达人指数'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[2]/div[3]').text
        cur['粉丝总量'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[1]/p[2]').text
        cur['作品总数'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[2]/p[2]').text
        cur['点赞总数'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[3]/p[2]').text
        cur['平均点赞'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[4]/p[2]').text
        cur['平均评论'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[5]/p[2]').text
        cur['平均转发'] = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[6]/p[2]').text

        # click 30 days
        browser.find_element_by_xpath('//*[@id="userdata_overview_btn"]/button[2]').click()
        # browser.implicitly_wait(20)

        cur['粉丝增量(w)'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[1]/div/span[2]/b').text
        cur['视频数'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[2]/div/span[2]/b').text
        cur['新增直播数'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[3]/div/span[2]/b').text
        cur['点赞增量(w)'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[4]/div/span[2]/b').text
        cur['评论增量(w)'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[5]/div/span[2]/b').text
        cur['转发增量(w)'] = browser.find_element_by_xpath(
            '//*[@id="userdata_overview"]/div/div[6]/div/span[2]/b').text

        # click zhibojilu  click 30 days
        browser.find_element_by_xpath('//*[@id="tab_menu"]/li[6]').click()
        browser.implicitly_wait(7)
        # time.sleep(2)
        browser.find_element_by_link_text('直播记录').click()
        # browser.find_element_by_xpath('//*[@id="webcastdata_overview_btn"]/button[2]').click()
        # browser.implicitly_wait(7)

        cur['观看总人数(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[1]/div[1]/p[2]').text
        cur['峰值人数(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[1]/div[2]/p[2]').text
        cur['送礼UV(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[1]/div[3]/p[2]').text
        cur['新增关注数(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[1]/div[4]/p[2]').text
        cur['新增粉丝团(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[1]/div[5]/p[2]').text
        cur['商品数'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[2]/div[1]/p[2]').text
        cur['销售额(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[2]/div[2]/p[2]').text
        cur['销量(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[2]/div[3]/p[2]').text
        cur['音浪收入(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[2]/div[4]/p[2]').text
        cur['总佣金(w)'] = browser.find_element_by_xpath(
            '//*[@id="webcastdata_overview"]/div[2]/div[5]/p[2]').text

        tt.append(pd.DataFrame(cur), ignore_index=True)
        browser.close()
        browser.switch_to.window(main_handle)
    tt.to_excel('shifu.xlsx')
