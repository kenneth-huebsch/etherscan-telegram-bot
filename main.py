import etherscan_client
import telegram_client
import threading


def start_etherscanning():
    telegram_client.send_start_message()
    while(1):
        try:
            updates = etherscan_client.check_for_updates()
            if len(updates) > 0:
                telegram_client.send_updates_to_channel(updates)
        except Exception as e:
            error_message = f"<strong>Warning: Exception recieved from etherscan thread: </strong>\n {str(e)}\n Continuing..."
            print(error_message)

def main() -> None:
    print("Starting Etherscan thread...")
    thread = threading.Thread(target=start_etherscanning)
    thread.start()
    print("Telegram bot listener is starting...")
    telegram_client.start_bot()

if __name__ == '__main__':
    main()