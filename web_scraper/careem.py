from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .models import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import dateutil.parser
import csv
import smtplib
import time
import imaplib
import email
import traceback
from pynput.keyboard import Key, Controller
import glob
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest
import re
from django.conf import settings 


def login():
    email  = "Mickeysowner@careemnow.com"
    password  = "steakaway.owner"

    options = Options()
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.ignore_protected_mode_settings = True
    global driver
    driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH,chrome_options=options)
    global wait
    wait = WebDriverWait(driver, 60)
    global channel
    channel = MainappChannel.objects.get(name='Careem')

    driver.maximize_window()

    driver.get("https://app.careemnow.com/auth/login")
    wait.until(EC.presence_of_element_located((By.ID,"email")))
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()
    wait.until(EC.presence_of_element_located((By.ID,"password")))
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//*[text()='Log In']").click()
    driver.execute_script('window.open("https://app.careemnow.com/merchant/operating-status")')
    driver.execute_script('window.open("https://app.careemnow.com/merchant/past-orders")')

def  request_data(start_date,end_date):
    driver.switch_to.window(driver.window_handles[0])
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"AdvancedSearchDrawer_advancedSearchButton__1UWFe")))
    driver.find_element(By.CLASS_NAME, "AdvancedSearchDrawer_advancedSearchButton__1UWFe").click()
    wait.until(EC.element_to_be_clickable((By.ID,"date_range")))


    inputs = driver.find_elements(By.CLASS_NAME,"ant-picker-input")
    inputs[0].find_element(By.TAG_NAME,"input").send_keys(str(start_date))
    inputs[1].find_element(By.TAG_NAME,"input").send_keys(str(end_date))

    from selenium.webdriver.common.action_chains import ActionChains

    anyway = driver.find_element(By.CLASS_NAME,"ant-badge")
    ActionChains(driver).move_to_element(anyway).click().perform()
    time.sleep(5)
    driver.find_element(By.CLASS_NAME,"Button_primaryButton__3CeEz").click()
    user_email= "mohammad.y.qudah@gmail.com"

    driver.find_element(By.CLASS_NAME, "Button_mediumButton__1uk9d").click()
    time.sleep(1)
    driver.find_element(By.ID, "user_email").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "user_email").send_keys(Keys.DELETE)

    driver.find_element(By.ID, "user_email").send_keys(user_email)
    driver.find_element(By.XPATH, "//*[text()='Confirm']").click()

def get_link_from_email():

    FROM_EMAIL = "mohammad.y.qudah@gmail.com" 
    FROM_PWD = "wdfxyfcropeovwfs" 
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993

    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    # email_subject = msg['subject']
                    email_from = msg['from']
                    link = str(msg).split("href=\"")[1].split("\">here")[0]
                    return link
                                        
    except Exception as e:
        traceback.print_exc() 
        print(channel.name,str(e))

def download_file(link):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH,chrome_options=options)
    driver.get(link)
    time.sleep(10)
    driver.quit()

def read_csv_file():    
    list_of_files = os.listdir(r'C:\Users\mohm1\Downloads') #list of files in the current directory
    for each_file in list_of_files:
        if each_file.startswith('soa'):  #since its all type str you can simply use startswith
            file_name ="C:\\Users\\mohm1\\Downloads\\"+ each_file
            file = open(file_name)
            csvreader = csv.reader(file)
            header = []
            header = next(csvreader)
            rows = []
            for row in csvreader:
                    rows.append(row)
                    save_data(row)
            file.close()
            if(os.path.exists(file_name) and os.path.isfile(file_name)):
                os.remove(file_name)
                print("file deleted")
            else:
                pass
                print("file not found")
            break

         
def get_order_details(start_date,end_date):
    driver.switch_to.window(driver.window_handles[1])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ant-table-row-level-0")))
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"AdvancedSearchDrawer_advancedSearchButton__1UWFe")))
    driver.find_element(By.CLASS_NAME, "AdvancedSearchDrawer_advancedSearchButton__1UWFe").click()
    wait.until(EC.element_to_be_clickable((By.ID,"date_range")))
    time.sleep(5)


    inputs = driver.find_elements(By.CLASS_NAME,"ant-picker-input")
    inputs[0].find_element(By.TAG_NAME,"input").send_keys(str(start_date))
    inputs[1].find_element(By.TAG_NAME,"input").send_keys(str(end_date))

    from selenium.webdriver.common.action_chains import ActionChains

    anyway = driver.find_element(By.CLASS_NAME,"ant-badge")
    ActionChains(driver).move_to_element(anyway).click().perform()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME,"Button_primaryButton__3CeEz").click()
    element = driver.find_element(By.CLASS_NAME,"ContentContainer_content__1yGKP")  
    while 1:
        time.sleep(7)
        
        order_list = driver.find_elements(By.CLASS_NAME, "ant-table-row-level-0")
        for order in order_list:
                order_id = order.find_element(By.CLASS_NAME, "ant-table-cell").text 
                order_id = order_id.replace("ID:", "")
                order_, created  = get_or_create_order(order_id)

                if len(MainappOrderItem.objects.filter(order=order_)) == 0:
                    
                    
                    order.click()
                    save_order_data(driver,order_id)
                    driver.find_element(By.CLASS_NAME, "Button_mediumWideButton__3LOil").click()
                    driver.execute_script("arguments[0].scrollBy(0, 70)", element)
        next_page = driver.find_elements(By.CLASS_NAME, "Button_smallButton__GJDGm")[1]
        if  "Button_disabled__1f6YP" in next_page.get_attribute("class"): 
            break
        next_page.click()

