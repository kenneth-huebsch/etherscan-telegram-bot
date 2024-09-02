import etherscan_client
import telegram_client
import global_vars
import time
from datetime import datetime, timedelta
import threading


def start_etherscanning():
    last_check = datetime.now() - timedelta(seconds=global_vars.POLL_TIME_SECONDS)
    telegram_client.send_start_message()
    while(1):
        try:
            updates = etherscan_client.check_for_updates_since(last_check)
            last_check = datetime.now()
            if len(updates) > 0:
                telegram_client.send_updates_to_channel(updates)

        except Exception as e:
            error_message = f"<strong>Error: </strong> {str(e)}\n Etherscan bot is shutting down."
            telegram_client.send_message_to_channel(error_message)
            raise e

        time.sleep(global_vars.POLL_TIME_SECONDS)

def main() -> None:
    print("Starting Etherscan thread...")
    thread = threading.Thread(target=start_etherscanning)
    thread.start()
    
    print("Telegram bot listener is starting...")
    telegram_client.start_bot()

if __name__ == '__main__':
    main()