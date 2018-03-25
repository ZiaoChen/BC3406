import requests
import csv

headers = ['id','name', 'created_time', 'link', 'message', 'likes', 'comments', 'shares']
writer = csv.DictWriter(open('facbook.csv', 'wb'), fieldnames=headers)
writer.writeheader()

page = 100
url = 'https://graph.facebook.com/paulaschoicesingapore/posts?access_token=EAACEdEose0cBAB1Ao8qtAELzfY8qAtkorYFx69C7dlQboh38nxK50h1QD0sZCdffM8oZAZCLkOIpzqrId2q4RreyrGCdXUjvyiw9L0IvYoJR5cFHTNGp0KnB93CamYyjzGmdVra9alMmCggAr5CoJP32JM2hXxoNOAqth9fq8CKVScDypodaQ8hwP1UtlrATkIqY2f7wgZDZD&fields=shares,likes.summary(true),comments.summary(true),link,message,name,created_time'
for i in range(page):
    print i
    data = requests.get(url).json()
    for post in data['data']:
        crawl_post = {}
        crawl_post['id'] = post['id']
        if 'link' in post:
            crawl_post['link'] = post['link']
        if 'name' in post:
            crawl_post['name'] = post['name']
        if 'message' in post:
            crawl_post['message'] = post['message']
        crawl_post['created_time'] = post['created_time']
        crawl_post['likes'] = str(post['likes']['summary']['total_count'])
        crawl_post['comments'] = str(post['comments']['summary']['total_count'])
        if 'shares' in post:
            crawl_post['shares'] = str(post['shares']['count'])
        else:
            crawl_post['shares'] = str(0)
        writer.writerow({k: v.encode('utf8') for k, v in crawl_post.items()})
    if 'paging' not in data:
        break
    url = data['paging']['next']


