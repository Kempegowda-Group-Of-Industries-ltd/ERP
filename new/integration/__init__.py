# integration/__init__.py

from .erp_integration import (
    authenticate_with_erp,
    send_inventory_to_erp,
    fetch_erp_data,
    update_erp_order_status
)

from .ecommerce_integration import (
    authenticate_with_ecommerce,
    send_inventory_to_ecommerce,
    fetch_orders_from_ecommerce,
    update_order_status
)

__all__ = [
    # ERP Integration Functions
    "authenticate_with_erp",
    "send_inventory_to_erp",
    "fetch_erp_data",
    "update_erp_order_status",
    
    # eCommerce Integration Functions
    "authenticate_with_ecommerce",
    "send_inventory_to_ecommerce",
    "fetch_orders_from_ecommerce",
    "update_order_status"
]
