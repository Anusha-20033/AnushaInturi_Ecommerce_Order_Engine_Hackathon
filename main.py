import threading
import time
import random
from datetime import datetime
from collections import defaultdict, deque

#MODELS 

class Product:
    def __init__(self, pid, name, price, stock):
        self.pid = pid
        self.name = name
        self.price = price
        self.stock = stock
        self.reserved = 0

class Order:
    def __init__(self, oid, user, items, total):
        self.oid = oid
        self.user = user
        self.items = items
        self.total = total
        self.status = "CREATED"
        self.timestamp = time.time()

# GLOBAL STORAGE

products = {}
carts = defaultdict(dict)
orders = {}
locks = defaultdict(threading.Lock)
logs = []
events = deque()
processed_requests = set()
user_orders_time = defaultdict(list)

#LOGGING 

def log(msg):
    logs.append(f"[{datetime.now()}] {msg}")

#PRODUCT SERVICE 

def add_product():
    pid = input("Product ID: ")
    if pid in products:
        print("❌ Duplicate ID")
        return

    name = input("Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    if stock < 0:
        print("❌ Invalid stock")
        return

    products[pid] = Product(pid, name, price, stock)
    log(f"Product {pid} added")

def view_products():
    for p in products.values():
        print(p.pid, p.name, p.price, f"Stock:{p.stock}", f"Reserved:{p.reserved}")

# CART SERVICE

def add_to_cart(user):
    pid = input("Product ID: ")
    qty = int(input("Qty: "))

    if pid not in products:
        print("❌ Not found")
        return

    product = products[pid]

    with locks[pid]:
        if product.stock - product.reserved >= qty:
            carts[user][pid] = carts[user].get(pid, 0) + qty
            product.reserved += qty
            log(f"{user} added {pid} qty={qty}")
            print("✅ Added")
        else:
            print("❌ Stock insufficient")

def remove_from_cart(user):
    pid = input("Product ID: ")

    if pid in carts[user]:
        qty = carts[user][pid]
        products[pid].reserved -= qty
        del carts[user][pid]
        print("✅ Removed")

def view_cart(user):
    print("Cart:", carts[user])

# RESERVATION EXPIRY 

def release_expired_reservations():
    for user in carts:
        for pid in list(carts[user].keys()):
            # simple expiry simulation
            if random.choice([True, False]):
                qty = carts[user][pid]
                products[pid].reserved -= qty
                del carts[user][pid]
                print(f"⏳ Reservation expired for {pid}")

#DISCOUNT ENGINE 

def apply_discount(total, items):
    qty = sum(items.values())

    if total > 1000:
        total *= 0.9
    if qty > 3:
        total *= 0.95

    coupon = input("Coupon: ")

    if coupon == "SAVE10":
        total *= 0.9
    elif coupon == "FLAT200":
        total -= 200

    return max(total, 0)

#PAYMENT 

def payment():
    return random.choice([True, False])

# FRAUD DETECTION 

def fraud_check(user, total):
    now = time.time()
    user_orders_time[user] = [t for t in user_orders_time[user] if now - t < 60]

    if len(user_orders_time[user]) >= 3:
        print("⚠️ Fraud Alert: Too many orders")

    if total > 50000:
        print("⚠️ High value order")

#EVENT SYSTEM 

def process_events():
    while events:
        e = events.popleft()
        print("📢 Event:", e)
        log(e)

#ORDER SERVICE 

valid_transitions = {
    "CREATED": ["PENDING_PAYMENT"],
    "PENDING_PAYMENT": ["PAID", "FAILED"],
    "PAID": ["SHIPPED"],
    "SHIPPED": ["DELIVERED"],
}

def place_order(user):
    req_id = input("Request ID: ")

    if req_id in processed_requests:
        print("⚠️ Duplicate request")
        return

    processed_requests.add(req_id)

    if not carts[user]:
        print("❌ Empty cart")
        return

    items = carts[user]
    total = sum(products[p].price * q for p, q in items.items())
    total = apply_discount(total, items)

    fraud_check(user, total)

    oid = str(len(orders) + 1)

    try:
        # lock all
        for pid in items:
            locks[pid].acquire()

        # stock validation
        for pid, qty in items.items():
            if products[pid].stock < qty:
                raise Exception("Stock error")

        # reserve to actual deduction
        for pid, qty in items.items():
            products[pid].stock -= qty
            products[pid].reserved -= qty

        order = Order(oid, user, dict(items), total)
        order.status = "PENDING_PAYMENT"
        orders[oid] = order

        events.append("ORDER_CREATED")

        if not payment():
            raise Exception("Payment failed")

        order.status = "PAID"
        carts[user].clear()
        user_orders_time[user].append(time.time())

        events.append("PAYMENT_SUCCESS")

        print("✅ Order Success")

    except Exception as e:
        print("❌ Error:", e)

        # rollback
        for pid, qty in items.items():
            products[pid].stock += qty

        if oid in orders:
            del orders[oid]

        events.append("ORDER_FAILED")

    finally:
        for pid in items:
            locks[pid].release()

    process_events()

# ORDER MANAGEMENT 

def view_orders():
    for o in orders.values():
        print(o.oid, o.user, o.total, o.status)

def cancel_order():
    oid = input("Order ID: ")

    if oid not in orders:
        print("❌ Not found")
        return

    order = orders[oid]

    if order.status == "CANCELLED":
        print("Already cancelled")
        return

    for pid, qty in order.items.items():
        products[pid].stock += qty

    order.status = "CANCELLED"
    print("✅ Cancelled")

# RETURN SYSTEM 

def return_product():
    oid = input("Order ID: ")
    pid = input("Product ID: ")
    qty = int(input("Qty: "))

    if oid not in orders:
        return

    order = orders[oid]

    if pid in order.items:
        products[pid].stock += qty
        order.total -= products[pid].price * qty
        print("✅ Returned")

#LOW STOCK 

def low_stock():
    for p in products.values():
        if p.stock <= 2:
            print("⚠️ Low stock:", p.pid)

#CONCURRENCY 

def simulate_users():
    def task(user):
        add_to_cart(user)

    t1 = threading.Thread(target=task, args=("A",))
    t2 = threading.Thread(target=task, args=("B",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

#  CLI

def main():
    user = "User1"

    while True:
        print("\n1.Add Product\n2.View Products\n3.Add Cart")
        print("\n4.Remove Cart\n5.View Cart\n6.Place Order")
        print("\n7.View Orders\n8.Cancel\n9.Low Stock")
        print("\n10.Return\n11.Concurrent\n12.Logs\n13.Expire")
        print("\n0.Exit")

        ch = input("Choice: ")

        if ch == "1": add_product()
        elif ch == "2": view_products()
        elif ch == "3": add_to_cart(user)
        elif ch == "4": remove_from_cart(user)
        elif ch == "5": view_cart(user)
        elif ch == "6": place_order(user)
        elif ch == "7": view_orders()
        elif ch == "8": cancel_order()
        elif ch == "9": low_stock()
        elif ch == "10": return_product()
        elif ch == "11": simulate_users()
        elif ch == "12": print(*logs, sep="\n")
        elif ch == "13": release_expired_reservations()
        elif ch == "0": break

if __name__ == "__main__":
    main()
