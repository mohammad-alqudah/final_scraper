
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from .utils import *
from .models import MainappOrder, MainappChannel, MainappBrandBranch ,MainappOrderItem, MainappItem,MainappAddOns,MainappOrderItemAddOns
import dateutil.parser
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from django.conf import settings 
import os
import pandas as pd

def read_orders(driver,brand_branch,count):

    orders =driver.find_elements(By.TAG_NAME, "tr")

    for order in orders[1:]:
        csmena_id = (order.text).split(" ")[0].replace("#", "")
        creation_time =order.find_elements(By.TAG_NAME,"td")[3].text

        # Convert 12 hour time to 24 hour format
        creation_time = datetime.strptime(creation_time, '%I:%M:%S %p')
        hour = creation_time.hour
        minute = creation_time.minute
        second = creation_time.second

       

        # if not MainappOrder.objects.filter(date_time__hour=hour,date_time__minute=minute,date_time_second=second).exists():   # change to len order item          
        order.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"order-details-box")))
        order_details = driver.find_elements(By.CLASS_NAME, "order-details-box")[1].text

        status = order.find_element(By.CLASS_NAME, "label-info").text
        if status == "Finished":
            status="Delivered"
        else:             
            status="Cancelled"

        order_list = order_details.split("\n")
        Customer_Phone_index = order_list.index("Phone")
        customer_mobile_number =  "+962" + order_list[Customer_Phone_index+1][1:]
        try:
        # if 1==1:
            # print(channel,hour,minute,second,customer_mobile_number)
            order  = MainappOrder.objects.get(channel=channel,date_time__hour=hour,date_time__minute=minute,date_time__second=second,customer_mobile_number=customer_mobile_number)
            if len(MainappOrderItem.objects.filter(order=order)) == 0:

                order.status = status
                order.brand_branch = brand_branch       
                Customer_Name_index = order_list.index("Name")
                order.customer_name = order_list[Customer_Name_index+1]
                order.total = (driver.find_element(By.CLASS_NAME, "total-item").text).split("\n")[1].replace("JOD", "")
                order.delivary_fee = (driver.find_element(By.CLASS_NAME, "delivery-item").text).split("\n")[1].replace("JOD", "")
                Customer_Address_index = order_list.index("Address")
                order.delivery_zone = order_list[Customer_Address_index+3]
                order.save()
                order_details = driver.find_element(By.CLASS_NAME,"info")
                index = 0
                items =  (order_details.text).split("\n")
                while 1:
                    name = items[index].split(" x ")[0]
                    quantity = items[index].split(" x ")[1]
                    item_ , _ = MainappItem.objects.get_or_create(name=name)
                    order_item  = MainappOrderItem.objects.create(item = item_ , order=order, quantity=int(quantity),price=0)
                    index +=1
                    while 1 :
                        if items[index].startswith("Addons:"):
                            name_ = items[index].replace("Addons:", "")

                            add_ons , _ = MainappAddOns.objects.get_or_create(name=name_[:49])
                            order_item_add_ons , _ = MainappOrderItemAddOns.objects.get_or_create(order_item=order_item, add_ons=add_ons, price=0)
                            index +=1
                        if items[index] == "":
                            index +=1
                            break
                        if items[index].startswith("Note"):
                            break
                    if items[index].endswith('JOD'):
                        price = items[index].replace(" JOD", "")
                        order_item.price = price
                        order_item.save()
                        index +=1


                    if items[index].startswith("Note"):
                        break
        except Exception as e:
                print(channel.name,e)   
            


def login():
    email  = "Mickeys"
    password  = "Mickeys"

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless")

    global driver
    driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH,chrome_options=options)
    driver.maximize_window()
    driver.get("https://restaurant.csmena.com/#/auth/login")
    global wait
    wait = WebDriverWait(driver, 30)
    global channel
    channel,_ = MainappChannel.objects.get_or_create(name='Csmena')

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    inputs = driver.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(email)
    inputs[1].send_keys(password)

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(5)

    try:
        driver.find_element(By.XPATH,"//*[text()='Logout']").click()
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
    except:pass

