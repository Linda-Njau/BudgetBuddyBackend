from .services.payment_entry_service import PaymentEntryService
from ..models import PaymentEntry
from flask import Blueprint, request, jsonify

payment_entries = Blueprint('payment_entries',__name__)
payment_entry_service = PaymentEntryService()

@payment_entries.route('/payment_entries', methods=['POST'], strict_slashes=False)
def create_payment_entry():
    data = request.get_json()
    response = payment_entry_service.create_payment_entry(data)
    return jsonify(response), 201

@payment_entries.route('/<int:payment_entry_id>', methods=['GET'], strict_slashes=False)
def get_payment_entry(payment_entry_id):
    payment_entry = payment_entry_service.get_payment_entry(payment_entry_id)
    return jsonify(payment_entry), 200

@payment_entries.route('/<int:payment_category_id>/payment_entries', methods=['GET'], strict_slashes=False)
def get_payment_entries(payment_category_id):
    """Returns a payment category and all the payment entries for the given user"""
    month = request.args.get('month')
    payment_category_entries = payment_entry_service.get_payment_entries(payment_category_id, month)
    return jsonify(payment_category_entries), 200

@payment_entries.route('/<int:payment_entry_id>', methods=['PUT'], strict_slashes=False)
def update_payment_entry(payment_entry_id):
    data = request.get_json()
    response = payment_entry_service.update_payment_entry(payment_entry_id, data)
    return jsonify(response), 200

@payment_entries.route('/<int:payment_entry_id>', methods=['DELETE'], strict_slashes=False)
def delete_payment_entry(payment_entry_id):
    response = payment_entry_service.delete_payment_entry(payment_entry_id)
    return jsonify(response), 200
