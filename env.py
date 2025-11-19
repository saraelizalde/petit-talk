import os

os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('SECRET_KEY', 'lEXuSg7uQqsh7EF5QPQYJ2b7GdhVCWuT')
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_DgjfPbxi16ol@ep-purple-unit-a25gvv67.eu-central-1.aws.neon.tech/silo_river_width_374249"

os.environ["STRIPE_PUBLIC_KEY"] = "pk_test_51QP9N9GLVhLhp5AKmLsnp1dcFQ9hQCWynRiKMBg2crxC1glpPOVSJbiNjvOwcSOQ5tRSOoi0OiaiIumErHsvnGqy00P75qyF0o"
os.environ["STRIPE_SECRET_KEY"] = "sk_test_51QP9N9GLVhLhp5AKq7r3PAE5mWxKdXpBHHZlDAsLsbgjEKRpRJp880oqP80ZXMPMO6Iplv9SosRBHwYpkGztbVZT00xofe9eiQ"
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_z0Ci3XDShzCPi2G1jPg2VZ3CkYAyGnAS"