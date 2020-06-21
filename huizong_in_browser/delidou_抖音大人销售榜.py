import os.path as osp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.set_window_size(2000, 2000)
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
    # browser.execute_script("document.getElementById('btnLogin').click()")
    browser.execute_script("$('#btnLogin').click()")
    browser.implicitly_wait(7)
    # browser.execute_script("document.body.style.zoom='0.5'")
    # time.sleep(2)

    # select
    # e = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "/html/body/nav/ul/li[4]/a/span")))
    # e.click()
    # e = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar"]/ul/li[4]/ul/li[10]/a')))
    # e.click()
    # browser.find_element_by_xpath('/html/body/nav/ul/li[4]/a/span').click()
    e = browser.find_element_by_link_text('抖音电商')
    e.click()
    e.send_keys(Keys.PAGE_DOWN)
    # browser.execute_script('document.querySelector("#sidebar > ul > li:nth-child(4)").click()')
    browser.implicitly_wait(7)
    # time.sleep(2)
    browser.find_element_by_xpath('//*[@id="sidebar"]/ul/li[4]/ul/li[10]/a').click()
    # browser.execute_script('document.querySelector("#sidebar > ul > li.submenu.open > ul > li:nth-child(9) > a").click()')

    # time.sleep(2)
    main_handle = browser.current_window_handle
    print(main_handle)

    tt = None
    last_time = 0
    if osp.exists('shifu.xlsx'):
        tt = pd.read_excel('shifu.xlsx')
        last_time = len(tt)
    # cols = ['排名',
    #         '姓名', '性别', '地区', '分类', '达人指数',
    #         '粉丝总量', '作品总数', '点赞总数', '平均点赞', '平均评论', '平均转发',
    #         '粉丝增量(w)', '视频数', '新增直播数', '点赞增量(w)', '评论增量(w)', '转发增量(w)',
    #         '观看总人数(w)', '峰值人数(w)', '送礼UV(w)', '新增关注数(w)', '新增粉丝团(w)',
    #         '商品数', '销售额(w)', '销量(w)', '音浪收入(w)', '总佣金(w)']
    # tt = pd.DataFrame(columns=cols)
    # start collection
    for idx in range(last_time, 50):
        browser.find_element_by_xpath(f'//*[@id="sku_seller_rank"]/tr[{idx + 1}]/td[2]/div/div[2]/div[1]/a').click()
        browser.switch_to.window(browser.window_handles[-1])
        browser.implicitly_wait(20)

        cur = {}
        # 基本信息
        cur['排名'] = idx + 1
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dt')))
            cur['姓名'] = element.text.split('\n')[0]
        except TimeoutException:
            break
        print(cur['排名'], cur['姓名'])

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[2]')))
            cur['性别'] = element.text.split('：')[1]
        except TimeoutException:
            break

        # try:
        #     element = WebDriverWait(browser, 10).until(
        #         EC.presence_of_element_located((By.XPATH, '')))
        #
        # except TimeoutException:
        #     break
        try:
            cur['地区'] = browser.find_element_by_xpath(
                '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[3]/span').text.split(
                '：')[1]
        except NoSuchElementException:
            cur['地区'] = ''

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/dl/dd[4]/span')))
            cur['分类'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[1]/div[2]/div[3]')))
            cur['达人指数'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[1]/p[2]')))
            cur['粉丝总量'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[2]/p[2]')))
            cur['作品总数'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[3]/p[2]')))
            cur['点赞总数'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[4]/p[2]')))
            cur['平均点赞'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[5]/p[2]')))
            cur['平均评论'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[6]/p[2]')))
            cur['平均转发'] = element.text
        except TimeoutException:
            break

        # browser.execute_script('window.scrollBy(0,500)')
        # e = browser.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div/div/div/div[2]/div[6]/p[1]/span[2]')
        # e.click()
        # click 30 days
        try:
            e = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview_btn"]/button[2]')))
        except TimeoutException:
            break
        e.click()
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.DOWN)
        browser.implicitly_wait(7)
        # browser.implicitly_wait(20)

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[1]/div/span[2]/b')))
            cur['粉丝增量(w)'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[2]/div/span[2]/b')))
            cur['视频数'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[3]/div/span[2]/b')))
            cur['新增直播数'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[4]/div/span[2]/b')))
            cur['点赞增量(w)'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[5]/div/span[2]/b')))
            cur['评论增量(w)'] = element.text
        except TimeoutException:
            break

        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userdata_overview"]/div/div[6]/div/span[2]/b')))
            cur['转发增量(w)'] = element.text
        except TimeoutException:
            break

        # init
        cur['观看总人数(w)'] = 0
        cur['峰值人数(w)'] = 0
        cur['送礼UV(w)'] = 0
        cur['新增关注数(w)'] = 0
        cur['新增粉丝团(w)'] = 0
        cur['商品数'] = 0
        cur['销售额(w)'] = 0
        cur['销量(w)'] = 0
        cur['音浪收入(w)'] = 0
        cur['总佣金(w)'] = 0

        ################
        if idx + 1 not in (19, 27, 37, 44, 46, 48, ):
            # click zhibojilu  click 30 days
            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="tab_menu"]/li[6]')))
                element.click()
            except TimeoutException:
                break
            browser.implicitly_wait(7)

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview_btn"]/button[2]')))
                element.click()
            except TimeoutException:
                break
            browser.implicitly_wait(7)

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[1]/div[1]/p[2]')))
                cur['观看总人数(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[1]/div[2]/p[2]')))
                cur['峰值人数(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[1]/div[3]/p[2]')))
                cur['送礼UV(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[1]/div[4]/p[2]')))
                cur['新增关注数(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[1]/div[5]/p[2]')))
                cur['新增粉丝团(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[2]/div[1]/p[2]')))
                cur['商品数'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[2]/div[2]/p[2]')))
                cur['销售额(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[2]/div[3]/p[2]')))
                cur['销量(w)'] = element.text

            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[2]/div[4]/p[2]')))
                cur['音浪收入(w)'] = element.text
            except TimeoutException:
                break

            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="webcastdata_overview"]/div[2]/div[5]/p[2]')))
                cur['总佣金(w)'] = element.text
            except TimeoutException:
                break

        cur = pd.DataFrame({k: [v] for k, v in cur.items()})
        if tt is None:
            tt = cur
        else:
            tt = tt.append(cur)
        browser.close()
        browser.switch_to.window(main_handle)
        # if idx % 2 == 0:
        tt.to_excel('shifu.xlsx', index=None)
    tt.to_excel('shifu.xlsx', index=None)
