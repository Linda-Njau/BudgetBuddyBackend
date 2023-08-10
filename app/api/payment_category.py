from flask import Blueprint, jsonify

payment_category = Blueprint('payment_category,__name__')


@payment_category.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_payment_categories(user_id):
    """Returns payment categories for the given user"""
    payment_categories = payments_category_service.get_payment_categories(user_id)
    return jsonify(payment_categories)

@payment_category.route('/<int:payment_category_id>', methods=['GET'], strict_slashes=False)
def get_payment_category_by_payment_category(payment_category_id):
    """Returns the payment category specified by it's id"""
    payment_category = payments_category_service.get_payment_category(payment_category_id)
    return jsonify(payment_category)

