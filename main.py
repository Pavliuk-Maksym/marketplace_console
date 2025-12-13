import requests

BASE_URL = "http://127.0.0.1:8000"

ORDER_SERVICE_BASE_URL = f"{BASE_URL}/orders"
PRODUCT_SERVICE_BASE_URL = f"{BASE_URL}/products"
USER_SERVICE_BASE_URL = f"{BASE_URL}/users"


class Console:
    # =============== Order Service =================
    @staticmethod
    def get_order():
        return requests.get(f"{ORDER_SERVICE_BASE_URL}/")

    # =============== Product Service ===============
    @staticmethod
    def get_product():
        return requests.get(f"{PRODUCT_SERVICE_BASE_URL}/")

    # =============== User Service ==================
    @staticmethod
    def get_user():
        return requests.get(f"{USER_SERVICE_BASE_URL}/")

    # =============== OpenAPI Contract ==============
    @staticmethod
    def get_openapi_contract():
        return requests.get(f"{BASE_URL}/openapi.json").json()
