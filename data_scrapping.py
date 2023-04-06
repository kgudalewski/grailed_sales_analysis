from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import warnings
warnings.filterwarnings('ignore')

# from selenium.webdriver.chrome.options import Options       ## stayed window opened
# chrome_options = Options()                                  ## stayed window opened
# chrome_options.add_experimental_option("detach", True)      ## stayed window opened
# driver = webdriver.Chrome(options=chrome_options)           ## stayed window opened

driver = webdriver.Chrome()


def check_exists_by_xpath(xpath):
    global driver
    try:
       driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def get_links_to_listings_from_main_category(main_link):
    driver.get(main_link)
    #----- log in ------
    time.sleep(30)
    #-----logged in-----

    result = []
    basic_list_of_links = []
    price = 50

    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[1]/div[2]/div/button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[3]/div/button[5]').click()
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').clear()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').send_keys(
        0)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').clear()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').send_keys(0)
    time.sleep(2)

    while True:
        driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').clear()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').send_keys(price - 50)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').clear()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').send_keys(price)
        time.sleep(2)
        basic_list_of_links.append(str(driver.current_url))
        price += 50

        if price == 350:
            driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').clear()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').send_keys(300)
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').clear()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[2]/input').send_keys(3000)
            time.sleep(2)
            # driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[2]/div[2]/div/div[5]/div/div[1]/input').send_keys(300)
            # time.sleep(2)
            basic_list_of_links.append(str(driver.current_url))
            break

    for link in basic_list_of_links:
        driver.get(link)
        # listing_number = driver.find_element(By.XPATH, '//*[@id="shop"]/div/div/div[1]/div[1]/div/span').text
        # listing_number = int(listing_number.split(" ")[0])
        # scroll_number = round(listing_number/40)+1
        #
        # for i in range(0, scroll_number):
        #     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     time.sleep(1)

        for i in range(25):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)

        list_of_elements = driver.find_elements(By.CLASS_NAME, 'listing-item-link')

        for element in list_of_elements:
            result.append(element.get_attribute(name="href"))
        print(len(list_of_elements))
    return result


def get_values(list_of_links):

    df = pd.DataFrame(columns=["title", "link", "size", 'condition', "color", "seller_name", "designers", "description",
                               "num_of_photos", "num_of_tags", "measurements", "location", "shipping_price", "price",
                               "sold_price"])
    for link in list_of_links:
        driver.get(link)
        time.sleep(1)

        try:
            title = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/h1').text
        except:
            title = None

        if check_exists_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[3]/span[1]'):
            item_price = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[3]/span[1]').text
        else:
            item_price = None

        if check_exists_by_xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div[2]/div[1]/div[3]/span'):
            sold_price = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div[2]/div[1]/div[3]/span').text.split(" ")[0]
            item_price = None
        else:
            sold_price = None

        try:
            size = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[2]/span').text
        except:
            size = None

        try:
            condition = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[5]/span').text
        except:
            condition = None

        try:
            color = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[4]/span').text
        except:
            color = None

        try:
            seller_name = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/a/span').text
        except:
            seller_name = None

        try:
            designers = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[2]/p[1]').text
        except:
            designers = None

        try:
            description = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[2]/div[2]/div[5]/div').text.replace("\n", "\\n")
        except:
            description = None

        idx = 1
        while True:
            if check_exists_by_xpath(f'//*[@id="__next"]/div/main/div/div[1]/div[1]/div/div[2]/img[{idx}]'):
                idx += 1
            else:
                num_of_photos = idx - 1
                break

        idx = 1
        while True:
            if check_exists_by_xpath(f'//*[@id="__next"]/div/main/div/div[1]/div[2]/div[2]/div[2]/div[6]/div/a[{idx}]'):
                idx += 1
            else:
                num_of_tags = idx - 1
                break

        if check_exists_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[1]/div[1]') \
                and check_exists_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[2]/div[1]'):
            measurements = 1
        else:
            measurements = 0

        if check_exists_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span'):
            full_location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text
            location = full_location.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("us")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("eu")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("uk")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("asia")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("ca")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("au")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
            if location == "shipping":
                sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
                sel.select_by_value("other")
                location = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[4]
        else:
            location = None

        if check_exists_by_xpath('//*[@id="listing_page_shipping_destination"]'):
            shipping_sum = 0
            sel = Select(driver.find_element(By.XPATH, '//*[@id="listing_page_shipping_destination"]'))
            for place in ["us", "uk", "eu", "asia", "ca", "au", "other"]:
                sel.select_by_value(place)
                value = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div[1]/div[2]/div[1]/div[4]/span').text.split(" ")[1].strip("$")
                if value == "-":
                    shipping_sum = None
                    break
                else:
                    shipping_sum += int(value)
            if shipping_sum is not None:
                shipping_price = round(shipping_sum / 7, 2)
            else:
                shipping_price = None
        else:
            shipping_price = None

        new_row = {"title": title, "link": link, "size": size, 'condition': condition, 'color': color,
                   "seller_name": seller_name, "designers": designers, "description": description,
                   "num_of_photos": num_of_photos, "num_of_tags": num_of_tags, "measurements": measurements,
                   "location": location, "shipping_price": shipping_price, "price": item_price, "sold_price": sold_price}
        df = df.append(pd.DataFrame([new_row], index=[len(df)], columns=df.columns))

    return df


if __name__ == "__main__":

    # mercedes_url = "https://www.grailed.com/shop/pnsoZ2mf6A"
    # mercedes_sold_url = "https://www.grailed.com/sold/VLyUS38lkA"
    # list_of_links_to_scrap = []
    # for main_link in [mercedes_url, mercedes_sold_url]:
    #     list_of_links_to_scrap += get_links_to_listings_from_main_category(main_link=main_link)
    #     print(len(list_of_links_to_scrap))
    # marlboro_df = get_values(list_of_links=list_of_links_to_scrap)
    # marlboro_df.to_csv("mercedes.csv", encoding="utf-16")