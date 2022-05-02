import os
from flask import Flask, request, session, json 
import requests
from twilio.twiml.messaging_response import MessagingResponse



SECRET_KEY = os.urandom(16)

## Init Flask APp
app = Flask(__name__)

# Function for geting all products
def dataStr():
    base_url = 'https://windowshoppingserver.herokuapp.com/product/All'
    data = requests.get(base_url).json()
    #structuring products in table format
    dat = 'name     price       description     quantity        Shop\n\n'

    #appending the products to the structured table format
    for product in data:
        dat =dat+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
        # print(dat)

    return dat

# Function for getting all registered shops 
def allshops():
    base_url = 'https://windowshoppingserver.herokuapp.com/shop/All'
    shop = requests.get(base_url).json()
    #structuring the shops in  table format 
    sho = 'name   location   phonenumber\n\n'

    #appending the shops to the structured table format for shops
    for s in shop:
        sho =sho+ f'{s["shopName"]}   {s["location"]}   {s["phoneNumber"]}\n'

    return sho

# shops and products
def productsbyShop():
    shop_url = 'https://windowshoppingserver.herokuapp.com/shop/All'
    shops = requests.get(shop_url).json()
    product_url = 'https://windowshoppingserver.herokuapp.com/product/All'
    productS = requests.get(product_url).json()

    if shops["shopName"] == productS["Shop"]:
        shopproducts = 'shopName \n\n'
        for pro in productS:
            allforshop = pro['Name']
            return allforshop


@app.route('/')

def index():
     return "window shoping whatsapp chatbot running"
@app.route('/bot', methods=['POST'])

#function getting user message and giving responses in the chatbot
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

    shop = requests.get('https://windowshoppingserver.herokuapp.com/shop/All').json()
    # print(r)
    data1 = r.json()

    # for an array shops
    shopMother =[]
    for Y in data1:
        shopName=Y['Shop']
        shopMother.append(shopName)


    # for an array for products
    mother=[]
    for X in data1:
            pname=X['Name']
            mother.append(pname)
        
    #An array for defined user messages
    basics=["hello","hie","hy","sup","who","help","groceries"]

    # Applying bot logic
    #Checking whether user message is in  the basics array
    if  user_msg in basics:
        if user_msg in ("hello","hie","hy","sup"):
            msg.body("""Hi there ! am window shopping bot. How may I help you? \n\n! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n 4. for help type 'help'""")
        #checking if who is in user message and giving its response
        elif "who" in user_msg:
            msg.body('   I am being  created by Edward Ali and william Pharaoh ')

        #checking if help is in user message and giving its response
        elif "help" in user_msg:

            msg.body('help Line \n You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n')
        
        # elif "groceries" in user_msg:
        #     msg.body(dataStr())
           

    ##checking whether shops is in user message and returning all shops 
    elif 'shops' in user_msg:

        msg.body(allshops())
    #Checking whether user message is not in basics array  
    # filter user input    
    elif user_msg not in basics:

         #An array for filtering shops
        filteredShop_arr=[]

        #  #An array for filtering products
        filtered_arr=[]
        splitText=user_msg.split()
        for X in splitText:
            #checking if product is in the array and appending to the list
            if X in mother:
                filtered_arr.extend([p for p in data1 if p['Name'] ==X])

            # #checking if shop is in the array and appending to the list
            elif X in shopMother:
                filteredShop_arr.extend([s for s in data1 if s['Shop'] ==X])
    
        if filtered_arr:

            # sorrted by price in ascending order
            sortedByPrice=sorted(filtered_arr, key=lambda x: x['Price'], reverse=False)
            
            # geting the lowest 3
            lowestThree=sortedByPrice[:3]
            firstThree = lowestThree

            # Printing firstThree
            datr = 'name     price       description     quantity        Shop\n\n'
            #appending the cheapest three products to the formatted table
            for product in firstThree:
                datr =datr+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
            
            msg.body(datr)

        
        ##checking if an array for shops is filtered 
        if filteredShop_arr:
            #stucturing the products in the shops in a table format
            dtr ='Name     quantity  price\n'
            #sorting the filtered  shop proudcts using shop name
            sortedShop=sorted(filteredShop_arr, key=lambda x: x['Shop'])
            #appending the sorted shop products to the structured table format
            for w in sortedShop:
        
                dtr = dtr +  f'{w["Name"]}       {w["Quantity"]}       {w["Price"]}\n'

            msg.body(dtr)
        




        #checking if an array is not filtered and giving its response
        elif not filtered_arr:
             msg.body("Sorry, what you are trying to find is not available \n\n ! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n 4. for help type 'help' ")

   
       
       

    else:
        msg.body("Sorry, I didn't get what you have said! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product ")

    
    return str(bot_resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)