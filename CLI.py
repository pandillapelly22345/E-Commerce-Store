# Pandillapelly Harshvardhini - 2022345
import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='password'
)

cursor = mydb.cursor()
cursor.execute("use online_store")
print(cursor.fetchall())

def adminUtility():
    while(True):
        print("1. Get Total Sales Per Category")
        print("2. Retrive Top 5 Customer who spent most money on their orders")
        print("3. Add new product into product table")
        print("4. EXIT")
        choice=input("Enter The option: ")
        if(choice=="1"):
            cursor.execute("""SELECT c.category_name, SUM(o.total_amount) AS total_sales FROM orders o JOIN order_item oi ON o.order_id = oi.order_id1 
                              JOIN products p ON oi.product_id1 = p.product_id JOIN category c ON p.category_id1 = c.category_id GROUP BY c.category_name;""")
            for data in cursor.fetchall():
                print("------------------------")
                print("Category Name: ",data[0])
                print("Total Sales: ",data[1])
                print("------------------------")
        elif(choice=="2"):
            cursor.execute("""SELECT c.customer_id, c.first_name, c.last_name, SUM(o.total_amount) AS total_spent FROM customer c 
                           JOIN orders o ON c.customer_id = o.customer_id1 GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_spent DESC LIMIT 5;""")
            for data in cursor.fetchall():
                print("------------------------")
                print("Customer ID: ",data[0])
                print("Customer Name: ",data[1],data[2])
                print("Total Spending: ",data[3])
                print("------------------------")

        elif(choice == "3"):
            product_name = input("Enter product name: ")
            product_description = input("Enter product description: ")
            price = float(input("Enter product price: "))
            stock = float(input("Enter product stock: "))
            discount = float(input("Enter product discount: "))
            category_id = int(input("Enter category ID: "))
            admin_id = int(input("Enter admin ID: "))

            # Insert the new product into the product table
            cursor.execute("""INSERT INTO products (product_name, p_description, price, stock, discount, category_id1, admin_id4)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (product_name, product_description, price, stock, discount, category_id, admin_id))
            mydb.commit()
            print("New product added successfully!")

        elif(choice=="4"):
            print("Going Back.....")
            return
        else:
            print("Wrong Option!!!!")

def customerUtility():
    print()
    print("Login successful as customer.")
    while(True):
        print("1. Show my orders")
        print("2. Select category Category and show its coresponding products")
        print("3. Order an item")
        print("4. Add product to cart")
        print("5. Delete product from cart")
        print("6. EXIT")
        x = (input("Enter your choice: "))
        if x=="1":
            customer_id = result[1]
            print("customer_id: ", customer_id)
            cmd="""SELECT * FROM orders
            WHERE customer_id1='{0}'""".format(customer_id)
            cursor.execute(cmd)
            for i in cursor.fetchall():
                data=i
                for item in range(len(data)):
                    if(item ==0):
                        print("Order ID: ",data[item])
                    if(item==1):
                        print("Order status: ",data[item])
                    if(item==2):
                        print("Order Date: ",data[item].strftime("%Y-%m-%d"))
    
        elif x=="2":
            cmd = """ SELECT * from Category"""
            cursor.execute(cmd)
            for i in cursor.fetchall():
                print("category_id: " , i[0] , " category_name: ", i[2])

            print("enter the category_id you want to go in: ")
            category_id = int(input())
            cmd1 = """SELECT * from products where category_id1 = '{0}'""".format(category_id)
            cursor.execute(cmd1)
            for data in cursor.fetchall():
                print("--------------------------------")
                item=data
                for i in range(len(item)):
                    if(i==0):
                        print("Product ID: ",item[i])
                    if(i==1):
                        print("Product Name: ",item[i])
                    if(i==3):
                        print("Product Price: ",item[i])
                print("--------------------------------")


        elif x=="3":
            product_id = int(input("Enter product id you want to buy: "))
            quantity = int(input("Enter quantity: "))

            cmd2 = "SELECT stock FROM products WHERE product_id = %s"
            cursor.execute(cmd2,(product_id,))
            result1 = cursor.fetchone()
            if result1 is None:
                print("Product does not exist.")
            elif quantity > result1[0]:
                print("Insufficient stock.")

            else:
                customer_id2 = result[1]
                cmd3 = """INSERT INTO orders (house_no1, street1, city1, order_status, order_date, customer_id1)
                    SELECT house_no, street, city, 'ordered', NOW(), %s
                    FROM customer
                    WHERE customer_id = %s"""
                cursor.execute(cmd3, (customer_id2, customer_id2))

                mydb.commit()
                order_id = cursor.lastrowid

                cmd5 = """SELECT price FROM products WHERE product_id = %s"""
                cursor.execute(cmd5, (product_id,))
                result2 = cursor.fetchone()

                if result2 is None:
                    print("Product not found.")
                else:
                    product_price = result2[0]  # Extracting the price from the result
                    total_price = product_price * quantity

                    cmd4 = """INSERT INTO order_item (quantity, price, order_id1, product_id1)
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(cmd4, (quantity, total_price, order_id, product_id))

                    mydb.commit()

                    print("Order placed sucessfully!!!!")
        
        elif x=="4":
            product_id = int(input("Enter product id you want to add to cart: "))
            quantity = int(input("Enter quantity: "))

            cmd_check_product = "SELECT stock FROM products WHERE product_id = %s"
            cursor.execute(cmd_check_product, (product_id,))
            result_product = cursor.fetchone()

            if result_product is None:
                print("Product does not exist.")
            elif quantity > result_product[0]:
                print("Insufficient stock.")
            else:
                customer_id2 = result[1]

                cmd_insert_cart = """INSERT INTO cart_items (cart_id1, product_id1, quantity)
                                      SELECT cart_id, %s, %s
                                    FROM cart
                                    WHERE customer_id3 = %s"""
                cursor.execute(cmd_insert_cart, (product_id, quantity, customer_id2))
                mydb.commit()
                print("Product added to cart successfully!")


        elif x=="5":
            product_id = int(input("Enter product id you want to delete from cart: "))

            # Get customer ID
            customer_id2 = result[1]

            # Delete product from cart
            cmd_delete_cart = """DELETE FROM cart_items
                                WHERE product_id1 = %s
                                AND cart_id1 IN (SELECT cart_id FROM cart WHERE customer_id3 = %s)"""
            cursor.execute(cmd_delete_cart, (product_id, customer_id2))
            mydb.commit()
            print("Product deleted from cart successfully!")

        elif x=="6":
            print("Going Back......")
            return
        else:
            print("Wrong Option!!!!!")


while True:
    print("1. Enter as admin")
    print("2. Enter as customer")
    print("3. Login as customer")
    print("4. Exit")
    a = (input("Enter the Option: "))
    if a=="1":
        admin_name = input("enter your name: ")
        cmd = """SELECT * FROM adminn
            WHERE namee = '{0}'""".format(admin_name)
        cursor.execute(cmd)
        result = cursor.fetchone()
        if result:
            print("Login successful as admin........")
            adminUtility()
        else:
            print("Invalid admin credentials!!!!!")

    elif a == "2":
        customer_login_id = input("Enter your login id: ")
        password = input("Enter your password: ")
        cmd = """SELECT * FROM authenticationn
            WHERE login_id = '{0}' AND password1 = '{1}'""".format(customer_login_id, password)
        cursor.execute(cmd)
        result = cursor.fetchone()
        if result:
            customerUtility()
        else:
            print("Invalid customer credentials.")

    elif a == "3":
        print("Enter your name: ")
        first_name = input("First Name: ")
        last_name = input("Last Name (Press Enter if not applicable): ")
        email_id = input("Enter your email_id: ")
        gender = input("Enter your gender: ")
        phone_number = input("Enter your phone number: ")
        house_no = input("Enter your house number: ")
        street = input("Enter your street: ")
        city = input("Enter your city: ")
        country = input("Enter your country: ")
        pincode = input("Enter your pincode: ")

        subscription_status = "NO"

        cmd_insert_customer = """
            INSERT INTO customer (first_name, last_name, email_id, gender, phone_number, house_no,
                              street, city, country, pincode, subscription_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        customer_values = (first_name, last_name, email_id, gender, phone_number, house_no, street,
                       city, country, pincode, subscription_status)
        cursor.execute(cmd_insert_customer, customer_values)
        mydb.commit()

        print("---------------------------------")
        print("Enter your Authentication!!!!!")
        customer_id = cursor.lastrowid
        login_id = input("Enter your login ID(email id that you entered while registering): ")
        password = input("Create password: ")

        cmd_insert_authentication = """INSERT INTO authenticationn (login_id, customer_id2, password1)
                                   VALUES (%s, %s, %s)"""
        authentication_data = (login_id, customer_id, password)
        cursor.execute(cmd_insert_authentication, authentication_data)
        mydb.commit()

        print("Customer signed up successfully.")


    elif a=="4":
        print("Exiting.......")
    else:
        print("Wrong Option")