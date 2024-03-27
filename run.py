import getpass
import login
import datetime
from Database import Database

def main():
    username = input("Username: ")
    password = getpass.getpass()
    login_result = login.check_credentials(username, password)

    if(login_result[0] == True):
        user_id = login_result[3]
        user = login_result[1]
        user_type = login_result[2]
        if(user_type == "admin"):
            while(True):
                print(f"Welcome {user} to kirane ka Dukan and you are {user_type}")
                print("----Please Select the Options for Operations------")
                print("\t1. view all Products")
                print("\t2. view Categories")
                print("\t3. insert Products")
                print("\t4. Update Product")
                print("\t5. Delete Product")
                print("\t6. to EXIT")

                inp = input("\nEnter your choice:")
                print()

                if(inp == "6"):
                    print("EXITTING..... Thank you")
                    break

                elif(inp == "3"):
                    try:
                        category_id = int(input("Enter Category ID: "))
                        product_name = input("Enter Product Name: ")
                        product_desc = input("Enter the Description of thre Product: ")
                        unit_price = float(input("ENter the Unit Price: "))
                        availibility = int(input("Enter the availibility"))
                        db = Database()
                        db.insert("products", category_id=category_id, product_name=product_name, 
                            product_desc=product_desc, unit_price=unit_price, 
                            availibility=availibility
                            )
                    except Exception as e:
                        print(e)

                elif(inp == "2"):
                    db = Database()
                    results = db.retrieve("categories")
                    print(f"\tcategory_ID | category_name")
                    for row in results:
                        print(f"\t{row[0]}      | {row[1]}")
                
                elif(inp=="1"):
                    db=Database()
                    products=db.retrieve("products")
                    #print(products)
                    print(f"\tproduct_id | category_id |     product_name     |   desc    |   price   | stock")
                    for row in products:
                        print(f"\t{row[0]}       | {row[1]}        | {row[2]}   | {row[3]}   | {row[4]}   | {row[5]}   ")

                elif(inp == "4"):
                    try:
                        db = Database()
                        products=db.retrieve("products")
                        #print(products)
                        print(f"\tproduct_id | category_id |     product_name     |      desc      |   price   | stock")
                        for row in products:
                            print(f"\t{row[0]}       | {row[1]}        |      {row[2]}   |   {row[3]}   | {row[4]}   | {row[5]}   ")

                        prod_id = int(input("Enter Product ID: "))
                        print("\t1. For new Stock")
                        print("\t2. For new Price")
                        print("\t3. For Both")

                        choice = input("Enter choice: ")

                        if(choice == "1"):
                            stock = int(input("Enter the new Stock: "))
                            db.update("products", f"product_id={prod_id}", availibility=stock)
                            continue
                        elif(choice == "2"):
                            price = float(input("Entr New Price: "))
                            db.update("products", f"product_id={prod_id}", unit_price=price)
                            continue
                        elif(choice == "3"):
                            stock = int(input("Enter the new Stock: "))
                            price = float(input("Entr New Price: "))
                            db.update("products", f"product_id={prod_id}", unit_price=price, availibility=stock)
                            continue
                        else:
                            print("Bad Choice..")
                    except Exception as e:
                        print(e)
                elif(inp=="5"):
                    try:
                        db = Database()
                        products=db.retrieve("products")
                        #print(products)
                        print(f"\tproduct_id | category_id |     product_name     |      desc      |   price   | stock")
                        for row in products:
                            print(f"\t{row[0]}       | {row[1]}        |      {row[2]}   |   {row[3]}   | {row[4]}   | {row[5]}   ")
                        
                        prod_id = int(input("Enter Product ID: "))
                        db.delete("products",clause=f"product_id={prod_id}")
                        continue                       
                    except Exception as e:
                        print(e)                   

            
        elif(user_type == "customer"):
            cart = {}
            while(True):
                print(f"Welcome {user} to kirane ka Dukan and you are {user_type}, a Valuable Customer")
                print("----Please Select the Options for Operations------")
                print("\t1. view Products Stock")
                print("\t2. view Categories")
                print("\t3. Select Product")
                print("\t4. Buy Selected Product")
                #print("\t5. view Orders")
                print("\t5. to EXIT")


                inp = input("\nEnter your choice:")
                print()
                if(inp == "5"):
                    print("EXITTING..... Thank you")
                    break
                elif(inp=="1"):
                    db=Database()
                    products=db.retrieve("products")
                    #print(products)
                    print(f"\tproduct_id | category_id |     product_name     |   description     |   price   | stock")
                    for row in products:
                        print(f"\t{row[0]}       | {row[1]}        | {row[2]}   | {row[3]}   | {row[4]}   | {row[5]}   ")
                elif(inp=="2"):
                    db = Database()
                    results = db.retrieve("categories")
                    print(f"\tcategory_ID | category_name")
                    for row in results:
                        print(f"\t{row[0]}      | {row[1]}")
                elif(inp=="3"):
                    db=Database()
                    products=db.retrieve("products")
                    #print(products)
                    print(f"\tproduct_id | category_id |     product_name     |   description     |   price   | stock")
                    for row in products:
                        print(f"\t{row[0]}       | {row[1]}        | {row[2]}   | {row[3]}   | {row[4]}   | {row[5]}   ")

                    print("Select the Product from ID: ")
                    while(True):
                        product_id = int(input("Enter ID: "))
                        if product_id not in cart:
                            cart[product_id] = 1
                        else:
                            cart[product_id] +=1

                        print("do you want to enter more y/n: ")
                        C = input()
                        if(C == 'Y' or C == 'y'):
                            continue
                        else:
                            break

                    print("your Cart is: ")    
                    try:
                        total_cart = []
                        for prod_id,count in cart.items():
                            con = db.connect()
                            cursor = con.cursor()
                            SQL = f"SELECT product_id, product_name, unit_price, abs({count}) as num_items, {count}*unit_price as total_price  FROM products WHERE product_id ={prod_id}"
                            cursor.execute(SQL)
                            results = cursor.fetchall()
                            for row in results:
                                total_cart.append(row)
                        
                        print(f"\tproduct_id | product_name |   unit_price    |  num_items  |   total_price  |")
                        for row in total_cart:
                            print(f"\t{row[0]}     | {row[1]}      | {row[2]}   | {row[3]}   | {row[4]}   | ")
                    except Exception as e:
                        print(f"EXCEPTION OCCOURED: {e}")
                    finally:
                        con.close()
                        cursor.close()
                
                elif(inp == "4"):
                    print("your Cart is: ")    
                    db = Database()
                    total_price = 0
                    try:
                        total_cart = []
                        for prod_id,count in cart.items():
                            con = db.connect()
                            cursor = con.cursor()
                            SQL = f"SELECT product_id, product_name, unit_price, abs({count}) as num_items, {count}*unit_price as total_price  FROM products WHERE product_id ={prod_id}"
                            cursor.execute(SQL)
                            results = cursor.fetchall()
                            for row in results:
                                total_cart.append(row)
                        
                        print(f"\tproduct_id | product_name |   unit_price    |  num_items  |   total_price  |")
                        for row in total_cart:
                            total_price +=row[4]
                            print(f"\t{row[0]}     | {row[1]}      | {row[2]}   | {row[3]}   | {row[4]}   | ")
                    except Exception as e:
                        print(f"EXCEPTION OCCOURED: {e}")
                    finally:
                        con.close()
                        cursor.close()

                    print(f"The total Price is {total_price} .")
                    print("Do you wish to buy y/n : ")
                    C = input()
                    if(C == 'Y' or C == 'y'):
                        db = Database()
                        today = datetime.datetime.now()
                        date_now = str(today).split()[0]
                        db.insert("orders",user_id = user_id, order_date=date_now, fulfilled='yes', cancled='no', paid_ammount=total_price )
                        
                        last_id = db.run_query("SELECT max(order_id) FROM orders")
                        for row in total_cart:
                            db.insert("orders_details", order_id=last_id[0][0], product_id=row[0], price=row[2], quantity=row[3], discount=0, total=row[2]* row[3] )
                            stock = db.run_query(f"SELECT availibility FROM products WHERE product_id={row[0]}")
                            db.update("products",id=f"product_id={row[0]}", availibility=stock[0][0] - row[3])

                        print("Order Completed Sucessfully..")
                    else:
                        pass
    
    else:
        print("LOGIN FAILED...!!!")
        exit()


if __name__ == "__main__":
    main()