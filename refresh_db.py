import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jkr.settings')
django.setup()

from orders.models import CustomerOrder, CustomerOrderItem, OrderStatusHistory, QuoteEnquiry, QuoteItem, Order, OrderItem
from blog.models import Post

def refresh_database():
    print("🧹 Refreshing database for production launch...")
    
    # 1. Clear all order data
    print("Clearing orders and enquires...")
    CustomerOrderItem.objects.all().delete()
    OrderStatusHistory.objects.all().delete()
    CustomerOrder.objects.all().delete()
    QuoteItem.objects.all().delete()
    QuoteEnquiry.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Post.objects.all().delete()
    
    # 2. Reset sequences (PostgreSQL/Neon specific)
    print("Resetting primary key sequences...")
    with connection.cursor() as cursor:
        tables = [
            'orders_customerorder',
            'orders_customerorderitem',
            'orders_orderstatushistory',
            'orders_quoteenquiry',
            'orders_quoteitem',
            'orders_order',
            'orders_orderitem',
            'blog_post',
        ]
        for table in tables:
            try:
                # This resets the serial/identity sequence to 1
                cursor.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;")
                print(f"  Reset sequence for {table}")
            except Exception as e:
                print(f"  Could not reset sequence for {table}: {e}")

    print("\n✅ Database refreshed. Your next order will be #Demo-00001")

if __name__ == "__main__":
    refresh_database()
