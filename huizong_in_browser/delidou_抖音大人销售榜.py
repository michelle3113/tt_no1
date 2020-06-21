from selenium import webdriver
import pandas as pd
import time

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://dy.delidou.com/login')

    # login
    browser.find_element_by_id('switch_login').click()
    # input account and passwd
    browser.find_element_by_id('txt-input').send_keys('shiyan')
    browser.find_element_by_id('pw-input').send_keys('shiyan')
    # click login
    browser.find_element_by_id('btnLogin').click()
    time.sleep(2)

    # select
    browser.find_element_by_xpath('/html/body/nav/ul/li[4]/a/span').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="sidebar"]/ul/li[4]/ul/li[10]/a').click()
    time.sleep(2)

    cols = ['排名',
            '姓名', '性别', '地区', '分类', '达人指数',
            '粉丝总量', '作品总数', '点赞总数', '平均点赞', '平均评论', '平均转发',
            '粉丝增量(w)', '视频数', '新增直播数', '点赞增量(w)', '评论增量', '转发增量',
            '观看总人数(w)', '峰值人数(w)', '送礼UV(w)', '新增关注数(w)', '新增粉丝团(w)',
            '商品数', '销售额(w)', '销量(w)', '音浪收入(w)', '总佣金(w)']
    tt = pd.DataFrame(columns=[''])
    # start collection
    browser.find_element_by_xpath('//*[@id="sku_seller_rank"]/tr[1]/td[2]/div/div[2]/div[1]/a')
    browser.find_element_by_xpath('//*[@id="sku_seller_rank"]/tr[2]/td[2]/div/div[2]/div[1]/a')
    browser.find_element_by_xpath('//*[@id="sku_seller_rank"]/tr[3]/td[2]/div/div[2]/div[1]/a')
    browser.find_element_by_xpath('//*[@id="sku_seller_rank"]/tr[50]/td[2]/div/div[2]/div[1]/a')
    browser.find_element_by_xpath('')
    browser.find_element_by_xpath('')
