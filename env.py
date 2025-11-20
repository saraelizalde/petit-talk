import os

os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'secret')
os.environ["DATABASE_URL"] = "url"

os.environ["STRIPE_PUBLIC_KEY"] = "test_public_placeholder"
os.environ["STRIPE_SECRET_KEY"] = "test_secret_placeholder"
os.environ["STRIPE_WEBHOOK_SECRET"] = "test_webhook_placeholder"