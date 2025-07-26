import json
import random
import string
from pathlib import Path
import streamlit as st

class BANK:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database) as f:
                cls.data = json.load(f)
        else:
            cls.data = []

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def __accountgenerate(cls):
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=7))

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return False, "Sorry, you can't open an account."

        acc_no = cls.__accountgenerate()
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": acc_no,
            "balance": 0
        }

        cls.data.append(info)
        cls.__update()
        return True, info

    @classmethod
    def validate_user(cls, accnumber, pin):
        return next((i for i in cls.data if i['accountNo'] == accnumber and i['pin'] == pin), None)

    @classmethod
    def deposit_money(cls, user, amount):
        if amount <= 0 or amount > 10000:
            return False, "Amount must be between 1 and 10000."
        # Find and update the user in cls.data
        for u in cls.data:
            if u['accountNo'] == user['accountNo']:
                u['balance'] += amount
                break
        cls.__update()
        return True, "Amount deposited successfully!"

    @classmethod
    def withdraw_money(cls, user, amount):
        # Find and update the user in cls.data
        for u in cls.data:
            if u['accountNo'] == user['accountNo']:
                if u['balance'] < amount:
                    return False, "Insufficient funds."
                u['balance'] -= amount
                cls.__update()
                return True, "Withdrawal successful!"
        return False, "User not found."

    @classmethod
    def update_user(cls, user, new_name, new_email, new_pin):
        for u in cls.data:
            if u['accountNo'] == user['accountNo']:
                if new_name: u['name'] = new_name
                if new_email: u['email'] = new_email
                if new_pin:
                    if len(str(new_pin)) == 4:
                        u['pin'] = int(new_pin)
                    else:
                        return False, "PIN must be 4 digits."
                cls.__update()
                return True, "Details updated."
        return False, "User not found."

    @classmethod
    def delete_account(cls, user):
        # Remove user by accountNo to ensure correct deletion
        cls.data = [u for u in cls.data if u['accountNo'] != user['accountNo']]
        cls.__update()
        return "Account deleted successfully!"
