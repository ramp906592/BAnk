import json
import random
import string
from pathlib import Path

class BANK:
    database = 'data.json'
    data = []  # here we kept all the data

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("file doesn't exist!")
    except Exception as err:
        print(f"An exception occurred: {err}")  



    @classmethod
    def __update(cls): 
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(BANK.data))
            
            
            
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k=3)
        num = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%^&*",k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
        


    def CreateAccount(self):
        info = {  # make a dictionary to save the data and their key values 
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "pin": int(input("Enter your 4-digit PIN: ")),
            "accountNo": BANK.__accountgenerate(),
            "balance": 0
        }

        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("Sorry, you can't open an account!")
        else:
            print("Account has been created successfully.")
            for i in info:
                print(f"{i}: {info[i]}")
            print("Please note down your Account Number.")

            BANK.data.append(info)
            BANK.__update()
            
        
        
    def depositemoney(self):
         accnumber = input("enter your account number: ")
         pin = int(input("enter your pin: "))
         
         userdata = [i for i in BANK.data if i['accountNo']==accnumber and i['pin']==pin]
         
         if userdata == False:
             print("sorry n data found!")
         else:
             amount = int(input("how much you want to deposite:- "))
             if amount > 10000 or amount < 0:
                 print("sorry the amonut is too much you can deposite below 10000 and above 0 ")
             else:
                 userdata[0]['balance'] += amount
                 BANK.__update()
                 print("Amount deposited succefully!")




    def withdrwmoney (self):
         accnumber = input("enter your account number: ")
         pin = int(input("enter your pin: "))
         
         userdata = [i for i in BANK.data if i['accountNo']==accnumber and i['pin']==pin]
         
         if userdata == False:
             print("sorry n data found!")
         else:
             amount = int(input("how much you want to withdraw:- "))
             if userdata[0]['balance'] < amount:
                 print("sorry you dont have enough money to withdraw!")
             else:
                 userdata[0]['balance'] -= amount
                 BANK.__update()
                 print("Amount withdraw succefully!")

    
    
    
    def showdetails(self):
        accnumber = input("enter your account number: ")
        pin = int(input("enter your pin: "))
        
        userdata = [i for i in BANK.data if i['accountNo']==accnumber and i['pin']==pin]
        print("user  details are \n\n\n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
         
    
    
    
    def updatedetails(self):
         accnumber = input("enter your account number: ")
         pin = int(input("enter your pin: "))
         
         userdata = [i for i in BANK.data if i['accountNo']==accnumber and i['pin']==pin]
         if userdata == False:
             print("sorry no data found!")
         else:
             print("you can't change your age,account number and balance\n")
             print("fill the details for cgnage or leave it empty if no changes")
             
             newdata = {
                "name" : input("enter the new name of press enter to skip: "),
                "email" : input("enter the new mail or press enter to skip: "),
                "pin" : input("enter new pin or press enter to skip: ")
             }
             
             if newdata["name"] == "":
                 newdata["name"] = userdata[0]['name']
             if newdata["email"] == "":
                 newdata["email"] = userdata[0]['email']
             if newdata["pin"] == "":
                 newdata["pin"] = userdata[0]['pin']
                 
             newdata["age"] = userdata[0]['age']
             newdata["accountNo"] = userdata[0]['accountNo']
             newdata["balance"] = userdata[0]['balance']
             
             if type(newdata['pin']) == str:
                 newdata['pin'] = int(newdata['pin'])
             
             for i in newdata:
                 if newdata[i] == userdata[0][i]:
                     continue
                 else:
                     userdata[0][i] = newdata[i]
                     
             BANK.__update()
             print("User details updated succesfully!")
             
             
             
             
             
    def deletaccount(self):
         accnumber = input("enter your account number: ")
         pin = int(input("enter your pin: "))
         
         userdata = [i for i in BANK.data if i['accountNo']==accnumber and i['pin']==pin]
         if userdata == False:
             print("sorry no data found!")
         else:
             print("press y ifyou want to delet you account or press n!")
             if check == "n" or check == "N":
                 pass
             else:
                 index = BANK.data.index(userdata[0])
                 BANK.data.pop(index)
                 print("Account deleted succefully!")
                 BANK.__update()
             
    
        
user = BANK()

print("press 1 for creating an Account: ")
print("press 2 for Deposit money in the bank: ")
print("press 3 for withdrwaing the money:  ")
print("press 4 for for details: ")
print("press 5 for updating the details: ")
print("press 6 for deleting the account: ")


check = int(input("tell your response: "))

if check == 1:
    user.CreateAccount()
    
if check == 2:
    user.depositemoney()
    
if check == 3:
    user.withdrwmoney()
    
if check == 4:
    user.showdetails()
    
if check == 5:
    user.updatedetails()
    
if check == 6:
    user.deletaccount()