def save_order_data(driver,order_id):
    order , created = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)
    promo_code  = soup = BeautifulSoup(driver.find_element(By.CLASS_NAME,"ant-modal-body").get_attribute("innerHTML"), "lxml")
    try:
        promo_code = promo_code.find(class_= "OrderSummary_promoCode__3J0Ey").text.split("JOD")[1]
        order.promo_code = promo_code
        order.save()
    except:pass
    items = driver.find_element(By.CLASS_NAME, "OrderItems_orderDetailsTable__2oSEV")
    html =items.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "lxml")

    items = soup.find_all("tr")
    for item in items:
        is_item = "OrderItems_tableHeader__ApUjD" in item["class"]
        if is_item == True:
            name = item.find("div", class_= "OrderItems_itemDetailsContent__1ufsO").find("div").text
            quantity= (item.text).split("x")[0]
            price =  (item.text).split("JOD ")[1]

            item_ , _ = MainappItem.objects.get_or_create(name=name)
            order_item , _ = MainappOrderItem.objects.get_or_create(item = item_ , order=order, quantity=quantity, price=price )

        is_add_ons = "OrderItems_optionItem__2gCHb" in item["class"]
        if is_add_ons == True:
            name = (item.text).split("- ")[1].split(" x ")[0]
            price = (item.text).split(" JOD ")[1]
            quantity = (item.text).split(" x ")[1].split("+ JOD")[0]

            add_ons , _ = MainappAddOns.objects.get_or_create(name=name)
            order_item_add_ons , _ = MainappOrderItemAddOns.objects.get_or_create(quantity=quantity,price=price,order_item=order_item, add_ons=add_ons)

def save_data(row):
    if row[5]== "delivered":
        status = "Delivered"
    else: status = "Cancelled"

    order , _ = MainappOrder.objects.get_or_create(channel=channel,order_id=row[0])
    order.status=status
    order.date_time=dateutil.parser.parse(row[26].replace("+03:00",""))
    order.total= row[12]
    order.delivery_zone=row[4]
    order.delivary_fee= row[14]
    order.pg_fees = row[8].replace("%","")
    order.gross_basket = row[12]
    print(row[12])
    print ("_____________________")
    # print (order,_)
    
    try:order.brand_branch = MainappBrandBranch.objects.get(careem_id=row[1])
    except:print (channel.name,"can't find careem id :",row[1])
    order.save()

def start(start_date,end_date,start_timer):
    # try:
        login()   
        while 1:
            # request_data(start_date,end_date)
            # time.sleep(60)
            link = get_link_from_email()
            download_file(link)
            read_csv_file()
            get_order_details(start_date,end_date)
            end = datetime.now()
            timer = end - start_timer
            time.sleep(60*15)
            if timer.seconds > 3*60*60:
                driver.quit()
                print(timer.seconds)
                break
    # except Exception as e:
    #     print(channel.name,e)   
    #     driver.quit()
    #     start(start_date, end_date, start_timer)





       
def start_careem(start_date,end_date,start_timer):
    start_timer = datetime.now()
    start(start_date,end_date,start_timer)

 














































def get_or_create_order(order_id):
    channel = MainappChannel.objects.get(name='Careem')
    order , created = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)
    return order, created 
def get_Status(driver):
    channel = MainappChannel.objects.get(name='Careem')
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(3)
    branches =driver.find_elements(By.TAG_NAME,"tr")[2:]

    for branch in branches:
        cells =branch.find_elements(By.TAG_NAME,"td")
        careem_name_status_tab =(cells[0].text +" "+cells[1].text+" "+cells[2].text).replace(" ", "_").lower()
        brand_branch = MainappBrandBranch.objects.filter(careem_name_status_tab=careem_name_status_tab).first()
        try:
            status, created = MainappStatus.objects.get_or_create(channel=channel,brand_branch=brand_branch)
            if cells[3].find_element(By.TAG_NAME,"button").get_attribute("aria-checked") == "true":
                status.status = "open"
            else:status.status = "close"
            status.save()

        except:pass
