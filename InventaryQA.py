# InventoryQA.py

import unittest
from InventoryManagement import InventoryManagement


class TestInventoryManagement(unittest.TestCase):

    def setUp(self):
        self.inventory = InventoryManagement()

        self.inventory.add_product("A", "Laptop", 20, 5)
        self.inventory.add_product("B", "Laptop", 10, 5)
        self.inventory.add_product("C", "Mouse", 15, 5)

    def test_stock_availability(self):
        stock = self.inventory.get_stock("A", "Laptop")
        self.assertEqual(stock, 20)

    def test_insufficient_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product("A", "Laptop", 50)

    def test_warehouse_transfer(self):
        self.inventory.transfer_stock(
            "A",
            "B",
            "Laptop",
            5
        )

        self.assertEqual(
            self.inventory.get_stock("A", "Laptop"),
            15
        )

        self.assertEqual(
            self.inventory.get_stock("B", "Laptop"),
            15
        )

    def test_concurrent_orders(self):
        warehouse1 = self.inventory.fulfill_order(
            "Laptop",
            10
        )

        warehouse2 = self.inventory.fulfill_order(
            "Laptop",
            10
        )

        self.assertEqual(warehouse1, "A")
        self.assertEqual(warehouse2, "A")
        self.assertEqual(
            self.inventory.get_stock("A", "Laptop"),
            0
        )

    def test_reorder_threshold(self):
        self.inventory.remove_product(
            "A",
            "Laptop",
            16
        )

        low_stock = self.inventory.low_stock()

        found = any(
            warehouse == "A"
            and product == "Laptop"
            for warehouse, product, quantity in low_stock
        )

        self.assertTrue(found)

    def test_invalid_product(self):
        with self.assertRaises(ValueError):
            self.inventory.get_stock(
                "A",
                "Mobile"
            )

    def test_negative_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product(
                "A",
                "Laptop",
                -5
            )

    def test_multiple_warehouses(self):
        self.assertIn("A", self.inventory.warehouses)
        self.assertIn("B", self.inventory.warehouses)
        self.assertIn("C", self.inventory.warehouses)

    def test_automatic_warehouse_selection(self):
        warehouse = self.inventory.select_warehouse(
            "Mouse",
            10
        )

        self.assertEqual(warehouse, "C")

    def test_reorder(self):
        self.inventory.reorder(
            "A",
            "Laptop",
            20
        )

        stock = self.inventory.get_stock(
            "A",
            "Laptop"
        )

        self.assertEqual(stock, 40)


if __name__ == "__main__":
    unittest.main()
