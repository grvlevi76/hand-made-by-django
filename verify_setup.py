import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from hand_made.models import Category, Product, Cart, CartItem
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

def run_verification():
    print("Starting verification...")

    # 1. Create User
    user_count = User.objects.count()
    user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('password123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"ℹ️ Test user already exists: {user.username}")

    # 2. Create Category
    category, created = Category.objects.get_or_create(name='Test Category', slug='test-category')
    if created:
        print(f"✅ Created category: {category.name}")
    else:
        print(f"ℹ️ Category already exists: {category.name}")

    # 3. Create Product
    product, created = Product.objects.get_or_create(
        slug='test-product',
        defaults={
            'name': 'Test Product',
            'category': category,
            'price': 999.00,
            'stock': 10,
            'description': 'This is a test product'
        }
    )
    if created:
        print(f"✅ Created product: {product.name}")
    else:
        print(f"ℹ️ Product already exists: {product.name}")

    # 4. Test Cart Functionality
    cart, created = Cart.objects.get_or_create(user=user)
    print(f"✅ Retrieved/Created cart for user: {user.username}")

    # Add item to cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print(f"✅ Added product to cart")
    else:
        cart_item.quantity += 1
        cart_item.save()
        print(f"✅ Incremented product quantity in cart")

    # Verify Cart Total
    expected_total = product.price * cart_item.quantity
    if cart.total_price == expected_total:
        print(f"✅ Cart total calculation correct: {cart.total_price}")
    else:
        print(f"❌ Cart total calculation incorrect: Expected {expected_total}, got {cart.total_price}")

    print("\nVerification complete!")

if __name__ == '__main__':
    try:
        run_verification()
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