def search(start_date,end_date):
    driver.get("https://restaurant.csmena.com/#/branch/history")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ng-invalid")))
    time.sleep(2)
    inputs = driver.find_elements(By.CLASS_NAME, "ng-invalid")
    inputs[1].send_keys(start_date.strftime('%m/%d/%Y'))
    inputs[2].send_keys(end_date.strftime('%m/%d/%Y'))

    driver.find_element(By.CLASS_NAME,"mat-form-field-infix").click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME,"mat-option")))
    time.sleep(2)
    for count , elemant in enumerate(driver.find_elements(By.TAG_NAME,"mat-option")):
        if count>0:
            elemant.click()
            time.sleep(2)
        brand_branch = (elemant.text)
        anyway = driver.find_element(By.CLASS_NAME,"btn-primary")
        ActionChains(driver).move_to_element(anyway).click().perform()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME,"btn-primary").click()

        try:wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='fa fa-history f-16']")))
        except:pass

        brand_branch = MainappBrandBranch.objects.get(csmena_name=brand_branch)

        read_orders(driver,brand_branch,count)
        for i in range (3):
            time.sleep(1)
            driver.execute_script("scrollBy(0,-1000);")

        driver.find_element(By.CLASS_NAME,"mat-form-field-infix").click()

        elemant.click()


def download_report(start_date,end_date):
    driver.get("https://restaurant.csmena.com/#/branch/reports")

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ng-invalid")))
    inputs = driver.find_elements(By.CLASS_NAME, "ng-invalid")
    inputs[1].send_keys(start_date.strftime('%m/%d/%Y'))
    inputs[2].send_keys(end_date.strftime('%m/%d/%Y'))
    
    driver.find_element(By.CLASS_NAME,"btn-primary").click()
    
    time.sleep(6)
    driver.execute_script("scrollBy(0,1000);")
    time.sleep(1)
    try:
        driver.find_element(By.CLASS_NAME,"buttons-excel").click()
        last_update(channel)
    except:print("csmena can't download report file")

def save_data(orderID, creationTime,customerPhoneNumber,pickUpType,branchName,totalAmount,deliveryCharge,orderStatus,isDeclined):

    order , _ = MainappOrder.objects.get_or_create(channel=channel,order_id=orderID)
    if isDeclined == False:
        order.status = "Delivered"
    else:
         order.status = "Cancelled"
    order.date_time=creationTime
    order.customer_mobile_number = "+962" + str(customerPhoneNumber)
    order.total= totalAmount
    order.delivary_fee= deliveryCharge
    order.type = pickUpType
    
    try:order.brand_branch = MainappBrandBranch.objects.get(csmena_name=branchName)
    except:print (channel.name,"can't find csmena name :",branchName)
    order.save()

def read_csv():
    list_of_files = os.listdir(settings.DOWNLOAD_PATH) #list of files in the current directory
    for each_file in list_of_files:
        if each_file.startswith('Report_created_on'): 
            file_name =os.path.join(str(settings.DOWNLOAD_PATH), each_file)

            df = pd.read_excel(file_name)
            for index, row in df.iterrows():
                # print(row['orderID'], row['creationTime'],row["customerPhoneNumber"],row["pickUpType"],row["branchName"],row["totalAmount"],row["deliveryCharge"],row["orderStatus"])
                save_data(row['orderID'], row['creationTime'],row["customerPhoneNumber"],row["pickUpType"],row["branchName"],row["totalAmount"],row["deliveryCharge"],row["orderStatus"],row["isDeclined"])
        
            if(os.path.exists(file_name) and os.path.isfile(file_name)):
                os.remove(file_name)
                print(file_name,"file deleted")
            else:print("file not found")
            break

def start(start_date,end_date,start_timer):
    try:
        login()
        while 1:
            download_report(start_date,end_date)
            read_csv()
            search(start_date,end_date)
            db.close_old_connections()
            time.sleep(60*15)
            end = datetime.now()
            timer = end - start_timer
            if timer.seconds > 3*60*60:
                driver.quit()
                print(timer.seconds)
                break
    except Exception as e:
            print(channel.name,e)   
            driver.quit()
            start(start_date,end_date,start_timer)
    
def start_csmena(start_date,end_date,start_timer):
    start_timer = datetime.now()
    start(start_date,end_date,start_timer)

  





