import requests
import json

# Налаштування URL-адрес для всіх сервісів
# (Зараз ми припускаємо, що вони на різних портах, як це зазвичай буває)
PRODUCT_SERVICE_URL = "http://127.0.0.1:8001"
ORDER_SERVICE_URL = "http://127.0.0.1:8002"
USER_SERVICE_URL = "http://127.0.0.1:8003"


class ServicesClient:


    # =======================================================
    #                   PRODUCT SERVICE
    # =======================================================
    @staticmethod
    def get_all_products():
        try:
            response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
            return response.json()
        except Exception as e:
            return f"Помилка з'єднання з Product Service: {e}"

    @staticmethod
    def get_user_products(owner_id):
        try:
            response = requests.get(f"{PRODUCT_SERVICE_URL}/products", params={"ownerId": owner_id})
            return response.json()
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def get_product_by_id(product_id):
        try:
            response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
            if response.status_code == 200:
                return response.json()
            return f"Помилка {response.status_code}: {response.text}"
        except Exception as e:
            return f"Помилка: {e}"

    @staticmethod
    def create_product():
        print("\n--- Створення нового товару ---")
        try:
            # Збираємо дані відповідно до вашої моделі ProductBase
            owner_id = int(input("ID власника (ownerId): "))
            title = input("Назва товару (title): ")
            description = input("Опис (description): ")
            price = float(input("Ціна (price): "))
            category = input("Категорія (category): ")
            quantity = int(input("Кількість (quantity): "))

            # Поля за замовчуванням (або можна теж запитати)
            status = "active"
            image_url = "http://example.com/default.jpg"

            new_data = {
                "ownerId": owner_id,
                "title": title,
                "description": description,
                "price": price,
                "category": category,
                "status": status,
                "quantity": quantity,
                "imageUrl": image_url
            }

            response = requests.post(f"{PRODUCT_SERVICE_URL}/products", json=new_data)
            return response.json()
        except ValueError:
            return "Помилка вводу: перевірте, чи ви ввели числа там, де потрібно."
        except Exception as e:
            return f"Помилка запиту: {e}"

    @staticmethod
    def delete_product(product_id):
        try:
            response = requests.delete(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
            return response.json()
        except Exception as e:
            return f"Помилка: {e}"

    # =======================================================
    #                   ORDER SERVICE
    # (Методи є, але в меню ми їх поки не додаємо)
    # =======================================================
    @staticmethod
    def get_all_orders():
        # Заготовка на майбутнє
        return requests.get(f"{ORDER_SERVICE_URL}/orders").json()

    @staticmethod
    def create_order(user_id, product_ids):
        # Заготовка
        data = {"user_id": user_id, "products": product_ids}
        return requests.post(f"{ORDER_SERVICE_URL}/orders", json=data).json()

    # =======================================================
    #                   USER SERVICE
    # (Методи є, але в меню ми їх поки не додаємо)
    # =======================================================
    @staticmethod
    def get_user_by_id(user_id):
        return requests.get(f"{USER_SERVICE_URL}/users/{user_id}").json()

    @staticmethod
    def create_user(username, password):
        data = {"username": username, "password": password}
        return requests.post(f"{USER_SERVICE_URL}/users", json=data).json()


# --- КОНСОЛЬНЕ МЕНЮ (Тільки для Product Service) ---

def run_console_menu():
    while True:
        print("\n================ МЕНЮ (PRODUCT SERVICE) ================")
        print("1. Показати всі товари")
        print("2. Знайти товари користувача (за ownerId)")
        print("3. Знайти товар за ID")
        print("4. Створити товар")
        print("5. Видалити товар")
        print("0. Вихід")
        print("========================================================")

        choice = input("Ваш вибір: ")

        if choice == "1":
            print(ServicesClient.get_all_products())

        elif choice == "2":
            uid = input("Введіть ownerId: ")
            if uid.isdigit():
                print(ServicesClient.get_user_products(int(uid)))
            else:
                print("ID має бути числом.")

        elif choice == "3":
            pid = input("Введіть ID товару: ")
            if pid.isdigit():
                print(ServicesClient.get_product_by_id(int(pid)))
            else:
                print("ID має бути числом.")

        elif choice == "4":
            result = ServicesClient.create_product()
            print("Результат:", result)

        elif choice == "5":
            pid = input("Введіть ID товару для видалення: ")
            if pid.isdigit():
                print(ServicesClient.delete_product(int(pid)))
            else:
                print("ID має бути числом.")

        elif choice == "0":
            print("Вихід.")
            break

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    run_console_menu()