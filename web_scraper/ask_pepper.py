from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from .models import MainappOrder, MainappChannel, MainappBrandBranch ,MainappOrderItem, MainappItem,MainappAddOns,MainappOrderItemAddOns,MainappBrand
import dateutil.parser
from datetime import datetime
from django.conf import settings 


def get_username_and_password():
    email  = "a.shehadeh@kitchefy.com"
    password  = "Abdelhadi@123"
    return email,password


def login(email,password):
    global channel
    channel = MainappChannel.objects.get(name='AskPepper')

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless")

    global driver
    driver = webdriver.Chrome(executable_path=settings.DRIVER_PATH,chrome_options=options)
    driver.maximize_window()

    url = "https://sirvycart.b2clogin.com/sirvycart.onmicrosoft.com/b2c_1_signin_v2/oauth2/v2.0/authorize?client_id=700621fb-3356-4427-b17a-35cd7282f1b5&redirect_uri=https%3A%2F%2Fdashboard.ask-pepper.com%2Fauth%2Fauthcallback&response_type=code&scope=openid%20https%3A%2F%2Fsirvycart.onmicrosoft.com%2Fapi-prod%2Faccess.readwrite&state=1e2acbf32b744467a1425e286bd518e7&code_challenge=14Nhyk6WFbu-pb6b2GmGfQxYewLtSKYOPIAEEqP0JI0&code_challenge_method=S256&response_mode=query"

    driver.get(url)
    global wait
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID,"email")))
    driver.find_element(By.ID, "email").send_keys(email)
    wait.until(EC.presence_of_element_located((By.ID,"password")))
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "next").click()
    time.sleep(10)
def get_order_details(status,total,deliveryZone,paymentMethod,order,type):
    
        order_text = driver.find_element(By.CLASS_NAME, "mat-grid-list").text
        list_data = order_text.split("\n")
        try:
            Order_time_index = list_data.index("Order time")
            if list_data[Order_time_index+1] != "Brand":
                order_date = datetime.strptime(list_data[Order_time_index+1], '%d/%m/%Y %H:%M %p')
                order.date_time = order_date
        except:
            print(channel.name,"erorr", list_data )


        Customer_Name_index = list_data.index("Customer Name")
        order.customer_name = list_data[Customer_Name_index+1]

        phone_number_index = list_data.index("Phone Number")
        order.customer_mobile_number = list_data[phone_number_index+1]
        order.status = status
        type_index = list_data.index("Type")
        order.type = list_data[type_index+1]
        order.total = total
        order.type = type
        info = driver.find_elements(By.XPATH,"//*[@class='delivery ng-star-inserted']")
        for i in info : 
            info_data = i.text.split("\n")
            if  info_data[0] == "Discount":
                order.promo_code = info_data[1].split("OD")[1].split(" - Code")[0]
            if  info_data[0] == "Delivery" and info_data[1]!= "Delivery fees are not specified for this order" :
                order.delivary_fee = info_data[1].replace("JOD","")

        order.delivery_zone = deliveryZone
        order.payment_method = paymentMethod
        order.save()

        items =  driver.find_elements(By.XPATH, "//div[@style='place-content: space-around flex-end; align-items: stretch; flex-direction: column; box-sizing: border-box; display: flex;']")
       
        for item in items:
            # try:
            item_details = item.find_element(By.TAG_NAME,"div").text.split("\n")
            quantity = item_details[0].split(" ", 1)[0].replace("x", "")
            name = item_details[0].split(" ", 1)[1]
            price = item_details[1].replace("JOD", "")
            item_ , _ = MainappItem.objects.get_or_create(name=name)

            order_item = MainappOrderItem.objects.create(item = item_ , order=order, quantity=quantity, price=price )

            # except:
            #     print(channel.name,"erorr in item ")
            item_add_ons= (item.find_elements(By.CLASS_NAME,"ng-star-inserted"))

            for add_ons in item_add_ons:
                    data = add_ons.text.split('\n')
                    name = data[0]
                    try:
                        if data[1] =="-": price = 0
                        else: price = data[1].replace("+","")
                        quantity = 1
                        add_ons , _ = MainappAddOns.objects.get_or_create(name=name)
                        order_item_add_ons , _ = MainappOrderItemAddOns.objects.get_or_create(quantity=quantity,price=price,order_item=order_item, add_ons=add_ons)
                    except:
                        print ("this is note ")
