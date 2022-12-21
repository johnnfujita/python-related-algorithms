import stripe
from flask import Flask, redirect, request, render_template
import os
import json
from stripe.api_resources import payment_intent



class StripeBackend():
    pk: str
    sk: str
    
    def __init__(self, pk: str, sk: str):
        self.pk = pk
        self.sk = sk
        self.set_api_key()

    def set_api_key(self):
        stripe.api_key = self.sk


app = Flask(
            __name__,
            static_url_path="",
            static_folder="public",
            template_folder="."
)


DOMAIN = "http://localhost:3000/checkout"

key: str = "pk_test_51JT6H8KVteqLEupjjXRbu5Dq5HdqdAQcIAjj5U3eXHxzsWPvaxjWTDvzmWcL7PrsNbuUELySNnm4ofwx8Lswi4wg00xrvOuwok"
secret: str = "sk_test_51JT6H8KVteqLEupjmqJyMg7XosV4GCeEjxNxEzm0JYpkDFARUKWRUZQDyaKLpUU4M6G1yOFh6dU3dyRyawJuKSQ500xBpMeSMZ"

stripe.api_key = secret


@app.route("/register-customer", methods=["POST"])
def register_customer():
    customer = stripe.Customer.create()
    return customer.id

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": 'price_1JT6nsKVteqLEupjGxegv5qy',
                    "quantity": 1
                }
            ],
            payment_method_types=[
                "card"
            ],
            mode="payment",
            success_url=DOMAIN + "?success=true",
            cancel_url=DOMAIN + "?canceled=true"
        )
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)


@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent_call():
    payment = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        payment_method_types=['card'],
        receipt_email='jenny.rosen@example.com',
        idempotency_key="7f8038h02hrubnjfsr38924jfko"

        
    )
    return json.dumps(payment)

@app.route("/register-payment-method", methods=["POST"])
def create_payment_method():
    payment_method = stripe.PaymentMethod.create(
        type="card",
        card={
          "number": "4242424242424242",
          "exp_month": 8,
          "exp_year": 2022,
          "cvc": "314",
        },
    )
    return json.dumps(payment_method)

@app.route("/retrieve-payment-method", methods=["GET"])
def retrieve_payment_method():
    payment_method = stripe.PaymentMethod.retrieve(
        "pm_1JUhMVKVteqLEupjfbWsdXfX"
    )
    return json.dumps(payment_method)

    
@app.route('/card-wallet')
def card_wallet():
  intent = stripe.SetupIntent.create(
    customer=stripe.Customer.create()
  )
  return render_template('card_wallet.html', client_secret=intent.client_secret)


# @app.route("/create-setup-intent", methods=["POST"])
# def create_setup_intent_call():
#     payment = stripe.SetupIntent.create(
#         amount=1000,
#         currency='usd',
#         payment_method_types=['card'],
#         receipt_email='jenny.rosen@example.com',
#         idempotency_key="7f8038h02hrubnjfsr38924jfko"

        
#     )
#     return json.dumps(payment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4242)
    stripe_back = StripeBackend(sk=secret)
    stripe_back.set_api_key()
