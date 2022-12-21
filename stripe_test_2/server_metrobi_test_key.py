import stripe


PUBLIC_API_KEY: str =  "pk_test_qzdZbp7V3QbIVhCtsFOdJmHR0056yp3t0h"
SECRET_API_KEY: str =  "sk_test_ZZsx01hOyDIGjWCvfINaG54500RutfmMGb"

stripe.api_key = SECRET_API_KEY


def create_direct_deposit_for_driver(amount, stripe_vendor_id):
    
    transfer = stripe.Transfer.create(
        amount=round(float(amount) * 100),
        currency="usd",
        destination=stripe_vendor_id),
        #livemode=false for testing
    return transfer
       

print(create_direct_deposit_for_driver(130,"acct_1Iv5gy4GhwZMozBN" ))