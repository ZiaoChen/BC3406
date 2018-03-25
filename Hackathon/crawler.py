from selenium import webdriver
import time
import csv
from selenium.webdriver import ChromeOptions
import traceback
base_url = 'https://paulaschoice.sg/'
options = ChromeOptions()
options.add_argument('--disable-popup-blocking')
options.add_experimental_option("prefs", {'profile.managed_default_content_settings.images': 2,
                                          'profile.managed_default_content_settings.javascript': 2})
driver = webdriver.Chrome('chromedriver', chrome_options=options)
cat_driver = webdriver.Chrome('chromedriver', chrome_options=options)
product_driver = webdriver.Chrome('chromedriver')

product_headers = ['Category1', 'Category2', 'Category3', 'Name', 'Price', 'Description', 'Variation', 'Rating', 'No_of_reviews']
review_headers = ['Name', 'Rating', 'Title', 'Content']
product_writer = csv.DictWriter(open('Data/Product.csv', 'wb'), fieldnames=product_headers)
review_writer = csv.DictWriter(open('Data/Review.csv', 'wb'), fieldnames=review_headers)
product_writer.writeheader()
review_writer.writeheader()
parent_directory = ""
parent_directory_2 = ""

def get_into_product_page(product_driver, url, parent1, parent2, parent3, product_writer, review_writer):
    product_driver.get(url)
    time.sleep(2)
    product = {}
    review = {}
    product['Category1'] = parent1
    product['Category2'] = parent2
    product['Category3'] = parent3
    print url
    product['Name'] = product_driver.find_element_by_class_name('product_name').text
    review['Name'] = product['Name']
    product['Price'] = product_driver.find_element_by_class_name('current_price').find_element_by_xpath('//span/span').text.replace('$', "")
    product['Description'] = product_driver.find_element_by_class_name('description').text
    try:
        product['Variation'] = ','.join([i.text for i in product_driver.find_element_by_tag_name('select').
                                         find_elements_by_tag_name('option')])
    except:
        product['Variation'] = ""
    try:
        rating_element = product_driver.find_element_by_class_name('spr-summary').find_element_by_tag_name('span').find_elements_by_tag_name('meta')
        product['Rating'] =  rating_element[3].get_attribute('content')
        product['No_of_reviews'] = rating_element[2].get_attribute('content')
    except:
        product['Rating'] = '0'
        product['No_of_reviews'] = '0'
    try:
        review_list = product_driver.find_elements_by_class_name('spr-review')
        print len(review_list)
        for r in review_list:
            review["Title"] = r.find_element_by_tag_name('h3').text
            review["Content"] = r.find_element_by_class_name('spr-review-content-body').text
            try:
                review["Rating"] = str(5 - len(r.find_elements_by_xpath(".//i[contains(@class, 'spr-icon spr-icon-star-empty')]")))
            except:
                review["Rating"] = '0'
            print review
            review_writer.writerow({k: v.encode('utf8') for k, v in review.items()})
    except:
        print traceback.print_exc()
        pass

    product_writer.writerow({k: v.encode('utf8') for k, v in product.items()})


def get_into_cat_page(cat_driver, url, product_driver, parent1, parent2, parent3, product_writer, review_writer):
    cat_driver.get(url)
    products = cat_driver.find_elements_by_xpath("//div[contains(@class, 'four columns alpha thumbnail even')]/a")
    for product in products:
        get_into_product_page(product_driver, product.get_attribute('href'), parent1, parent2, parent3, product_writer, review_writer)

driver.get(base_url)
parent_list = driver.find_elements_by_xpath("//ul[contains(@class,'menu center')]/li")
for parent in parent_list:
    parent1 = parent.find_element_by_tag_name('a').get_attribute('innerHTML').split('&nbsp;')[0].strip()
    sub_parent_list = parent.find_elements_by_tag_name('li')
    for sub_parent in sub_parent_list:
        a_tag_list = sub_parent.find_elements_by_tag_name('a')
        try:
            sub_parent.find_element_by_class_name('sub-link')
            for a_tag in a_tag_list:
                if a_tag.get_attribute('class') != 'sub-link':
                    parent2 = a_tag.get_attribute('innerHTML').replace("amp;","")
                else:
                    parent3 = a_tag.get_attribute('innerHTML').replace("amp;","")
                    get_into_cat_page(cat_driver, a_tag.get_attribute('href'), product_driver, parent1, parent2, parent3, product_writer, review_writer)
        except:
            parent3 = ""
            for a_tag in a_tag_list:
                parent2 = a_tag.get_attribute('innerHTML').replace("amp;","")
                get_into_cat_page(cat_driver, a_tag.get_attribute('href'), product_driver, parent1, parent2, parent3, product_writer, review_writer)





driver.quit()
cat_driver.quit()
product_driver.quit()