    
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os
from .models import MainappBrand, MainappOrder, MainappChannel, MainappBrandBranch ,MainappOrderItem, MainappStatus, MainappItem, MainappAddOns,MainappOrderItemAddOns
import dateutil.parser
from datetime import datetime, timedelta
from django.conf import settings 
from .utils import *



def login():  
    email  = "a.shehadeh@kitchefy.com"
    password  = "Admin123"

    options = Options()
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)

    global driver
    driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH,chrome_options=options)
    driver.maximize_window()
    global wait
    wait = WebDriverWait(driver, 30)
    global channel
    channel = MainappChannel.objects.get(name='makane')
    driver.get("https://dashboard.makane.com/admin/login")
    wait.until(EC.presence_of_element_located((By.ID,"email")))
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME,"btn-primary").click()

    time.sleep(6)

    driver.get("https://dashboard.makane.com/admin/resources/orders?orders_filter=W3siY2xhc3MiOiJBcHBcXE5vdmFcXEZpbHRlcnNcXE9yZGVyc0NhbGxDZW50ZXIiLCJ2YWx1ZSI6MjI2OTV9XQ%3D%3D")

def get_items(order):

    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='flex border-b border-dotted border-60 py-2']")))
    list_of_items = driver.find_element(By.CLASS_NAME , "text-lg")
    iteems = list_of_items.find_elements(By.CLASS_NAME, "border-dotted")
    for item in iteems[:-1]:        
        data = item.text.split("\n")
        price = data[-1].replace(" JOD","")
        name = data[0].split("x ")[1]
        quantity = data[0].split("x ")[0]

        item_ , _ = MainappItem.objects.get_or_create(name=name)
        order_item = MainappOrderItem.objects.create(item = item_ , order=order, quantity=quantity,price=price)
        if data[2].startswith("Add On"):

            name = data[2].replace("Add On","").replace(":","").strip()
            price = data[3].replace("(","").replace(") JOD","")
            add_ons , _ = MainappAddOns.objects.get_or_create(name=name)
            if name != "":
                order_item_add_ons , _ = MainappOrderItemAddOns.objects.get_or_create(quantity=0,price=price,order_item=order_item, add_ons=add_ons)
               

def get_order_details(order_link,order_id):
    driver.execute_script('window.open("{}")'.format(order_link))
    driver.switch_to.window(driver.window_handles[1])
    wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='card mb-6 py-3 px-6']")))
    time.sleep(5)
    try:
        driver.find_element(By.XPATH,"//*[text()='OK']").click()
    except:pass

    order_info =driver.find_element(By.XPATH,"//*[@class='card mb-6 py-3 px-6']").text.split("\n")
    order , _ = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)

    date_time = datetime.strptime(order_info[1], '%Y-%m-%d %I:%M:%S %p')
    order.date_time = date_time
    order.customer_name = order_info[3]
    order.total = order_info[7].replace(" JOD", "")
    order.type = order_info[9]
    status = order_info[12]
    if status == "Canceled":
        order.status = "Cancelled"
    elif status =="Cancelled":
        order.status ="Cancelled"
    else:
        order.status = "Delivered"
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mb-1")))
    time.sleep(1)
    order.customer_mobile_number = driver.find_elements(By.CLASS_NAME, "mb-1")[1].text
    order.delivary_fee = driver.find_elements(By.CLASS_NAME, "text-right")[-1].text.replace(" JOD", "")
    order.delivery_zone = driver.find_elements(By.CLASS_NAME, "mb-1")[2].text 
    order.save()
    get_items(order)
    driver.close()

def get_orders():

    while 1 :
        time.sleep(10)
        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='cursor-pointer text-70 hover:text-primary mr-3 inline-flex items-center has-tooltip']")))
        orders = driver.find_elements(By.TAG_NAME , "tr")
        id_list = []
        link_list = []
        brands_list = []
        for count , order in enumerate(orders[1:]):
 
            id_list.append(order.find_elements(By.TAG_NAME,"td")[1].text.replace("R",""))
            link_list.append(order.find_elements(By.TAG_NAME,"td")[1].find_element(By.TAG_NAME,"a").get_attribute("href"))
            brands_list.append(order.find_elements(By.TAG_NAME,"td")[4].text)

        count = 0

        for i in range (len(id_list)):
            order , created  = MainappOrder.objects.get_or_create(channel=channel,order_id=id_list[i])
        
            if created != True:
                count+=1
            try:
                order.brand_branch = MainappBrandBranch.objects.filter(makane_name=brands_list[i]).first()
                order.save()
            except:
                
                print (channel.name,"can't find brand_branch name :",brands_list[i])
            
            if len(MainappOrderItem.objects.filter(order=order)) == 0:

                driver.switch_to.window(driver.window_handles[0])
                driver.window_handles[0]
                
                get_order_details(link_list[i],id_list[i])
        # if count > 10:
        #     break
        driver.window_handles[0]
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(1)



        driver.find_elements(By.XPATH, "//*[@class='btn btn-link py-3 px-4 text-primary dim']")[-1].click()

def start(start_date, end_date, start_timer):

    try:
        login()

        while 1:

            get_orders()
            last_update(channel)
            db.close_old_connections()

            end = datetime.now()
            timer = end - start_timer
            time.sleep(60*15)
            if timer.seconds > 3*60*60:
                driver.quit()
                print(timer.seconds)
                break
    except Exception as e:
        print(channel.name,e)   
        driver.quit()
        start(start_date, end_date, start_timer)


def start_makane(start_date,end_date,start_timer):

    start_timer = datetime.now()
    start(start_date,end_date,start_timer)
 