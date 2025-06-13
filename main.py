import requests
from pystyle import *
import os
import time
import threading

os.system("title Skid Tool")

def print_boxed_text(text_lines):
    max_len = max(len(line) for line in text_lines)
    top = "╔" + "═" * (max_len + 2) + "╗"
    bottom = "╚" + "═" * (max_len + 2) + "╝"
    lines = [top]
    for line in text_lines:
        lines.append("║ " + line.ljust(max_len) + " ║")
    lines.append(bottom)

    print(Colorate.Horizontal(Colors.cyan_to_blue, "\n".join(lines)))

def wait_key(prompt="Press Enter to continue..."):
    print(Colorate.Horizontal(Colors.cyan_to_blue, prompt))
    input()
    os.system("cls")

def get_webhook_info(webhook_url):
    try:
        response = requests.get(webhook_url)
        if response.status_code != 200:
            print(Colorate.Horizontal(Colors.cyan_to_blue,
                  f"Failed to fetch webhook info: {response.text}"))
            return
        data = response.json()
        lines = [
            "Webhook Information:",
            f"Name: {data.get('name')}",
            f"ID: {data.get('id')}",
            f"Channel ID: {data.get('channel_id')}",
            f"Guild ID: {data.get('guild_id')}",
            f"Avatar: {data.get('avatar')}"
        ]
        print_boxed_text(lines)
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"{e}"))

def spam_webhook(webhook_url, message, delay):
    stop_event = threading.Event()

    def wait_for_stop():
        input(Colorate.Horizontal(Colors.cyan_to_blue, "Press Enter to stop spamming..."))
        stop_event.set()

    threading.Thread(target=wait_for_stop, daemon=True).start()

    data = {"content": message}
    try:
        while not stop_event.is_set():
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                print(Colorate.Horizontal(Colors.cyan_to_blue, "Message sent!"))
            else:
                print(Colorate.Horizontal(Colors.cyan_to_blue, f"Failed to send message: {response.text}"))
                retry_after = response.json().get('retry_after')
                time.sleep(float(retry_after) + 0.5)
            time.sleep(delay)
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"Error sending message: {e}"))

    print(Colorate.Horizontal(Colors.cyan_to_blue, "Spam stopped."))

def delete_webhook(webhook_url):
    try:
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print(Colorate.Horizontal(Colors.cyan_to_blue, "Webhook deleted successfully."))
        else:
            print(Colorate.Horizontal(Colors.cyan_to_blue,f"Failed to delete webhook: {response.text}"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.cyan_to_blue, f"Error deleting webhook: {e}"))

def main():
    banner = """
                                               ╦═╗┌─┐┌─┐┌─┐  ╔═╗┬┌─┬┌┬┐┌─┐
                                               ╠╦╝├─┤├─┘├┤   ╚═╗├┴┐│ ││└─┐
                                               ╩╚═┴ ┴┴  └─┘  ╚═╝┴ ┴┴─┴┘└─┘
                                              ╔═══════════════════════════╗
                                              ║ [1] Info                  ║
                                              ║ [2] Spam                  ║
                                              ║ [3] Delete                ║
                                              ╚═══════════════════════════╝ 
                                              """
    while True:
        print(Colorate.Horizontal(Colors.cyan_to_blue, banner))
        optiontext = Colorate.Horizontal(Colors.cyan_to_blue, "Option (1-3): ")
        choice = input(optiontext)
        if choice not in ("1", "2", "3"):
            print(Colorate.Horizontal(Colors.cyan_to_blue, "Invalid option! Please enter 1, 2 or 3."))
            continue

        if choice == "1":
            webhook_url = input(Colorate.Horizontal(Colors.cyan_to_blue, "Enter webhook URL: "))
            get_webhook_info(webhook_url)
            wait_key()
        elif choice == "2":
            webhook_url = input(Colorate.Horizontal(Colors.cyan_to_blue, "Enter webhook URL: "))
            message = input(Colorate.Horizontal(Colors.cyan_to_blue, "Enter message to spam: "))
            delay_str = input(Colorate.Horizontal(Colors.cyan_to_blue, "Enter delay between messages (seconds, e.g. 1): "))
            try:
                delay = float(delay_str)
            except ValueError:
                delay = 1
            spam_webhook(webhook_url, message, delay)
            wait_key()
        elif choice == "3":
            webhook_url = input(Colorate.Horizontal(Colors.cyan_to_blue, "Enter webhook URL to delete: "))
            delete_webhook(webhook_url)
            wait_key()

if __name__ == "__main__":
    main()
