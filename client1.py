import socket
import threading


def receive_messages(client_socket):
    """Отримує повідомлення від сервера в окремому потоці"""
    while True:
        try:
            message = client_socket.recv(8080).decode('utf-8')
            if message:
                print(f"\n{message}")
            else:
                print("\n🔌 Сервер закрив з'єднання")
                break
        except Exception as e:
            print(f"\n❌ Помилка: {e}")
            break


def start_chat_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Підключаємося до сервера
        client_socket.connect(('localhost', 8080))
        print("✅ Підключено до чат-бота!")

        # Вводимо ім'я
        username = input("Введіть ваше ім'я: ")
        client_socket.send(username.encode('utf-8'))

        print("\n📝 Почніть розмову з ботом! (напишіть 'вихід' щоб завершити)")
        print("💡 Спробуйте: автомобіль, собака, програмування, піца, футбол")
        print("-" * 50)

        # Запускаємо потік для отримання повідомлень
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        # Головний цикл для відправки повідомлень
        while True:
            message = input("Ваше повідомлення: ")

            if message.lower() == 'вихід':
                print("👋 До побачення!")
                break

            if message.strip():  # Відправляємо тільки непусті повідомлення
                client_socket.send(message.encode('utf-8'))

    except Exception as e:
        print(f"❌ Помилка підключення: {e}")
    finally:
        client_socket.close()
        print("🔌 З'єднання закрито")


if __name__ == "__main__":
    start_chat_client()