# AnushaInturi_Ecommerce_Order_Engine_Hackathon

# 🛒 Anusha Ecommerce Order Engine Hackathon

# 📌 Project Overview

This project is a **Distributed E-Commerce Order Engine** built using Python (CLI-based).
It simulates real-world backend systems used by companies like Amazon and Flipkart.

The system handles:

* Multiple users accessing products
* Inventory conflicts (overselling prevention)
* Payment failures and recovery
* Order lifecycle management
* Real-time stock updates

The goal is to demonstrate **scalable system design, concurrency handling, and fault tolerance**.

---

## 🚀 Features Implemented

### 🧾 Product Management

* Add new products
* Prevent duplicate product IDs
* Update and view inventory
* Low stock alert system

### 🛒 Multi-User Cart System

* Separate cart for each user
* Add/remove/update items
* Cart synced with inventory

### 🔒 Concurrency Handling

* Thread-based locking mechanism
* Prevents overselling issues

### 📦 Order Management

* Place orders (atomic operation)
* View and search orders
* Cancel orders with stock restoration

### 💳 Payment Simulation

* Random success/failure simulation
* Failure triggers rollback

### 🔁 Transaction Rollback

* Ensures "all or nothing" execution
* Restores stock on failure

### 🎟️ Discount & Coupon Engine

* 10% discount for orders > ₹1000
* Extra 5% discount for bulk orders
* Coupon codes:

  * SAVE10 → 10% off
  * FLAT200 → ₹200 off

### 📢 Event-Driven System

* ORDER_CREATED
* PAYMENT_SUCCESS
* ORDER_FAILED
* Events processed sequentially

### ⏳ Inventory Reservation Expiry

* Reserved stock auto-released after expiry

### 📜 Audit Logging System

* Immutable logs with timestamps

### 🚨 Fraud Detection

* Flags users placing 3+ orders in 1 minute
* Detects high-value transactions

### 🔁 Idempotency Handling

* Prevents duplicate orders from multiple clicks

---

## 🏗️ Design Approach

The system follows a **modular service-based architecture**:

* Product Service → Handles inventory management
* Cart Service → Manages user carts
* Order Service → Processes orders and lifecycle
* Payment Service → Simulates payment processing

Concurrency is handled using **thread locks**, ensuring safe access to shared resources.

---

## ⚙️ Assumptions

* CLI-based application (no UI)
* Single system simulation (not distributed servers)
* Payment is simulated randomly
* Reservation expiry is simplified for demonstration

---

## 🧪 How to Run the Project

### Step 1: Clone Repository

```bash
git clone https://github.com/Anusha-20033/Anusha_Ecommerce_Order_Engine_Hackathon.git
```

### Step 2: Navigate to Folder

```bash
cd Anusha_Ecommerce_Order_Engine_Hackathon
```

### Step 3: Run the Program

```bash
python main.py
```

---

## 👩‍💻 Author

**Anusha**
GitHub: https://github.com/Anusha-20033
