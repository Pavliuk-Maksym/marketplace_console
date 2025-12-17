import requests


PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"
ORDER_SERVICE_URL = "http://127.0.0.1:8002"
USER_SERVICE_URL = "http://127.0.0.1:8003"
DISCOVERY_SERVICE_URL = "http://127.0.0.1:8000"

GATEWAY_URL = "http://127.0.0.1:8080"

current_user = None


class ServicesClient:

    @staticmethod
    def get_all_products():
        try:
            response = requests.get(f"{GATEWAY_URL}/products")
            return response.json()
        except Exception as e:
            return f"Помилка з'єднання з Product Service: {e}"

    @staticmethod
    def get_user_products(owner_id):
        try:
            response = requests.get(
                f"{GATEWAY_URL}/products", params={"ownerId": owner_id}
            )
            return response.json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def get_product_by_id(product_id):
        try:
            response = requests.get(f"{GATEWAY_URL}/products/{product_id}")
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def create_product():
        if not current_user:
            return "Потрібна авторизація"

        print("\n--- Створення нового товару ---")
        try:
            new_data = {
                "ownerId": current_user["id"],
                "title": input("Назва: "),
                "description": input("Опис: "),
                "price": float(input("Ціна: ")),
                "category": input("Категорія: "),
                "status": "active",
                "quantity": int(input("Кількість: ")),
                "imageUrl": "http://example.com/default.jpg",
            }

            response = requests.post(f"{GATEWAY_URL}/products", json=new_data)
            return response.json()
        except ValueError:
            return "Помилка вводу: перевірте, чи ви ввели числа там, де потрібно."
        except Exception as e:
            return f"Помилка запиту: {e}"

    @staticmethod
    def delete_product(product_id):
        product = ServicesClient.get_product_by_id(product_id)

        if not isinstance(product, dict):
            return "Товар не знайдено"

        if product["ownerId"] != current_user["id"]:
            return "Ви не можете видаляти чужий товар"

        return requests.delete(f"{GATEWAY_URL}/products/{product_id}").json()

    @staticmethod
    def get_user_orders(user_id):
        try:
            return requests.get(f"{GATEWAY_URL}/orders/users/{user_id}").json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def find_order_by_id(order_id):
        try:
            return requests.get(f"{GATEWAY_URL}/orders/{order_id}").json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def create_order_console():
        print("Введіть ID товару для замовлення:")
        pid = input().strip()
        if not pid.isdigit():
            print("ID товару має бути числом")
            return

        product_id = int(pid)
        order_payload = {"buyerId": current_user["id"], "productId": product_id}

        try:
            response = requests.post(f"{GATEWAY_URL}/orders", json=order_payload)
            if response.status_code == 200:
                print("Замовлення створено:", response.json())
            else:
                print(f"Помилка {response.status_code}: {response.text}")
        except Exception as e:
            print("Помилка запиту:", e)

    @staticmethod
    def update_order_status(order_id, status):
        order = ServicesClient.find_order_by_id(order_id)
        if not order or order.get("buyerId") != current_user["id"]:
            return "Ви не можете змінювати чужі замовлення!"
        try:
            return requests.put(f"{GATEWAY_URL}/orders/{order_id}/{status}").json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def cancel_order(order_id):
        order = ServicesClient.find_order_by_id(order_id)
        if not order or order.get("buyerId") != current_user["id"]:
            return "Ви не можете відміняти чужі замовлення!"
        try:
            return requests.delete(f"{GATEWAY_URL}/orders/{order_id}").json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def get_user_by_id(user_id):
        try:
            response = requests.get(f"{GATEWAY_URL}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def create_user(user_data):
        try:
            response = requests.post(f"{GATEWAY_URL}/users", json=user_data)
            if response.status_code in (200, 201):
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def list_users():
        try:
            response = requests.get(f"{GATEWAY_URL}/users")
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def update_user(user_id, updates):
        try:
            user_id = current_user["id"]
            response = requests.put(f"{GATEWAY_URL}/users/{user_id}", json=updates)
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def delete_user(user_id):
        try:
            response = requests.delete(f"{GATEWAY_URL}/users/{user_id}")
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def update_current_user(updates):
        return ServicesClient.update_user(current_user["id"], updates)

    @staticmethod
    def delete_current_user():
        return ServicesClient.delete_user(current_user["id"])

    @staticmethod
    def login(username: str, password: str):
        global current_user

        users = ServicesClient.list_users()
        if not isinstance(users, list):
            return "Помилка отримання користувачів"

        for u in users:
            if u["username"] == username and u.get("password") == password:
                current_user = u
                return f"Ви увійшли як {u['username']}"

        return "Невірний логін або пароль"

    @staticmethod
    def logout():
        global current_user
        current_user = None
        return "Ви вийшли з акаунту"

    @staticmethod
    def whoami():
        if current_user:
            return current_user
        return "Користувач не авторизований"

    @staticmethod
    def get_openapi_contract():
        return (
            requests.get(f"{PRODUCT_SERVICE_URL}/openapi.json").json(),
            requests.get(f"{ORDER_SERVICE_URL}/openapi.json").json(),
            requests.get(f"{USER_SERVICE_URL}/openapi.json").json(),
            requests.get(f"{DISCOVERY_SERVICE_URL}/openapi.json").json(),
            requests.get(f"{GATEWAY_URL}/openapi.json").json(),
        )


current_user = None


def auth_menu():
    global current_user
    while not current_user:
        print("\n=== АВТОРИЗАЦІЯ / РЕЄСТРАЦІЯ ===")
        print("1. Реєстрація")
        print("2. Вхід (login)")
        print("3. Отримати OpenAPI Контракт")
        print("0. Вихід")
        choice = input("Ваш вибір: ")

        if choice == "1":
            username = input("Username: ")
            email = input("Email: ")
            full_name = input("Full name: ")
            password = input("Password: ")

            user = {
                "username": username,
                "email": email,
                "fullName": full_name,
                "password": password,
            }
            print(ServicesClient.create_user(user))

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            print(ServicesClient.login(username, password))
        elif choice == "3":
            (
                product_contract,
                order_contract,
                user_contract,
                discovery_contract,
                gateway_contract,
            ) = ServicesClient.get_openapi_contract()
            print(
                "=============================== PRODUCT CONTRACT ==============================="
            )
            print(product_contract)
            print(
                "=============================== ORDER CONTRACT ================================="
            )
            print(order_contract)
            print(
                "=============================== USER CONTRACT =================================="
            )
            print(user_contract)
            print(
                "=============================== DISCOVERY CONTRACT ============================="
            )
            print(discovery_contract)
            print(
                "=============================== GATEWAY CONTRACT ==============================="
            )
            print(gateway_contract)

        elif choice == "0":
            print("Вихід.")
            exit()

        else:
            print("Невідома команда.")


def app_menu():
    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ ===")
        print("=== PRODUCT SERVICE ===")
        print("1. Показати всі товари")
        print("2. Показати мої товари")
        print("3. Знайти товар за ID")
        print("4. Створити товар")
        print("5. Видалити свій товар")
        print("\n=== ORDER SERVICE ===")
        print("6. Показати мої замовлення")
        print("7. Створити замовлення")
        print("8. Знайти замовлення за ID")
        print("9. Оновити статус замовлення")
        print("10. Відмінити замовлення")
        print("\n=== USER SERVICE ===")
        print("11. Показати мої дані")
        print("12. Оновити мої дані")
        print("13. Вихід (logout)")
        print("0. Вихід")
        choice = input("Ваш вибір: ")

        if choice == "1":
            print(ServicesClient.get_all_products())

        elif choice == "2":
            print(ServicesClient.get_user_products(current_user["id"]))

        elif choice == "3":
            pid = input("Введіть ID товару: ")
            if pid.isdigit():
                print(ServicesClient.get_product_by_id(int(pid)))
            else:
                print("ID має бути числом.")

        elif choice == "4":
            ServicesClient.create_product()

        elif choice == "5":
            pid = input("ID вашого товару для видалення: ")
            if pid.isdigit():
                print(ServicesClient.delete_product(int(pid)))
            else:
                print("ID має бути числом.")

        elif choice == "6":
            print(ServicesClient.get_user_orders(current_user["id"]))

        elif choice == "7":
            ServicesClient.create_order_console()

        elif choice == "8":
            oid = input("ID замовлення: ")
            if oid.isdigit():
                order = ServicesClient.find_order_by_id(int(oid))
                if order.get("buyerId") != current_user["id"]:
                    print("Це не ваше замовлення!")
                else:
                    print(order)
            else:
                print("ID має бути числом.")

        elif choice == "9":
            oid = input("ID замовлення: ")
            status = input("Новий статус: ")
            if oid.isdigit():
                order = ServicesClient.find_order_by_id(int(oid))
                if order.get("buyerId") != current_user["id"]:
                    print("Ви не можете змінювати чужі замовлення!")
                else:
                    print(ServicesClient.update_order_status(int(oid), status))
            else:
                print("ID має бути числом.")

        elif choice == "10":
            oid = input("ID замовлення для відміни: ")
            if oid.isdigit():
                order = ServicesClient.find_order_by_id(int(oid))
                if order.get("buyerId") != current_user["id"]:
                    print("Ви не можете відміняти чужі замовлення!")
                else:
                    print(ServicesClient.cancel_order(int(oid)))
            else:
                print("ID має бути числом.")

        elif choice == "11":
            print(current_user)

        elif choice == "12":
            username = input("Новий username (залиште порожнім щоб не змінювати): ")
            email = input("Новий email (залиште порожнім щоб не змінювати): ")
            full_name = input("Новий fullName (залиште порожнім щоб не змінювати): ")
            updates = {}
            if username:
                updates["username"] = username
            if email:
                updates["email"] = email
            if full_name:
                updates["fullName"] = full_name
            if updates:
                print(ServicesClient.update_user(current_user["id"], updates))
            else:
                print("Немає змін.")

        elif choice == "13":
            print(ServicesClient.logout())
            auth_menu()

        elif choice == "0":
            print("Вихід.")
            break

        else:
            print("Невідома команда.")


def run_console_menu():
    while True:
        auth_menu()
        app_menu()


if __name__ == "__main__":
    run_console_menu()
