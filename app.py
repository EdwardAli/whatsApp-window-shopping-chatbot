import os
from flask import Flask, request, session, json 
import requests
from twilio.twiml.messaging_response import MessagingResponse



SECRET_KEY = os.urandom(16)

## Init Flask APp
app = Flask(__name__)

# geting all products
def dataStr():
    base_url = 'https://windowshoppingserver.herokuapp.com/product/All'
    data = requests.get(base_url).json()
    
    dat = 'name     price       description     quantity        Shop\n\n'

    for product in data:
        dat =dat+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
        # print(dat)

    return dat

# getting all registered shops 
def allshops():
    base_url = 'https://windowshoppingserver.herokuapp.com/shop/All'
    shop = requests.get(base_url).json()
    sho = 'name   location   call\n\n'

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

    # for shops
    shopMother =[]
    for Y in data1:
        shopName=Y['Shop']
        shopMother.append(shopName)


    # for products
    mother=[]
    for X in data1:
            pname=X['Name']
            mother.append(pname)
        

    basics=["hello","hie","hy","sup","who","help","groceries"]

    # Applying bot logic
    if  user_msg in basics:
        if user_msg in ("hello","hie","hy","sup"):
            msg.body("""Hi there ! am window shopping bot. How may I help you? \n\n! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n 4. for help type 'help'""")
        
        elif "who" in user_msg:
            # print(productsbyShop())
            msg.body('   I am being  created by Edward Ali and william Pharaoh ')

        
        elif "help" in user_msg:

            msg.body('help Line \n ! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n')
        
        # elif "groceries" in user_msg:
        #     msg.body(dataStr())
           

   # geting all shops
    elif 'shops' in user_msg:

        msg.body(allshops())
     
    # filter user input
   
        
    elif user_msg not in basics:

        # checking if the shop name is in user massage
        filteredShop_arr=[]

        # checking if the product name is in user massage
        filtered_arr=[]
        splitText=user_msg.split()
        for X in splitText:

            if X in mother:
                
                filtered_arr.extend([p for p in data1 if p['Name'] ==X])

            # for shop
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

            for product in firstThree:
                datr =datr+ f'{product["Name"]}       {product["Price"]}        {product["Description"]}      {product["Quantity"]}        {product["Shop"]}\n'
            
            msg.body(datr)

        
        # for shop 
        
        if filteredShop_arr:
            dtr ='Name     quantity  price\n'

            sortedShop=sorted(filteredShop_arr, key=lambda x: x['Shop'])
            
            for w in sortedShop:
        
                dtr = dtr +  f'{w["Name"]}       {w["Quantity"]}       {w["Price"]}\n'

            msg.body(dtr)
        

                # checking products for a given shop


           
            
            # print("filteredshop array is")
            # print(sortedShop)
            

            # print("p name on shop")
            # print(shopMother)




        elif not filtered_arr:
             msg.body("Sorry, what you are trying to find is not available \n\n ! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product\n 3. type shop name to access products in that shop\n 4. for help type 'help' ")

   
       
       

    else:
        msg.body("Sorry, I didn't get what you have said! You can access the following services.\n 1.Available shops typing shops.\n 2.Available product by typing name of the product ")

    
    return str(bot_resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)