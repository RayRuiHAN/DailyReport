# -*- coding: utf-8 -*-
from selenium import webdriver
import smtplib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText  # 引入smtplib和MIMEText
from time import sleep
import time
import urllib3
from requests import exceptions
from tenacity import retry, retry_if_exception_type, stop_after_attempt

# 声明谷歌、Firefox、Safari等浏览器
driver = webdriver.Chrome()

driver.implicitly_wait(15)
time.sleep(3)


def health_report(stuid, stukey, ifvpn):
    @retry(
        retry=retry_if_exception_type(exceptions.Timeout),
        stop=stop_after_attempt(5)
    )
    # 登陆VPN
    def do_retry():
        driver.get("https://webvpn.xmu.edu.cn/login")

    if ifvpn:
        do_retry()
        sleep(2)
        # print(driver.page_source)
        driver.find_element(By.XPATH, '//*[@id="local"]').click()
        driver.find_element(By.XPATH, '//*[@id="user_name"]').send_keys(stuid)
        driver.find_element(By.XPATH, '//*[@id="form"]/div[3]/div/input').send_keys(stukey)
        driver.find_element(By.XPATH, '//*[@id="form"]/div[3]/div/input').send_keys(Keys.ENTER)
        time.sleep(2)
        driver.refresh()
        time.sleep(2)

    # 登录事务大厅
    def do0_retry():
        driver.get(
            "https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu")

    def do1_retry():
        driver.get(
            "https://webvpn.xmu.edu.cn/https/77726476706e69737468656265737421f9f352d23f3d7d1e7b0c9ce29b5b/authserver"
            "/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu")

    if ifvpn:
        do1_retry()
    else:
        do0_retry()

    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(stuid)

    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(stukey)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(Keys.ENTER)
    time.sleep(2)

    # 登录健康打卡
    def do00_retry():
        driver.get(
            "https://xmuxg.xmu.edu.cn/app/214")

    def do11_retry():
        driver.get(
            "https://webvpn.xmu.edu.cn/https/77726476706e69737468656265737421e8fa5484207e705d6b468ca88d1b203b/app/214")

    if ifvpn:
        do11_retry()
    else:
        do00_retry()
    time.sleep(2)
    driver.refresh()
    time.sleep(5)

    # 获取我的表单
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()
    time.sleep(2)

    # 下拉菜单为是
    driver.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li/label').click()
    time.sleep(1)

    # 保存按钮
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/span/span').click()
    time.sleep(1)

    # 确认保存弹窗
    a = driver.switch_to.alert  # 新方法，切换alert
    print(a.text)  # 获取弹窗上的文本
    a.accept()  # 确认，相当于点击[确定]按钮
    time.sleep(1)
    driver.quit()


def self_email(host, port, sender, pwd):
    # host: 发件服务器地址
    # port: 发件服务器端口, 一般是456
    # sender: 发件邮箱
    # pwd: 发件邮箱第三方授权码
    receiver = sender  # 设置邮件接收人为自己
    http = urllib3.PoolManager()  # 创建PoolManager对象生成请求
    response = http.request('GET', 'http://v4.ipv6-test.com/api/myip.php')  # get方式请求
    nowip = response.data.decode('utf-8')
    body = 'AutoMSG From Ray ' + nowip  # 设置邮件正文,这里是支持HTML的
    msg = MIMEText(body, "plain", 'utf-8')  # 设置正文为UTF8
    msg['subject'] = 'DailyReport Complete'  # 设置邮件标题
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())
        # 发送邮件！
        print('Done.sent email success')
    except smtplib.SMTPException:
        print('Error.sent email fail')


if __name__ == '__main__':
    # health_report(学号, 密码)
    health_report('15220182202416', 'Wxf665789', ifvpn=0)
    sleep(1)
    # self_email(发件服务器地址,发件服务器端口,发件邮箱,发件邮箱第三方授权码)
    self_email('smtp.qq.com', '465', '992353539@qq.com', 'vissmgnejpfsbfid')

'''    # 地址省市县
    driver.find_element_by_xpath('//*[@id="address_1582538163410"]/div/div[1]/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div[2]/div[3]/li[28]/label').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="address_1582538163410"]/div/div[2]/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li[2]/label').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="address_1582538163410"]/div/div[3]/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/ul/div/li[1]/label').click()
    time.sleep(1)

    # 在校
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[14]/div/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li[1]/label').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[17]/div/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li[1]/label/span[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[18]/div/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li[1]/label/span[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[20]/div/div/div').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[8]/ul/div[2]/div[3]/li[82]/label').click()
    time.sleep(1)
    dom='0408'
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[4]/div/div[21]/div[1]/input').send_keys(dom)
    time.sleep(1)
'''
