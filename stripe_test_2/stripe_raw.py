import stripe

key: str = "pk_test_51JT6H8KVteqLEupjjXRbu5Dq5HdqdAQcIAjj5U3eXHxzsWPvaxjWTDvzmWcL7PrsNbuUELySNnm4ofwx8Lswi4wg00xrvOuwok"
secret: str = "sk_test_51JT6H8KVteqLEupjmqJyMg7XosV4GCeEjxNxEzm0JYpkDFARUKWRUZQDyaKLpUU4M6G1yOFh6dU3dyRyawJuKSQ500xBpMeSMZ"
stripe.api_key = secret


account = stripe.Account.create(
  type="custom",
  country="US",
  email="johnnie_fujitao@example.com",
  capabilities={
    "card_payments": {"requested": True},
    "transfers": {"requested": True},
  },
)

