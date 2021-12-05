import requests
import json


def addcustomer(fname, lname, street, streetnum, city, state, zipd):
    

    url = "http://api.nessieisreal.com/customers"

    querystring = {"key":"get ur own key"}

    # payload = "{\r\n  \"first_name\": \"oxfam\",\r\n  \"last_name\": \"the charity\",\r\n  \"address\": {\r\n    \"street_number\": \"123\",\r\n    \"street_name\": \"some needy street\",\r\n    \"city\": \"some city\",\r\n    \"state\": \"fl\",\r\n    \"zip\": \"33146\"\r\n  }\r\n}"

    payload = {}
    payload['first_name'] = fname
    payload['last_name'] = lname
    address = {}
    address['street_number'] = streetnum
    address['street_name'] = street
    address['city'] = city
    address['state'] = state
    address['zip'] = zipd

    payload['address'] = address
    
    payl = json.dumps(payload)

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payl, headers=headers, params=querystring)

    print(response.text)
    return json.loads(response.text)
    


def getcustomers(keyword):
    
    url = "http://api.nessieisreal.com/customers"

    querystring = {"key":"get ur own key"}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "5d2dd985-c70d-4b15-a7fb-66b30ec0f89d"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    print(response.text)
    
    dat =  json.loads(response.text)
    
    rt = []
    
    if keyword != "":
        for x in dat:
           robj = {}
           if x['last_name'] != keyword:
               continue
           robj['name'] = x['first_name']
           robj['id'] = x['_id']
           
           rt.append(robj)
    
    else:
        for x in dat:
            robj = {}

            robj['name'] = x['first_name']
            robj['id'] = x['_id']
            rt.append(robj)
    
    return rt
        


##test

# rs = addcustomer("world wildlife fund", "the charity", "some street", "124", "miami", "FL", "33152")

# print (rs['objectCreated']['_id'])

rt = getcustomers("the charity")

print (rt)
