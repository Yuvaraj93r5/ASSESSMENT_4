import time

class DigitalWallet:
    def __init__(self, account_id, pin, balance=0.0, daily_limit=1000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = float(balance)
        self.daily_limit = float(daily_limit)
        
        # Format: (type, amount, timestamp, status)
        self.transactions = []         
        self.failed_pin_attempts = 0
        self.is_locked = False

    def verify_pin(self, input_pin):
        if self.is_locked:
            return False
        if input_pin == self.pin:
            self.failed_pin_attempts = 0
            return True
        else:
            self.failed_pin_attempts += 1
            if self.failed_pin_attempts >= 3:
                self.is_locked = True
            return False

    def check_fraud(self, amount):
        now = time.time()
        
        # Bug Fix: tx is a tuple, timestamp is at index 2, status is at index 3
        recent_txs = [tx for tx in self.transactions if (now - tx[2]) < 600 and tx[3] == "Success"]
        if len(recent_txs) >= 5:
            return "Suspicious: High transaction frequency"
            
        if amount > self.daily_limit:
            return "Suspicious: Transaction exceeds safe threshold"
            
        if self.failed_pin_attempts > 0:
            return "Suspicious: Previous failed PIN attempts recorded"
            
        return None

    def deposit(self, amount, input_pin):
        if not self.verify_pin(input_pin):
            return "Error: Invalid PIN or Account Locked"
        if amount <= 0:
            return "Error: Deposit amount must be positive"
            
        fraud_alert = self.check_fraud(amount)
        status = "Suspicious" if fraud_alert else "Success"
        
        self.balance += amount
        self.transactions.append(("Deposit", amount, time.time(), status))
        return fraud_alert if fraud_alert else "Deposit Successful"

    def withdraw(self, amount, input_pin):
        if not self.verify_pin(input_pin):
            return "Error: Invalid PIN or Account Locked"
        if amount <= 0:
            return "Error: Withdrawal amount must be positive"
        if amount > self.balance:
            return "Error: Insufficient balance"
            
        # Bug Fix: Correctly sum the amount from index 1 of matching transaction tuples
        now = time.time()
        today_total = sum(tx[1] for tx in self.transactions if (now - tx[2]) < 86400 and tx[0] in ["Withdraw", "Transfer Out"] and tx[3] == "Success")
        if today_total + amount > self.daily_limit:
            return "Error: Daily transaction limit exceeded"

        fraud_alert = self.check_fraud(amount)
        status = "Suspicious" if fraud_alert else "Success"

        self.balance -= amount
        self.transactions.append(("Withdraw", amount, time.time(), status))
        return fraud_alert if fraud_alert else "Withdrawal Successful"

    def transfer(self, target_wallet, amount, input_pin):
        if not self.verify_pin(input_pin):
            return "Error: Invalid PIN or Account Locked"
        if amount <= 0:
            return "Error: Transfer amount must be positive"
        if amount > self.balance:
            return "Error: Insufficient balance"

        fraud_alert = self.check_fraud(amount)
        status = "Suspicious" if fraud_alert else "Success"

        self.balance -= amount
        target_wallet.balance += amount
        
        self.transactions.append(("Transfer Out", amount, time.time(), status))
        target_wallet.transactions.append(("Transfer In", amount, time.time(), "Success"))
        return fraud_alert if fraud_alert else "Transfer Successful"

    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.transactions

