import requests
import csv
import sys
import traceback
# reload(sys)
# sys.setdefaultencoding('UTF8')

base_url = 'https://hackathon.paulaschoice.tech/events/?email=%s@email.com'
normal_headers = [u'updated_date', u'event_name', u'creation_date', u'completed_at', u'total_discounts', u'order_number',
           u'id', u'processing_method', u'total_price', u'user_id', u'created_at', u'gateway',
           u'abandoned_checkout_url', u'intercom_user_id', u'email']
product_headers = [u'product_id', u'product_title', u'product_price',
           u'product_status', u'product_grams', u'product_sku']

# sensitivity, cart, skintype, name, concerns, gender, age, tracking_number, type

def getHeader(base_url, ran):
    final_headers = set()
    for i in range(1, ran):
        try:
            response = requests.get(base_url % 'customer%d' % i, timeout=6).json()
            for event in response:
                final_headers = final_headers.union(event.keys())
                for key in event["metadata"]:
                    # if 'product' not in key:
                    # if isinstance(event["metadata"][key], dict):
                    #     for key2 in event['metadata'][key]:
                    #         final_headers.add('%s_%s' %(key, key2))
                    # else:
                    final_headers.add(key)
        except:
            pass
    final_headers.remove('metadata')
    return final_headers
#
# metadata_headers = getHeader(base_url, 50)
# print metadata_headers
# print len(metadata_headers)
max_product = 10
with open('Events.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=normal_headers+product_headers)
    writer.writeheader()
    for i in range(1, 10000):
        try:
            response = requests.get(base_url % 'customer%d'% i, timeout=10).json()
            for event in response:
                if event["event_name"] != 'performed-discover':
                    print("here")
                event.update(event['metadata'])
                product_dict = {k: v for k, v in event.items() if k in normal_headers}
                if "total_price" in product_dict:
                    product_dict["total_price"] = product_dict["total_price"]["amount"]

                if "total_discount" in product_dict:
                    product_dict["total_discount"] = product_dict["total_discount"]["amount"]

                if "order_number" in product_dict:
                    product_dict["order_number"] = product_dict["order_number"]["value"]

                if isinstance(product_dict['id'], dict):
                    product_dict['id'] = product_dict['id']['value']

                for j in range(1, max_product+1):
                    if 'product_%d_id' %j not in event:
                        break
                num_product = j - 1
                for j in range(1, num_product + 1):
                    temp_dict = product_dict.copy()
                    temp_dict['product_id'] = event['product_%d_id' %j]['value']
                    temp_dict['product_title'] = event['product_%d_title' %j]
                    if isinstance(event['product_%d_price' % j], dict):
                        temp_dict['product_price'] = event['product_%d_price' % j]['amount']
                    else:
                        temp_dict['product_price'] = event['product_%d_price' % j]
                    if 'product_%d_status' % j in event:
                        temp_dict['product_status'] = event['product_%d_status' % j]
                    if 'product_%d_grams' % j in event:
                        temp_dict['product_grams'] = event['product_%d_grams' % j]
                    temp_dict['product_sku'] = event['product_%d_sku' % j]
                    writer.writerow(temp_dict)
            print (i)
        except Exception as e:
            # print e
            print (traceback.print_exc())
            pass