def search(start_date,end_date):
    time.sleep(3)
    driver.get("https://dashboard.ask-pepper.com/admin/reports/all-tickets")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "mat-start-date")))
    webElement = driver.find_element(By.CLASS_NAME, "mat-start-date")
    webElement.click()
    webElement.send_keys(Keys.CONTROL + "a")
    webElement.send_keys(Keys.DELETE)

    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "mat-start-date").send_keys(start_date.strftime('%m/%d/%Y'))
    driver.find_element(By.CLASS_NAME, "mat-raised-button").click()
    time.sleep(2)
    while 1:
        time.sleep(4)

        orders = driver.find_elements(By.CLASS_NAME, "mat-row")
        count=0
        brand_name = driver.find_element(By.XPATH,"//*[@class='mat-focus-indicator mat-menu-trigger mat-button mat-button-base']").text.replace("expand_more","").strip()
        
        # brand =MainappBrand.objects.get(name=brand_name)

        
        for order in orders:
            fp = order.find_element(By.CLASS_NAME, "cdk-column-outlet").text

            try:brand_branch = MainappBrandBranch.objects.get(askpaper_name=brand_name+" "+fp)
            
            except:
                print( channel.name,"can't find askpaper name", brand_name+" "+fp)
                brand_branch = None
            if brand_branch is not None:
                order_id = order.find_element(By.CLASS_NAME,"mat-button-wrapper").text
                
                order_ , created = MainappOrder.objects.get_or_create(channel=channel,order_id=order_id,brand_branch=brand_branch)
                if created != True:
                    count+=1
                
                if len(MainappOrderItem.objects.filter(order=order_.id)) == 0:
                    status =order.find_element(By.CLASS_NAME, "mat-column-status").text
                    if status == "Completed":
                        status = "Delivered"
                    else:
                        status = "Cancelled"

                    total = order.find_element(By.CLASS_NAME, "cdk-column-total").text.replace("JOD", "")
                    deliveryZone = order.find_element(By.CLASS_NAME, "cdk-column-deliveryZone").text
                    paymentMethod = order.find_element(By.CLASS_NAME, "mat-column-paymentMethod").text
                    type = order.find_element(By.CLASS_NAME, "cdk-column-type").text.lower().capitalize()

                    order.find_element(By.CLASS_NAME, "mat-stroked-button").click()
                    time.sleep(2)

                    get_order_details(status,total,deliveryZone,paymentMethod,order_,type)

                    driver.find_element(By.CLASS_NAME, "mat-secondary").click()   

                    time.sleep(3)
        # if count > 2  or len(orders)< 9 :
        #     break
        element= driver.find_element(By.CLASS_NAME,"mat-sidenav-content")
        driver.execute_script("arguments[0].scrollBy(0, 10000)", element)
        driver.find_elements(By.CLASS_NAME,"mat-paginator-icon")[-1].click()

def get_brands_data(start_date,end_date):
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='mat-focus-indicator mat-menu-trigger mat-button mat-button-base']" )))
    driver.find_element(By.XPATH, "//*[@class='mat-focus-indicator mat-menu-trigger mat-button mat-button-base']" ).click()
    wait.until(EC.presence_of_element_located(( By.CLASS_NAME,"mat-menu-item")))
    brands = driver.find_elements(By.CLASS_NAME,"mat-menu-item")
    for index, brand in enumerate (brands):
        
        time.sleep(2)
        list_of_brands = driver.find_element(By.CLASS_NAME,"mat-menu-content")
        list_of_brands.find_elements(By.TAG_NAME,"button")[index].click()
        search(start_date,end_date)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='mat-focus-indicator mat-menu-trigger mat-button mat-button-base']" )))

        driver.find_element(By.XPATH, "//*[@class='mat-focus-indicator mat-menu-trigger mat-button mat-button-base']" ).click()

def start(start_date,end_date,start_timer):
    # try:
        email ,password = get_username_and_password()
        login(email, password)
        while 1:
            get_brands_data(start_date,end_date)
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




def start_ask_pepper(start_date,end_date,start_timer):
    start_timer = datetime.now()
    start(start_date,end_date,start_timer)
 