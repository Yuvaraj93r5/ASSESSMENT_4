# InventoryManagement.py

class InventoryManagement:

    def __init__(self):
        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }

        self.suppliers = {}
        self.reorder_threshold = {}

    def add_product(self, warehouse, product, quantity, threshold=10):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.warehouses[warehouse][product] = (
            self.warehouses[warehouse].get(product, 0) + quantity
        )

        self.reorder_threshold[product] = threshold

    def remove_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        if self.warehouses[warehouse][product] < quantity:
            raise ValueError("Insufficient inventory")

        self.warehouses[warehouse][product] -= quantity

    def get_stock(self, warehouse, product):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        return self.warehouses[warehouse][product]

    def transfer_stock(self, source, destination, product, quantity):
        if source not in self.warehouses:
            raise ValueError("Invalid source warehouse")

        if destination not in self.warehouses:
            raise ValueError("Invalid destination warehouse")

        if source == destination:
            raise ValueError("Source and destination cannot be same")

        if product not in self.warehouses[source]:
            raise ValueError("Invalid product")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.warehouses[source][product] < quantity:
            raise ValueError("Insufficient inventory")

        self.warehouses[source][product] -= quantity

        self.warehouses[destination][product] = (
            self.warehouses[destination].get(product, 0) + quantity
        )

    def add_supplier(self, product, supplier):
        self.suppliers[product] = supplier

    def get_supplier(self, product):
        if product not in self.suppliers:
            raise ValueError("Supplier not found")

        return self.suppliers[product]

    def low_stock(self):
        low_stock_products = []

        for warehouse, products in self.warehouses.items():
            for product, quantity in products.items():
                threshold = self.reorder_threshold.get(product, 10)

                if quantity <= threshold:
                    low_stock_products.append(
                        (warehouse, product, quantity)
                    )

        return low_stock_products

    def reorder(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if quantity <= 0:
            raise ValueError("Reorder quantity must be positive")

        self.warehouses[warehouse][product] = (
            self.warehouses[warehouse].get(product, 0) + quantity
        )

    def select_warehouse(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        for warehouse in self.warehouses:
            stock = self.warehouses[warehouse].get(product, 0)

            if stock >= quantity:
                return warehouse

        raise ValueError("Insufficient inventory in all warehouses")

    def fulfill_order(self, product, quantity):
        warehouse = self.select_warehouse(product, quantity)

        self.warehouses[warehouse][product] -= quantity

        return warehouse

    def display_inventory(self):
        for warehouse, products in self.warehouses.items():
            print(f"Warehouse {warehouse}")

            for product, quantity in products.items():
                print(f"{product}: {quantity}")


if __name__ == "__main__":

    inventory = InventoryManagement()

    inventory.add_product("A", "Laptop", 20, 5)
    inventory.add_product("B", "Laptop", 10, 5)
    inventory.add_product("C", "Laptop", 5, 5)

    inventory.add_product("A", "Mouse", 30, 10)
    inventory.add_product("B", "Keyboard", 15, 5)

    inventory.add_supplier("Laptop", "Dell")
    inventory.add_supplier("Mouse", "Logitech")
    inventory.add_supplier("Keyboard", "HP")

    inventory.remove_product("A", "Mouse", 5)

    inventory.transfer_stock("A", "B", "Laptop", 5)

    warehouse = inventory.select_warehouse("Laptop", 8)
    print("Selected Warehouse:", warehouse)

    inventory.fulfill_order("Laptop", 8)

    print("Low Stock:", inventory.low_stock())

    inventory.reorder("C", "Laptop", 20)

    inventory.display_inventory()
