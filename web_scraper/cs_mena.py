
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from .models import MainappOrder, MainappChannel, MainappBrandBranch ,MainappOrderItem, MainappItem,MainappAddOns,MainappOrderItemAddOns
import dateutil.parser
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from django.conf import settings 


def read_orders(driver,brand_branch,count):
    time.sleep(10)

    orders =driver.find_elements(By.TAG_NAME, "tr")

    for order in orders[1:]:
        csmena_id = (order.text).split(" ")[0].replace("#", "")
        order.find_element(By.TAG_NAME,"i").click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"mat-card-subtitle")))
        time.sleep(1)
        dateTime = driver.find_element(By.CLASS_NAME,"mat-card-subtitle").text
        time.sleep(5)
        driver.find_element(By.CLASS_NAME,"w-100").click()
        time.sleep(1)
        dateWithTime = datetime.strptime(dateTime, '%b %d, %Y, %H:%M:%S %p')
        date= datetime.strftime(dateWithTime, '%y%m%d')

        order_id = str(date) + str(brand_branch.id) +str(csmena_id)
        if not MainappOrder.objects.filter(order_id=order_id).exists():            
            order.click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,"order-details-box")))
            try:order_details = driver.find_elements(By.CLASS_NAME, "order-details-box")[1].text
            except: print (channel.name,"ordeer don't have details")

            status = order.find_element(By.CLASS_NAME, "label-info").text
            if status == "Finished":
                status="Delivered"
            else:             
                status="Cancelled"

            order_list = order_details.split("\n")
            Customer_Phone_index = order_list.index("Phone")

            order , created = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)
            order.status = status
            order.date_time = dateWithTime
            order.brand_branch = brand_branch       
            Customer_Name_index = order_list.index("Name")
            order.customer_name = order_list[Customer_Name_index+1]
            order.total = (driver.find_element(By.CLASS_NAME, "total-item").text).split("\n")[1].replace("JOD", "")
            order.delivary_fee = (driver.find_element(By.CLASS_NAME, "delivery-item").text).split("\n")[1].replace("JOD", "")
            order.customer_mobile_number = order_list[Customer_Phone_index+1]
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
    wait = WebDriverWait(driver, 60)
    global channel
    channel = MainappChannel.objects.get(name='csmena')

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
    inputs = driver.find_elements(By.CLASS_NAME, "ng-invalid")
    inputs[1].send_keys(start_date.strftime('%m/%d/%Y'))
    inputs[2].send_keys(end_date.strftime('%m/%d/%Y'))

    driver.find_element(By.CLASS_NAME,"mat-form-field-infix").click()
    time.sleep(10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME,"mat-option")))

    for count , elemant in enumerate(driver.find_elements(By.TAG_NAME,"mat-option")):
        if count>0:
            elemant.click()
            time.sleep(5)
        # if count ==0: 
        #     print("aaaaa")
        #     pass   
        brand_branch = (elemant.text)
        anyway = driver.find_element(By.CLASS_NAME,"btn-primary")
        ActionChains(driver).move_to_element(anyway).click().perform()
        driver.find_element(By.CLASS_NAME,"btn-primary").click()
        time.sleep(20)

        brand_branch = MainappBrandBranch.objects.get(csmena_name=brand_branch)
        read_orders(driver,brand_branch,count)
        for i in range (2):
            time.sleep(1)
            driver.execute_script("scrollBy(0,-1000);")

        time.sleep(15)
        print(len(driver.find_elements(By.TAG_NAME,"mat-option")))

        driver.find_element(By.CLASS_NAME,"mat-form-field-infix").click()

        elemant.click()



def start(start_date,end_date,start_timer):
    try:
        login()
        while 1:
            search(start_date,end_date)
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

  





