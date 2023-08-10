from flask import Blueprint, jsonify

payments = Blueprint('payments,__name__')


@payments.route('/<int:user_id>', methods=['GET'])
def get_payment(user_id):
    payments = payments_service.get_payments(user_id)
    return jsonify(payments)
