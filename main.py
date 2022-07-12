# Author nadimnesar 24.06.2022

import mysql.connector as sql_connect  # Must Install this module library

try:
    projectDB = sql_connect.connect(host='localhost', user='root', password='')
except:
    print("Please Open XAMPP then start Apache and mySQL!")
    exit()

sqlCMD = projectDB.cursor()

# Creating & Connecting Database
try:
    sqlCMD.execute("CREATE DATABASE bankmsys")
except:
    pass
finally:
    projectDB.connect(database='bankmsys')


# Checking Database Is Connected Or Not
if projectDB.is_connected():
    pass
else:
    print("Database Not Connected, Please Recheck All.\n")
    exit()


# Creating User Info Table
try:
    sqlCMD.execute("CREATE TABLE userInfo(Account_Number INT(20) PRIMARY KEY, Name VARCHAR(20), Age INT(20), "
                   "Address VARCHAR(20), Phone VARCHAR(20), Gender VARCHAR(10));")
except:
    pass


# Creating Admin Info Table
try:
    sqlCMD.execute("CREATE TABLE adminInfo(Account_Number INT(20) PRIMARY KEY, Balance FLOAT(50), Account_Type "
                   "VARCHAR(50), Username VARCHAR(20), Password VARCHAR(20));")
except:
    pass


adminUsername = "Admin"
adminPassword = "12345"
customerAccountNumber = None


def user_check_info():
    print("\nYour Account Information")
    sql = "SELECT * FROM `userinfo` WHERE Account_Number = %s;"
    val = [customerAccountNumber]
    sqlCMD.execute(sql, val)
    res = sqlCMD.fetchall()

    print("Account Number:", res[0][0])
    print("Name:", res[0][1])
    print("Age:", res[0][2])
    print("Address:", res[0][3])
    print("Phone:", res[0][4])
    print("Gender:", res[0][5])


