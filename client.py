import json
import http.client
import random

# take the input for sources from the user
sources = input('Please enter the source of marketplace: ').split(' ')
random.shuffle(sources)

#initialize a random order id
order_id = random.choice(range(1000,10000))

# take the input for the products from the user
products = input('Enter the product names: ').split(' ')

# lets make a connection to the service provider
conn = http.client.HTTPConnection("localhost", 8000)
headers = {'Content-type': 'application/json'}

# create a data simulator here.
# it attaches random products with random quantity for an order from marketplace
i=0
while (i<len(sources)):
    source = sources[i]
    order = dict()
    order['source']=source
    order['order_id'] = order_id + 1
    order_id+=1
    lines = list()
    for product in random.choices(products, k=2):
        lines.append({
            'product' : product,
            'quantity' : random.choice([0,1,2,3,4,5,6])
        })
    order['lines'] = lines

    # print order details for comparing with output of api
    print(order)
    
    #lets call the api with orders
    order_json = json.dumps(order)

    conn.request('POST', '/api/', order_json, headers)

    response = conn.getresponse()
    # print response from api
    print(response.read().decode(), response.status)
    i+=1
    if response.status==500:
        break
