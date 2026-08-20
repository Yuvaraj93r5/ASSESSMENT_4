import time

class DigitalWallet:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.transactions = [] # Format: (timestamp, type, amount, status)
        self.failed_pin_attempts = 0
        self.daily_limit = 50000.0
        self.daily_spent = 0.0

    def create_account(self):
        return f"Account {self.account_id} created successfully."

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid deposit amount"
        self.balance += amount
        self.transactions.append((time.time(), 'deposit', amount, 'Success'))
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        
        # Fraud check: Daily Limit
        if self.daily_spent + amount > self.daily_limit:
            return self.flag_suspicious("Daily limit exceeded")
            
        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append((time.time(), 'withdraw', amount, 'Success'))
        return self.balance

    def money_transfer(self, target_wallet, amount):
        # Fraud check: Large or unusual transaction amount thresholds
        if amount >= 10000.0:
            return self.flag_suspicious("Large transaction flag activated")
            
        withdrawal_status = self.withdraw(amount)
        if isinstance(withdrawal_status, float):
            target_wallet.deposit(amount)
            return "Transfer Successful"
        return withdrawal_status

    def get_transaction_history(self):
        return self.transactions

    def verify_balance(self):
        return self.balance

    def flag_suspicious(self, reason):
        # Basic fraud detection logging mechanisms
        print(f"[SECURITY ALERT] Suspicious Activity Flagged: {reason}")
        return f"Suspicious Activity Detected: {reason}"

    def check_velocity_fraud(self):
        # Fraud check: More than 5 transactions in 10 minutes
        now = time.time()
        recent_txs = [tx for tx in self.transactions if now - tx[0] <= 600]
        if len(recent_txs) > 5:
            return self.flag_suspicious("Velocity control: >5 tx in 10 mins")
        return "Normal velocity"