def user_edit_info():
    while True:
        print("\nEdit Your Information")
        print("1. Name")
        print("2. Age")
        print("3. Address")
        print("4. Phone")
        print("5. Gender")
        print("6. Exit")
        option = int(input("Enter Type (1 to 6): "))
        if option == 1:
            Name = str(input("\nEnter New Name: "))

            sql = "UPDATE `userinfo` SET `Name`= %s WHERE Account_Number = %s;"
            val = [Name, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()
            print("Updated!")
        elif option == 2:
            Age = int(input("\nEnter New Age: "))

            sql = "UPDATE `userinfo` SET `Age`= %s WHERE Account_Number = %s;"
            val = [Age, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()
            print("Updated!")
        elif option == 3:
            Address = str(input("\nEnter New Address: "))

            sql = "UPDATE `userinfo` SET `Address`= %s WHERE Account_Number = %s;"
            val = [Address, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()
            print("Updated!")
        elif option == 4:
            Phone = str(input("\nEnter New Phone: "))

            sql = "UPDATE `userinfo` SET `Phone`= %s WHERE Account_Number = %s;"
            val = [Phone, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()
            print("Updated!")
        elif option == 5:
            Gender = str(input("\nEnter New Gender: "))

            sql = "UPDATE `userinfo` SET `Gender`= %s WHERE Account_Number = %s;"
            val = [Gender, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()
            print("Updated!")
        elif option == 6:
            break
        else:
            print("Wrong Input!")


def user_check_balance():
    sql = "SELECT Balance FROM `admininfo` WHERE Account_Number = %s;"
    val = [customerAccountNumber]
    sqlCMD.execute(sql, val)
    res = sqlCMD.fetchall()
    print("\nYour Balance is", res[0][0], "BDT")


def user_deposit():
    amount = float(input("\nEnter Amount You Want to Deposit: "))
    sql = "SELECT Balance FROM `admininfo` WHERE Account_Number = %s;"
    val = [customerAccountNumber]
    sqlCMD.execute(sql, val)
    res = sqlCMD.fetchall()
    new_balance = res[0][0] + amount

    sql = "UPDATE `admininfo` SET `Balance`= %s WHERE Account_Number = %s;"
    val = [new_balance, customerAccountNumber]
    sqlCMD.execute(sql, val)
    projectDB.commit()
    print("Deposit Done!")


def user_withdraw():
    amount = float(input("\nEnter Amount You Want to Withdraw: "))
    sql = "SELECT Balance FROM `admininfo` WHERE Account_Number = %s;"
    val = [customerAccountNumber]
    sqlCMD.execute(sql, val)
    res = sqlCMD.fetchall()
    new_balance = res[0][0] - amount

    if new_balance < 0:
        print("Insufficient Balance")
    else:
        sql = "UPDATE `admininfo` SET `Balance`= %s WHERE Account_Number = %s;"
        val = [new_balance, customerAccountNumber]
        sqlCMD.execute(sql, val)
        projectDB.commit()
        print("Withdraw Done!")


def user_transfer():
    acc_num = str(input("\nEnter Account Number Which You Want to Transfer Money: "))
    sql = "SELECT Account_Number FROM `userinfo` WHERE Account_Number = %s;"
    val = [acc_num]
    sqlCMD.execute(sql, val)

    res = sqlCMD.fetchall()
    if len(res) == 1:
        amount = float(input("\nEnter Amount You Want to Transfer: "))

        sql = "SELECT Balance FROM `admininfo` WHERE Account_Number = %s;"
        val = [customerAccountNumber]
        sqlCMD.execute(sql, val)
        res = sqlCMD.fetchall()
        b_from = res[0][0] - amount

        if b_from < 0:
            print("Insufficient Balance")
        else:
            sql = "SELECT Balance FROM `admininfo` WHERE Account_Number = %s;"
            val = [acc_num]
            sqlCMD.execute(sql, val)
            res = sqlCMD.fetchall()
            b_to = res[0][0] + amount

            sql = "UPDATE `admininfo` SET `Balance`= %s WHERE Account_Number = %s;"
            val = [b_from, customerAccountNumber]
            sqlCMD.execute(sql, val)
            projectDB.commit()

            sql = "UPDATE `admininfo` SET `Balance`= %s WHERE Account_Number = %s;"
            val = [b_to, acc_num]
            sqlCMD.execute(sql, val)
            projectDB.commit()

            print("\nSuccessfully Transfer")
    else:
        print("Wrong Account Number, Try Again Later!")


def user_delete():
    sql = "DELETE FROM `admininfo` WHERE Account_Number = %s;"
    val = [customerAccountNumber]
    sqlCMD.execute(sql, val)
    sql = "DELETE FROM `userinfo` WHERE Account_Number = %s;"
    sqlCMD.execute(sql, val)
    projectDB.commit()
    print("\nSuccessfully Deleted")
    main()


def user():
    while True:
        print("\nWelcome to User Panel")
        print("1. Check Own Information")
        print("2. Edit")
        print("3. Check Balance")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Transfer")
        print("7. Delete")
        print("8. Exit")
        option = int(input("Enter Type (1 to 8): "))
        if option == 1:
            user_check_info()
        elif option == 2:
            user_edit_info()
        elif option == 3:
            user_check_balance()
        elif option == 4:
            user_deposit()
        elif option == 5:
            user_withdraw()
        elif option == 6:
            user_transfer()
        elif option == 7:
            user_delete()
        elif option == 8:
            break
        else:
            print("Wrong Input!")


def admin_all_info():
    sqlCMD.execute("SELECT * FROM userinfo NATURAL JOIN admininfo;")
    res = sqlCMD.fetchall()
    cnt = 0
    for idx in res:
        cnt += 1
        print("\nUser No.", cnt)
        print("Account Number:", idx[0])
        print("Name:", idx[1])
        print("Age:", idx[2])
        print("Address:", idx[3])
        print("Phone:", idx[4])
        print("Gender:", idx[5])
        print("Balance:", idx[6])
        print("Account Type:", idx[7])
        print("Username:", idx[8])
        print("Password:", idx[9])


def admin_search_info():
    while True:
        print("\nSearch User Information By")
        print("1. Account Number")
        print("2. Age Range")
        print("3. Address")
        print("4. Gender")
        print("5. Exit")
        option = int(input("Enter Type (1 to 5): "))
        if option == 1:
            acc_num = str(input("\nEnter Account Number: "))

            sql = "SELECT * FROM userinfo NATURAL JOIN admininfo WHERE Account_Number = %s;"
            val = [acc_num]
            sqlCMD.execute(sql, val)
            res = sqlCMD.fetchall()

            if len(res) == 1:
                idx = res[0]
                print("\nAccount Number:", idx[0])
                print("Name:", idx[1])
                print("Age:", idx[2])
                print("Address:", idx[3])
                print("Phone:", idx[4])
                print("Gender:", idx[5])
                print("Balance:", idx[6])
                print("Account Type:", idx[7])
                print("Username:", idx[8])
                print("Password:", idx[9])
            else:
                print("Wrong Account Number, Try Again Later!")
        elif option == 2:
            min_age = int(input("\nEnter Min Age: "))
            max_age = int(input("Enter Max Age: "))

            sql = "SELECT * FROM userinfo NATURAL JOIN admininfo WHERE age >= %s AND age <= %s;"
            val = [min_age, max_age]
            sqlCMD.execute(sql, val)
            res = sqlCMD.fetchall()

            if len(res) >= 1:
                cnt = 0
                for idx in res:
                    cnt += 1
                    print("\nUser No.", cnt)
                    print("Account Number:", idx[0])
                    print("Name:", idx[1])
                    print("Age:", idx[2])
                    print("Address:", idx[3])
                    print("Phone:", idx[4])
                    print("Gender:", idx[5])
                    print("Balance:", idx[6])
                    print("Account Type:", idx[7])
                    print("Username:", idx[8])
                    print("Password:", idx[9])
            else:
                print("No One in This Range!")
        elif option == 3:
            address = str(input("\nEnter Address: "))
            address = "%" + address
            address = address + "%"

            sql = "SELECT * FROM userinfo NATURAL JOIN admininfo WHERE userinfo.Address LIKE %s;"
            val = [address]
            sqlCMD.execute(sql, val)
            res = sqlCMD.fetchall()

            if len(res) >= 1:
                cnt = 0
                for idx in res:
                    cnt += 1
                    print("\nUser No.", cnt)
                    print("Account Number:", idx[0])
                    print("Name:", idx[1])
                    print("Age:", idx[2])
                    print("Address:", idx[3])
                    print("Phone:", idx[4])
                    print("Gender:", idx[5])
                    print("Balance:", idx[6])
                    print("Account Type:", idx[7])
                    print("Username:", idx[8])
                    print("Password:", idx[9])
            else:
                print("No One from this Address!")
        elif option == 4:
            Gender = str(input("\nEnter Gender: "))

            sql = "SELECT * FROM userinfo NATURAL JOIN admininfo WHERE userinfo.Gender = %s;"
            val = [Gender]
            sqlCMD.execute(sql, val)
            res = sqlCMD.fetchall()

            if len(res) >= 1:
                cnt = 0
                for idx in res:
                    cnt += 1
                    print("\nUser No.", cnt)
                    print("Account Number:", idx[0])
                    print("Name:", idx[1])
                    print("Age:", idx[2])
                    print("Address:", idx[3])
                    print("Phone:", idx[4])
                    print("Gender:", idx[5])
                    print("Balance:", idx[6])
                    print("Account Type:", idx[7])
                    print("Username:", idx[8])
                    print("Password:", idx[9])
            else:
                print("No One from this gender!")
        elif option == 5:
            break
        else:
            print("Wrong Input!")


def admin_total_balance():
    sqlCMD.execute("SELECT Sum(Balance) FROM `admininfo`;")
    res = sqlCMD.fetchall()
    print("\nTotal Balance:", res[0][0])


def admin_average():
    sqlCMD.execute("SELECT AVG(Balance) FROM `admininfo`;")
    res = sqlCMD.fetchall()
    print("\nAverage Balance:", res[0][0])


def admin_frequency():
    sqlCMD.execute("SELECT COUNT(Account_Type), Account_Type FROM admininfo GROUP BY Account_Type;")
    res = sqlCMD.fetchall()
    print("\nCount     Account Type")
    for idx in res:
        print(idx[0], "       ", idx[1])


def admin_sort():
    sqlCMD.execute("SELECT * FROM userinfo NATURAL JOIN admininfo ORDER BY (admininfo.Balance) ASC;")
    res = sqlCMD.fetchall()
    cnt = 0
    for idx in res:
        cnt += 1
        print("\nUser No.", cnt)
        print("Account Number:", idx[0])
        print("Name:", idx[1])
        print("Age:", idx[2])
        print("Address:", idx[3])
        print("Phone:", idx[4])
        print("Gender:", idx[5])
        print("Balance:", idx[6])
        print("Account Type:", idx[7])
        print("Username:", idx[8])
        print("Password:", idx[9])


def admin():
    while True:
        print("\nWelcome to Admin Panel")
        print("1. Show All Information")
        print("2. Search A User Information")
        print("3. Total Balance")
        print("4. Average Balance")
        print("5. Check Frequency of Accounts by Type")
        print("6. Check All Account By Balance Sorted Increasing Order")
        print("7. Exit")
        option = int(input("Enter Type (1 to 7): "))
        if option == 1:
            admin_all_info()
        elif option == 2:
            admin_search_info()
        elif option == 3:
            admin_total_balance()
        elif option == 4:
            admin_average()
        elif option == 5:
            admin_frequency()
        elif option == 6:
            admin_sort()
        elif option == 7:
            break
        else:
            print("Wrong Input!")


def user_input():
    while True:
        print("\nUser Login/SignUp")
        print("1. Login")
        print("2. SignUp")
        print("3. Exit")
        option = int(input("Enter Type (1 or 2 or 3): "))
        if option == 1:
            print("\nUser Login")
            username = str(input("Enter User Username: "))
            password = str(input("Enter User Password: "))

            sql = "SELECT Account_Number FROM `admininfo` WHERE (Username = %s) AND (Password = %s);"
            val = (username, password)
            sqlCMD.execute(sql, val)

            res = sqlCMD.fetchall()
            if len(res) == 1:
                print("\nSuccessfully Login")
                global customerAccountNumber
                customerAccountNumber = res[0][0]
                user()
                break
            else:
                print("Wrong Username or Password, Please Try Again Later!")
        elif option == 2:
            print("\nUser SignUp")
            Username = str(input("Username: "))
            Password = str(input("Password: "))
            Name = str(input("Name: "))
            Gender = str(input("Gender: "))
            Age = int(input("Age: "))
            Address = str(input("Address: "))
            Phone = str(input("Phone: "))
            AccountType = str(input("Account Type (Savings/Student/Business): "))
            Initialbalance = float(input("Initial Deposit (min. 500.00 BDT): "))
            AccountNumber = 1001

            sqlCMD.execute("SELECT MAX(Account_Number) FROM `userinfo`;")
            res = sqlCMD.fetchall()
            if res[0][0] == None:
                pass
            else:
                AccountNumber = res[0][0] + 1

            sql = "INSERT INTO `userinfo`(`Account_Number`, `Name`, `Age`, `Address`, `Phone`, `Gender`) VALUES (%s, " \
                  "%s, %s, %s, %s, %s);"
            val = [AccountNumber, Name, Age, Address, Phone, Gender]
            sqlCMD.execute(sql, val)
            projectDB.commit()

            sql = "INSERT INTO `admininfo`(`Account_Number`, `Balance`, `Account_Type`, `Username`, `Password`) " \
                  "VALUES (%s, %s, %s, %s, %s);"
            val = (AccountNumber, Initialbalance, AccountType, Username, Password)
            sqlCMD.execute(sql, val)
            projectDB.commit()

            print("\nSuccessfully Created Account")
        elif option == 3:
            break
        else:
            print("Wrong Input!")


def admin_input():
    while True:
        print("\nAdmin Login")
        username = input("Enter Admin Username: ")
        password = input("Enter Admin Password: ")
        if username == adminUsername and password == adminPassword:
            print("Login Successful")
            admin()
            break
        else:
            print("Wrong Username or Password, Please Try Again Later!")


def insert_random_value():
    try:
        sql = "INSERT INTO `userinfo`(`Account_Number`, `Name`, `Age`, `Address`, `Phone`, `Gender`) VALUES (%s, %s, %s, %s, %s, %s);"
        val = [
            ('1001', 'Nesar Ahmed', '21', 'Khilgaon', '01628871060', 'Male'),
            ('1002', 'Farhin Khaled', '22', 'Jatrabari', '01921261473', 'Female'),
            ('1003', 'Sayed Hasan', '21', 'Dhanmondi', '01711892303', 'Male'),
            ('1004', 'Md. Rakib', '21', 'Zigatola', '01711119475', 'Male'),
            ('1005', 'Musfiqur Sohidul', '20', 'Kolabagan', '01711155024', 'Male'),
            ('1006', 'Minhajul Islam', '22', 'Cumilla', '01711828122', 'Male'),
            ('1007', 'FI Nabil', '22', 'Asulia', '01818676657', 'Male'),
            ('1008', 'Nabid Anzum Akash', '21', 'DSC', '01713008868', 'Male'),
            ('1009', 'Jahirul Islam', '23', 'Khilgaon', '01711194474', 'Male'),
            ('1010', 'Ariful Hauqe', '21', 'Farmgate', '01712187524', 'Male')
        ]
        sqlCMD.executemany(sql, val)
        projectDB.commit()
        sql = "INSERT INTO `admininfo`(`Account_Number`, `Balance`, `Account_Type`, `Username`, `Password`) VALUES (%s, %s, %s, %s, %s);"
        val = [
            ('1001', '500', 'Student', 'nadimnesar', '12345'),
            ('1002', '500', 'Savings', 'farhin567', '12345'),
            ('1003', '500', 'Business', 'sayedhasan', '12345'),
            ('1004', '500', 'Savings', 'mdrakib', '12345'),
            ('1005', '500', 'Business', 'musfiqur', '12345'),
            ('1006', '500', 'Savings', 'minhajul', '12345'),
            ('1007', '500', 'Savings', 'finabil', '12345'),
            ('1008', '500', 'Savings', 'nabid', '12345'),
            ('1009', '500', 'Business', 'jahirul', '12345'),
            ('1010', '500', 'Savings', 'ariful', '12345')
        ]
        sqlCMD.executemany(sql, val)
        projectDB.commit()
    except:
        pass


def main():
    while True:
        print("\nBank Management System")
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        option = int(input("Enter Type (1 or 2 or 3): "))
        if option == 1:
            user_input()
            break
        elif option == 2:
            admin_input()
            break
        elif option == 3:
            break
        else:
            print("Wrong Input!")


insert_random_value()
main()
sqlCMD.close()
projectDB.disconnect()

# All rights reserved by Nesar Ahmed @2022
