import os

os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'lEXuSg7uQqsh7EF5QPQYJ2b7GdhVCWuT')
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_DgjfPbxi16ol@ep-purple-unit-a25gvv67.eu-central-1.aws.neon.tech/silo_river_width_374249"

os.environ["STRIPE_PUBLIC_KEY"] = "pk_test_..."
os.environ["STRIPE_SECRET_KEY"] = "sk_test_..."