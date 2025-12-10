import requests

ORDER_SERVICE_BASE_URL = "http://127.0.0.1:8000/order"
PRODUCT_SERVICE_BASE_URL = "http://127.0.0.1:8000/product"
USER_SERVICE_BASE_URL = "http://127.0.0.1:8000/user"


class Console:
    # =============== Order Service =================
    @staticmethod
    def get_order():
        return requests.get(f"{ORDER_SERVICE_BASE_URL}/")

    # =============== Product Service ===============
    @staticmethod
    def get_product():
        return requests.get(f"{ORDER_SERVICE_BASE_URL}/")

    # =============== User Service ==================
    @staticmethod
    def get_user():
        return requests.get(f"{ORDER_SERVICE_BASE_URL}/")
