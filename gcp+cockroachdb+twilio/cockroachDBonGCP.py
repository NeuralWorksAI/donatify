import os
import json
import random
import psycopg2
import math



def connector():
    # cockroachstring = "get your own credentials"
    cockroachstring = os.environ.get('COCKROACHSTR')
    conn=psycopg2.connect(cockroachstring)
    return conn



def initialize(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS us (id INT PRIMARY KEY, username STRING,  userpassword STRING, useraddress STRING)"
        )


        cur.execute(
            "CREATE TABLE IF NOT EXISTS transactions (id INT PRIMARY KEY, userid STRING, amount STRING, merchant STRING, purchaseurl STRING)"
        )

        cur.execute(
            "CREATE TABLE IF NOT EXISTS donation (id INT PRIMARY KEY, userid STRING, transactionid STRING, charity STRING, amount STRING)"
        )

        cur.execute(
            "CREATE TABLE IF NOT EXISTS fundraiser (id INT PRIMARY KEY, userid STRING, name STRING, url STRING, startdate STRING, enddate STRING)"
        )


        cur.execute(
            "CREATE TABLE IF NOT EXISTS events (id INT PRIMARY KEY, userid STRING, name STRING, imageurl STRING, goal STRING, raised STRING)"
        )


        cur.execute(
            "CREATE TABLE IF NOT EXISTS sys (id INT PRIMARY KEY, donated STRING, used STRING, balance STRING, impacts STRING)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS charities (id INT PRIMARY KEY, name STRING)"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()





def add_event(conn, userid, name, imageurl, goal, raised):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM events")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)

        st = "donated"
        
        cur.execute("UPSERT INTO events (id, userid, name, imageurl, goal, raised) VALUES (" + i +", '" + userid + "', '" + name + "', '" + imageurl +"', '"  + goal +"', '"  + raised +"')")
        conn.commit()


    conn.commit()
    return i
    # print ("DONATION added")


def getevents(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, userid, imageurl, goal, raised FROM events")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        places = []

        for row in rows:
            place = {}
            place['id'] = row[0]
            place['name'] = row[1]
            place['userid'] = row[2]
            place['imageurl'] = row[3]
            place['goal'] = row[4]
            place['raised'] = row[5]

            places.append(place)

        return places 



def getevent(conn, eid):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, userid, imageurl, goal, raised FROM events")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        places = []

        place = {}

        for row in rows:
            if row[0] != eid:
                continue
            place['id'] = row[0]
            place['name'] = row[1]
            place['userid'] = row[2]
            place['imageurl'] = row[3]
            place['goal'] = row[4]
            place['raised'] = row[5]

            return place

            places.append(place)

        return place 



def add_donation(conn, userid, tid, charity, amount):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM donation")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)

        st = "donated"
        
        cur.execute("UPSERT INTO donation (id, userid, transactionid, charity, amount) VALUES (" + i +", '" + userid + "', '" + tid + "', '" + charity +"', '"  + amount +"')")
        conn.commit()


    conn.commit()
    return i
    # print ("DONATION added")

def add_transaction(conn, userid, amount, merchant, purchaseurl, charity):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM transactions")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)

        st = "donated"
        
        cur.execute("UPSERT INTO transactions (id, userid, amount, merchant, purchaseurl) VALUES (" + i +", '" + userid + "', '" + amount + "', '" + merchant +"', '"  + purchaseurl +"')")
        conn.commit()


        amt = float(amount)

        amt2 = math.ceil(amt)
        camt = amt2-amt
        camount = str(camt)


        add_donation(conn, userid, i, charity, camount)


    conn.commit()
    return i
    # print ("DONATION added")



def add_users(conn, uname, pw, uaddress):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM us")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)
        
        cur.execute("UPSERT INTO us (id, userpassword, username, useraddress) VALUES (" + i +", '" + pw +"', '" + uname  +"', '" + uaddress +"')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    return i
    # print ("user added")



def login(conn, username, pw):
    with conn.cursor() as cur:
        cur.execute("SELECT id, userpassword, username, useraddress FROM us")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            # print(row)
            # print (type(row))
            if row[2] == username and row[1] == pw:
                # print ("found")
                return True, row[0], row[3]
        return False, 'none', 'none', '-1' 


def getuserbyid(conn, uid):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, userpassword, usertype, username, lat, lon, useraddress FROM us")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            # print(row)
            # print (type(row))
            if row[0] == int(uid):
                # print ("found")
                return True, row[0], row[1], row[3], row[4], row[5], row[6], row[7]
        return False, 'none', 'none', '-1', '-1', '-1', '-1', '-1', '-1' , '-1'


def gettransactions(conn, userid):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, userid, cost, price, items, helperid, status FROM tasks")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        tasks = []

        for row in rows:
            if row[2] != userid:
                continue
             
            place = {}
            place['id'] = row[0]
            place['name'] = row[1]
            place['userid'] = row[2]
            place['cost'] = row[3]
            place['price'] = row[4]
            place['items'] = row[5]
            place['helperid'] = row[6]
            place['status'] = row[7]

            tasks.append(place)

        return tasks 




def delete_users(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

    print ("users table deleted")


def purgedb(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

    print ("users table deleted")



def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    request_json = request.get_json()
    conn = connector()
    initialize(conn)

    retjson = {}

    action = request_json['action']
    if action == "createuser" :
        uname = request_json['name']
        pw = request_json['password']
        uaddress = request_json['address']

        pid = add_users(conn, uname, pw, uaddress)

        retjson['status'] = "successfully added"
        retjson['id'] = pid

        return json.dumps(retjson)


    if action == "createevent" :
        name = request_json['name']
        uid = request_json['userid']
        imageurl = request_json['imageurl']
        goal = request_json['goal']

        raised = "0"
        
        eid = add_event(conn, uid, name, imageurl, goal, raised)

        retjson['status'] = "successfully added"
        retjson['id'] = eid

        return json.dumps(retjson)



    
    if action == "getplaces" :
        places = getplaces(conn)
        
        retjson['status'] = "successfully retrieved"
        retjson['id'] = places

        return json.dumps(retjson)



    if action == "getevents" :
        events = getevents(conn)
        
        retjson['status'] = "successfully retrieved"
        retjson['events'] = events

        return json.dumps(retjson)

    if action == "getevent" :
        eid = request_json['eid']
        event = getevent(conn)
        
        retjson['status'] = "successfully retrieved"
        retjson['event'] = event

        return json.dumps(retjson)





    if action == "pickuptask" :
        helperid = request_json['helperid']
        taskid = request_json['taskid']
        
        res = pendingtask(conn, helperid, taskid)
        retjson['status'] = "task successfully picked up"

        return json.dumps(retjson)
    
    if action == "accepttask" :
        taskid = request_json['taskid']

        res = acceptedtask(conn, taskid)
        
        retjson['status'] = "task successfully accepted"

        return json.dumps(retjson)   


    if action == "completetask" :
        taskid = request_json['taskid']

        res = completedtask(conn, taskid)
        
        retjson['status'] = "task successfully accepted"

        return json.dumps(retjson)    

    

    if action == 'login':
        username = request_json['username']
        pw = request_json['password']

        res = login(conn, username, pw)

        retjson['status'] = str(res[0])

        

        return json.dumps(retjson)



    if action == 'getuserbyid':
        uid = request_json['uid']

        res = getuserbyid(conn, uid)

        retjson['status'] = str(res[0])
        retjson['id'] = str(res[1])
        retjson['email'] = str(res[2])
        retjson['type'] = str(res[3])
        retjson['name'] = str(res[4])
        retjson['lat'] = str(res[5])
        retjson['lon'] = str(res[6])
        retjson['address'] = str(res[7])
        

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
