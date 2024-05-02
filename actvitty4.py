import csv

class Article:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity


class shoppingcart:
    def __init__(self):
        self.products = self.load_products()
        self.cart = {}

    def load_products(self):
        try:
            with open('products.csv', 'r') as file:
                reader = csv.reader(file)
                products = {row[0]: {'price': float(row[1]), 'inventory': int(row[2])} for row in reader}
            return products
        except FileNotFoundError:
            print("Error: 'products.csv' file not found.")
            return {}

    def save_products(self):
        with open('products.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for product, details in self.products.items():
                writer.writerow([product, details['price'], details['inventory']])

    def display_products(self):
        print("Product List:")
        for product, details in self.products.items():
            print(f"{product} - ${details['price']} - Inventory: {details['inventory']}")

    def add_to_cart(self, product, quantity):
        if product in self.products and quantity > 0:
            if quantity <= self.products[product]['inventory']:
                self.cart[product] = {'quantity': quantity, 'price': self.products[product]['price']}
                self.products[product]['inventory'] -= quantity
                print(f"{quantity} {product}(s) added to the cart.")
            else:
                print("Error: Insufficient inventory.")
        else:
            print("Error: Invalid product or quantity.")

    def display_cart(self):
        print("Shopping Cart:")
        for product, details in self.cart.items():
            print(f"{product} - Quantity: {details['quantity']} - Total: ${details['quantity'] * details['price']}")

    def remove_from_cart(self, product, quantity):
        if product in self.cart and quantity > 0:
            if quantity <= self.cart[product]['quantity']:
                self.cart[product]['quantity'] -= quantity
                self.products[product]['inventory'] += quantity
                print(f"{quantity} {product}(s) removed from the cart.")
                if self.cart[product]['quantity'] == 0:
                    del self.cart[product]
            else:
                print("Error: Invalid quantity to remove.")
        else:
            print("Error: Invalid product or quantity.")

    def checkout(self):
        subtotal = sum(details['quantity'] * details['price'] for details in self.cart.values())
        tax = 0.07 * subtotal
        total = subtotal + tax

        print("\nOrder Summary:")
        self.display_cart()
        print(f"\nSubtotal: ${subtotal:.2f}")
        print(f"Tax (7%): ${tax:.2f}")
        print(f"Total: ${total:.2f}")

        self.save_products()

    def run(self):
        while True:
            print("\nCommands:")
            print("1. List\n2. Cart\n3. Add\n4. Remove\n5. Checkout\n6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.display_products()
            elif choice == '2':
                self.display_cart()
            elif choice == '3':
                product = input("Enter the product name to add: ")
                quantity = int(input("Enter the quantity: "))
                self.add_to_cart(product, quantity)
            elif choice == '4':
                product = input("Enter the product name to remove: ")
                quantity = int(input("Enter the quantity: "))
                self.remove_from_cart(product, quantity)
            elif choice == '5':
                self.checkout()
                break
            elif choice == '6':
                self.save_products()
                print("Exiting the program. Thank you!")
                break
            else:
                print("Error: Invalid choice. Please choose a valid command.")

if __name__ == "__main__":
    shopping = shoppingcart()
    shopping.run()