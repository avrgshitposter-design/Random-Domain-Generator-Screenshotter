import os
import random
import string
import requests
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot
import time

TELEGRAM_TOKEN = "ТВОЙ БОТ ТОКЕН"
CHAT_ID = "ТВОЙ ЧАТ АЙДИ"
OUTPUT_DIR = "photos"
DOMAINS_FILE = "found.txt"

ZONES = [".com", ".net", ".org", ".xyz", ".online", ".info", ".site"]

init(autoreset=True)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def random_domain():
    length = random.randint(4, 12)
    name = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    return name + random.choice(ZONES)


def check_domain(domain):
    print(Fore.YELLOW + f"[Проверка] {domain}")
    try:
        r = requests.get("http://" + domain, timeout=5)
        if r.status_code == 200:
            print(Fore.GREEN + f"[Найден] ✅🌐 {domain}")
            return True
    except:
        print(Fore.RED + f"[Ошибка] {domain} не отвечает")
    return False


def take_screenshot(domain):
    print(Fore.BLUE + f"[Скриншот] {domain}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(" --enable-unsafe-swiftshader")

    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(1280, 720)
        driver.get("http://" + domain)
        time.sleep(3)
        filename = os.path.join(OUTPUT_DIR, f"{domain}.png")
        driver.save_screenshot(filename)
        driver.quit()
        return filename
    except Exception as e:
        driver.quit()
        print(Fore.RED + f"[Ошибка скриншота] {e}")
        return None


def send_to_telegram(domain, screenshot):
    try:
        print(Fore.BLUE + f"[Отправка в Telegram] {domain}")
        with open(screenshot, "rb") as photo:
            bot.send_photo(CHAT_ID, photo, caption=f"🌐 Домен найден! ✅\n{domain}")
    except Exception as e:
        print(Fore.RED + f"[Ошибка Telegram] {e}")


def main():
    while True:
        domain = random_domain()
        if check_domain(domain):
            with open(DOMAINS_FILE, "a") as f:
                f.write(domain + "\n")
            screenshot = take_screenshot(domain)
            if screenshot:
                send_to_telegram(domain, screenshot)


if __name__ == "__main__":
    main()
