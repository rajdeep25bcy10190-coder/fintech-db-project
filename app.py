import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="fintech_app"
    )
    cursor = db.cursor(dictionary=True)
    print("🚀 System Connected to scaled architecture.")
except mysql.connector.Error as err:
    print(f"❌ Connection Failed: {err}")
    exit()

def add_transaction():
    print("\n--- Log New Expense ---")
    user_id = input("Enter User ID (Use '1' for test user): ")
    amount = input("Amount ($): ")
    category = input("Category: ")
    date_str = input("Date (YYYY-MM-DD) or press Enter for Today: ")
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')
    try:
        query = "INSERT INTO transactions (user_id, amount, category, transaction_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (int(user_id), float(amount), category, date_str))
        db.commit()
        print("✅ Transaction saved successfully!")
    except Exception as e:
        print(f"❌ Operation Failed: {e}")

def view_transactions():
    print("\n--- Transaction History ---")
    try:
        query = "SELECT t.transaction_id, u.username, t.amount, t.category, t.transaction_date FROM transactions t JOIN users u ON t.user_id = u.user_id ORDER BY t.transaction_date DESC"
        cursor.execute(query)
        records = cursor.fetchall()
        if not records:
            print("No entries recorded.")
            return
        print(f"{'ID':<5} | {'User':<15} | {'Amount':<10} | {'Category':<12} | {'Date':<12}")
        print("-" * 65)
        for row in records:
            print(f"{row['transaction_id']:<5} | {row['username']:<15} | ${row['amount']:<9} | {row['category']:<12} | {str(row['transaction_date']):<12}")
    except Exception as e:
        print(f"❌ Error: {e}")

def subscribe_to_service():
    print("\n--- Available Marketplace Plans ---")
    try:
        # Complex multi-table JOIN query to show clean product profiles
        query = """
            SELECT s.subscription_id, m.name AS merchant, s.plan_name, s.billing_cycle, s.cost 
            FROM subscriptions s
            JOIN merchants m ON s.merchant_id = m.merchant_id
        """
        cursor.execute(query)
        plans = cursor.fetchall()
        
        print(f"{'ID':<5} | {'Provider':<15} | {'Plan Tier':<22} | {'Cycle':<10} | {'Cost':<8}")
        print("-" * 68)
        for plan in plans:
            print(f"{plan['subscription_id']:<5} | {plan['merchant']:<15} | {plan['plan_name']:<22} | {plan['billing_cycle']:<10} | ${plan['cost']:<8}")
            
        user_id = input("\nEnter User ID to link (e.g., 1): ")
        sub_id = input("Enter Plan ID to register: ")
        
        start_date = datetime.today()
        next_billing = start_date + timedelta(days=30) # Automatically project next renewal date
        
        sub_query = """
            INSERT INTO user_subscriptions (user_id, subscription_id, start_date, next_billing_date, status)
            VALUES (%s, %s, %s, %s, 'active')
        """
        cursor.execute(sub_query, (int(user_id), int(sub_id), start_date.strftime('%Y-%m-%d'), next_billing.strftime('%Y-%m-%d')))
        db.commit()
        print("🎉 Successfully subscribed! Live enrollment complete.")
    except Exception as e:
        print(f"❌ Enrollment Failed: {e}")

def view_active_subscriptions():
    print("\n--- User Active Subscriptions Dashboard ---")
    user_id = input("Enter User ID to review (e.g., 1): ")
    try:
        # Triple-join query pulling data down across our complete schema network
        query = """
            SELECT m.name AS platform, s.plan_name, s.cost, us.next_billing_date, us.status
            FROM user_subscriptions us
            JOIN subscriptions s ON us.subscription_id = s.subscription_id
            JOIN merchants m ON s.merchant_id = m.merchant_id
            WHERE us.user_id = %s
        """
        cursor.execute(query, (int(user_id),))
        active_subs = cursor.fetchall()
        
        if not active_subs:
            print("No active subscription lines mapped to this account profile.")
            return
            
        print(f"\n{'Platform':<15} | {'Plan Name':<22} | {'Monthly Cost':<12} | {'Renewal Date':<12} | {'Status':<8}")
        print("-" * 75)
        for sub in active_subs:
            print(f"{sub['platform']:<15} | {sub['plan_name']:<22} | ${sub['cost']:<11} | {str(sub['next_billing_date']):<12} | {sub['status'].upper():<8}")
    except Exception as e:
        print(f"❌ Failed to fetch user dashboard: {e}")

def main():
    while True:
        print("\n=== Scaled FinTech Hub Terminal ===")
        print("1. Log an Outright Expense")
        print("2. View Expense Logs")
        print("3. Purchase Marketplace Subscription (Many-to-Many)")
        print("4. View User Active Subscription Dashboard")
        print("5. Exit Workspace")
        choice = input("Select operation option (1-5): ")
        
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            subscribe_to_service()
        elif choice == choice == "4":
            view_active_subscriptions()
        elif choice == "5":
            print("Disconnecting from database engine. Systems offline.")
            break
        else:
            print("Unknown input flag. Re-verify interface command.")

if __name__ == "__main__":
    main()