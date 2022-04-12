#from crypt import methods
from operator import attrgetter
from itertools import product
import os
from unicodedata import name
from unittest import result
from urllib import parse
from webbrowser import get
from flask import Flask, request, session, json , render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse

# from tabulate import tabulate


SECRET_KEY = os.urandom(16)

## Init Flask APp
app = Flask(__name__)


def dataStr():
    base_url = 'https://windowshoppingserver.herokuapp.com/product/All'
    data = requests.get(base_url).json()
    # print(data)
    dat = 'name     price       description     quantity        Shop\n\n'

    for product in data:
        dat =dat+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
        print(dat)

    return dat




@app.route('/')
def index():
     return "window shoping whatsapp chatbot running"
@app.route('/bot', methods=['GET','POST'])


def bot():
    
    user_session = None
    # msg = request.form.get('Body')
    counter = session.get('counter', 0)

    # get the message from the user 
    user_msg = request.values.get('Body', '').lower()

    ## Init the response
    bot_resp= MessagingResponse()
    msg = bot_resp.message()

    r = requests.get('https://windowshoppingserver.herokuapp.com/product/All')
    print(r)
    data1 = r.json()

    mother=[]
    for X in data1:
            pname=X['Name']
            mother.append(pname)
        

    basics=["hello","hie","hy","sup","who","help","groceries"]

    # Applying bot logic
    if  user_msg in basics:
        if user_msg in ("hello","hie","hy","sup"):
            msg.body("""Hi there ! am window shopping bot. How may I help you? \n\n1. To find out about the shops available reply to this massege with 'shop' \n\n2. To find out about the product you want  reply to this massege with 'NAME OF PRODUCT'""")
        
        elif "who" in user_msg:
            msg.body('   I am being  created by Edward Ali and william Pharaoh ')
        
        elif "help" in user_msg:

            msg.body('help Line \n 1.Search for the product by typing the NAME of product \n 2.Type GROCERIES to get all the latest available products \n 3.Type HELP to go to the help line menu')
        
        elif "groceries" in user_msg:
             msg.body(dataStr())
     

    
    # filter user input
   
        
    elif user_msg not in basics:
        filtered_arr=[]
        splitText=user_msg.split()
        for X in splitText:
        # r = requests.get('https://windowshoppingserver.herokuapp.com/product/All')
            if X in mother:
                filtered_arr.extend([p for p in data1 if p['Name'] ==X])
        #data1 = r.json()
        if filtered_arr:
            print("filtered array is")
            print(filtered_arr)
            #sortedByPrice=filtered_arr.sort(key=lambda x: x["Quantity"], reverse=True)
            sortedByPrice=sorted(filtered_arr, key=lambda x: x['Price'], reverse=False)
            print("sorrted by price in ascending order")
            print(sortedByPrice)
            lowestThree=sortedByPrice[:3]
            print("lowest 3")
            print(lowestThree)

           
            
            #base_url = 'https://windowshoppingserver.herokuapp.com/product/All'
            firstThree = lowestThree
            # Printing firstThree
            datr = 'name     price       description     quantity        Shop\n\n'

            for product in firstThree:
                datr =datr+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
            
            msg.body(datr)


        elif not filtered_arr:
             msg.body("Sorry, I didn't get what you have said! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n")
   
       
       

    else:
        msg.body("Sorry, I didn't get what you have said! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product ")

    
    return str(bot_resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)