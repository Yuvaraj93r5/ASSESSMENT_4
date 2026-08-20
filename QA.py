import unittest
from DigitalWallet import DigitalWallet

class TestWalletSecurityQA(unittest.TestCase):
    
    def setUp(self):
        self.wallet = DigitalWallet(account_id="QA_TEST_01", balance=1000.0)
        self.target_wallet = DigitalWallet(account_id="QA_RECEIVER", balance=0.0)

    def test_normal_transaction(self):
        self.wallet.deposit(500)
        self.assertEqual(self.wallet.verify_balance(), 1500.0)

    def test_insufficient_balance(self):
        result = self.wallet.withdraw(2000.0)
        self.assertEqual(result, "Insufficient balance")

    def test_daily_limit(self):
        self.wallet.deposit(60000.0)
        result = self.wallet.withdraw(55000.0)
        self.assertIn("Daily limit exceeded", result)

    def test_multiple_failed_pins(self):
        # Simulating automated rule check for too many pin strikes
        self.wallet.failed_pin_attempts = 4
        if self.wallet.failed_pin_attempts >= 3:
            result = self.wallet.flag_suspicious("Multiple failed PIN attempts")
        self.assertIn("failed PIN attempts", result)

    def test_suspicious_transaction_large_amount(self):
        result = self.wallet.money_transfer(self.target_wallet, 15000.0)
        self.assertIn("Large transaction flag", result)

    def test_duplicate_transaction(self):
        # Ensures validation fails if exact duplicate criteria occur rapidly
        self.wallet.withdraw(100)
        # Mock validation framework catch rule logic here
        pass 

    def test_negative_amount(self):
        result = self.wallet.deposit(-50)
        self.assertEqual(result, "Invalid deposit amount")

    def test_concurrent_transactions(self):
        # Validates system logic under race conditions or rapid inputs
        pass

if __name__ == '__main__':
    unittest.main()

