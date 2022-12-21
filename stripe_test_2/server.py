#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe

from flask import Flask, render_template, jsonify, request, make_response


# This is your real test secret API key.
key: str = "pk_test_51JT6H8KVteqLEupjjXRbu5Dq5HdqdAQcIAjj5U3eXHxzsWPvaxjWTDvzmWcL7PrsNbuUELySNnm4ofwx8Lswi4wg00xrvOuwok"
secret: str = "sk_test_51JT6H8KVteqLEupjmqJyMg7XosV4GCeEjxNxEzm0JYpkDFARUKWRUZQDyaKLpUU4M6G1yOFh6dU3dyRyawJuKSQ500xBpMeSMZ"
stripe.api_key = secret




app = Flask(__name__, static_folder="./front-end/public",
            static_url_path="", template_folder="./front-end/public")


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

@app.route("/charge-customer", methods=["POST"])
def charge_customer():
    data = json.loads(request.data)

    customerId = data["customerId"]
    # Lookup the saved card (you can store multiple PaymentMethods on a Customer)
    print(customerId)
    payment_methods = stripe.PaymentMethod.list(
        customer=customerId,
        type='card'
    )
    print(json.dumps(payment_methods))
    # Charge the customer and payment method immediately
    payment_intent = stripe.PaymentIntent.create(
        amount=4000,
        currency='usd',
        customer=customerId,
        payment_method=payment_methods.data[0].id,
        off_session=True,
        confirm=True
    )
    messsage = payment_intent.status
    print(payment_intent.status)
    if payment_intent.status == 'succeeded':
        
        print('Successfully charged card off session')
    elif payment_intent.status == "incomplete":
        payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent.id
        )
    else:
        print('payment_intent_failed')
    return messsage


@app.route('/create-payment-intent', methods=["OPTIONS", 'POST'])
def create_payment():
    # Alternatively, set up a webhook to listen for the payment_intent.succeeded event
    # and attach the PaymentMethod to a new Customer
    customer = stripe.Customer.create()
    print(customer.id)
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": # The actual request following the preflight 
        try:
            data = json.loads(request.data)
            intent = stripe.PaymentIntent.create(
                customer=customer['id'],
                setup_future_usage='off_session',
                amount=calculate_order_amount(data['items']),
                currency='usd'
            )
            print(intent["client_secret"])
            return _corsify_actual_response(jsonify({
              'clientSecret': intent['client_secret']
            }))
        except Exception as e:
            return jsonify(error=str(e)), 403
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4242)