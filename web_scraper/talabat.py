from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os
from .utils import *

from scraper.settings import DOWNLOAD_PATH
from .models import MainappBrand, MainappOrder, MainappChannel, MainappBrandBranch ,MainappOrderItem, MainappStatus, MainappItem, MainappAddOns,MainappOrderItemAddOns
import dateutil.parser
from datetime import datetime, timedelta
from django.conf import settings 

def login(start_date,end_date):  
    email  = "a.shehadeh@kitchefy.com"
    password  = "Abdelhadi@123"

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
    channel = MainappChannel.objects.get(name='Talabat')

    driver.get("https://talabat.portal.restaurant/dashboard")
    wait.until(EC.presence_of_element_located((By.ID,"login-email-field")))
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.ID,"button_login").click()

    time.sleep(10)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME,"css-19ns9tv")))

    driver.get("https://talabat.portal.restaurant/orders?from={}&to={}&billableFilterState=ALL".format(start_date,end_date))
    driver.execute_script('window.open("https://talabat.portal.restaurant/vendor-availability-tb?int_ref=side-nav")')
    driver.execute_script('window.open("https://talabat.portal.restaurant/finances-tb/financial-report?vendor=TB_JO;663459")')

    return(driver)

def ignore_tabs():
    for x in range(3):
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[x])

        try:driver.find_element(By.XPATH,"//*[text()='Later']").click()
        except:pass
            
        try:driver.find_element(By.XPATH,"//*[text()='No thanks']").click()
        except:pass

def save_data(row):
    order , _ = MainappOrder.objects.get_or_create(channel=channel,order_id=row[1])
    if row[4]== "Delivered":
        status = "Delivered"
    else:
        status = "Cancelled"
    order.date_time=dateutil.parser.parse(row[5])
    order.status=status
    order.total= row[18]
    order.delivery_zone=row[14]
    order.delivary_fee= row[23]
    order.payment_method=row[18]
    order.type = "Delivery"
    try:order.brand_branch = MainappBrandBranch.objects.get(talabat_id=row[3])
    except:print (channel.name,"can't find brand_branch name :",row[3] )
    order.save()

def read_csv_file():
    file = open(os.path.join(str(settings.DOWNLOAD_PATH), "orderDetails.csv"))
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
            rows.append(row)
            save_data(row)
    file.close()
    file = os.path.join(str(settings.DOWNLOAD_PATH), "orderDetails.csv")
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")

def get_orders():
    driver.switch_to.window(driver.window_handles[0])
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-testid="order-email-card"]')))
    driver.find_element(By.XPATH,'//*[@data-testid="order-email-card"]').click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@data-testid="download-btn"]')))
    driver.find_element(By.XPATH,'//*[@data-testid="download-btn"]').click()
    time.sleep(30)
    read_csv_file()

def get_order_details(order_id):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"webapp_global-MuiSvgIcon-fontSizeSmall")))
    order_details = driver.find_element(By.TAG_NAME, "tbody")
    items = order_details.find_elements(By.TAG_NAME , "tr")
    order , _  = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)

    for item in items:
        if not "iGYJVa" in item.get_attribute("class"): # is add ons 
            data = item.find_elements(By.TAG_NAME, "td")            
            item , _ = MainappItem.objects.get_or_create(name=data[2].text)
            quantity = data[0].text.replace("×", "")
            price =  data[4].text.split("JOD ")[1]
            order_item  = MainappOrderItem.objects.create(item = item , order=order, quantity=quantity,price=price)
            
        else:
            data2 = item.find_elements(By.TAG_NAME, "td")
            name = data2[2].text.split("× ")[1]
            quantity = data2[2].text.split("× ")[0]
            price = data2[4].text.split("JOD ")[1]
            add_ons , _ = MainappAddOns.objects.get_or_create(name=name)
            order_item_add_ons , _ = MainappOrderItemAddOns.objects.get_or_create(quantity=quantity,price=price,order_item=order_item, add_ons=add_ons)
               
    driver.find_element(By.CLASS_NAME , "plugin-muiv4-MuiIconButton-colorInherit").click()

def get_orders_details():
    driver.switch_to.window(driver.window_handles[0])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"sc-iGrrsa")))
    order_list = driver.find_elements(By.CLASS_NAME, "sc-iGrrsa")

    for order in order_list:
        order_id = order.find_element(By.TAG_NAME,"p").text
        order_ , created = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id)
        if len(MainappOrderItem.objects.filter(order=order_)) == 0:
            
            status = order.find_elements(By.TAG_NAME,"p")[2].text
            if status == "Delivered" or status == "Cancelled":
                order.find_element(By.TAG_NAME,"p").click()
                get_order_details(order_id)


def update_status(cell_data):
    channel = MainappChannel.objects.get(name='Talabat')
    try:
        brand_branch = MainappBrandBranch.objects.filter(talabat_name=cell_data[0]).first()  # we need to add talabat name 
        status, created = MainappStatus.objects.get_or_create(channel=channel,brand_branch=brand_branch)
        status.status = cell_data[1][:6]
        status.datetime = datetime.now()
        status.save()
    except:print(channel.name,"can't find :",cell_data[0] )
        
def get_Status():
    driver.switch_to.window(driver.window_handles[2])
    list_status= []
    for row in driver.find_elements(By.TAG_NAME,'tr'):
        cell_data = []
        for index, cell in enumerate(row.find_elements(By.TAG_NAME,'td')[1:]):
            cell_data.append(cell.text)
        if len(cell_data)>2:
            update_status(cell_data)



     
def start(start_date,end_date,start_timer):

    try:
        login(start_date,end_date)  

        time.sleep(10) 
        while 1:
            ignore_tabs()
            get_orders() 
            get_orders_details()
            get_Status()
            last_update(channel)
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
        


def start_talabat(start_date,end_date,start_timer):
    start_timer = datetime.now()
    start(start_date,end_date,start_timer)
