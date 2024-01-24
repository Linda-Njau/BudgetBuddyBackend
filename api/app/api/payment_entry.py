from .services.payment_entry_service import PaymentEntryService
from ..models import PaymentEntry
from flask import Blueprint, request, jsonify

payment_entries = Blueprint('payment_entries',__name__)
payment_entry_service = PaymentEntryService()

@payment_entries.route('/payment_entries', methods=['POST'], strict_slashes=False)
def create_payment_entry():
    data = request.get_json()
    response, status_code = payment_entry_service.create_payment_entry(data)
    return jsonify(response), status_code

@payment_entries.route('/payment_entries/<int:payment_entry_id>', methods=['GET'], strict_slashes=False)
def get_payment_entry(payment_entry_id):
    payment_entry, status_code = payment_entry_service.get_payment_entry(payment_entry_id)
    return jsonify(payment_entry), status_code

@payment_entries.route('/users/<int:user_id>/payment_entries', methods=['GET'], strict_slashes=False)
def get_payment_entries(user_id):
    payment_category = request.args.get('payment_category')
    month = request.args.get('month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    all_payment_entries, status_code = payment_entry_service.get_payment_entries(user_id, payment_category, month, start_date, end_date)
    return jsonify(all_payment_entries), status_code

@payment_entries.route('/payment_entries/<int:payment_entry_id>', methods=['PUT'], strict_slashes=False)
def update_payment_entry(payment_entry_id):
    data = request.get_json()
    response, status_code = payment_entry_service.update_payment_entry(payment_entry_id, data)
    return jsonify(response), status_code

@payment_entries.route('/payment_entries/<int:payment_entry_id>', methods=['PATCH'], strict_slashes=False)
def patch_payment_entry(payment_entry_id):
    data = request.get_json()
    response, status_code = payment_entry_service.patch_payment_entry(payment_entry_id, data)
    return jsonify(response), status_code

@payment_entries.route('/payment_entries/<int:payment_entry_id>', methods=['DELETE'], strict_slashes=False)
def delete_payment_entry(payment_entry_id):
    response, status_code = payment_entry_service.delete_payment_entry(payment_entry_id)
    return jsonify(response), status_code
