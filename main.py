import requests
import time
import json
import threading
from playsound import playsound


# Some pre-defined constants
interval = 60


# Collecting user data
number_of_urls = int(input("Введите количество ссылок (число), по которым будет происходить мониторинг: "))
json_url_array = []

for i in range(number_of_urls):
    url = input("Введите ссылку, по которой будет проходить мониторинг билетов: ").strip()

    # Format to JSON URL
    splitted_url = url.split("/")
    company_id = splitted_url[4]
    show_id = splitted_url[6]
    event_id = splitted_url[7]
    json_url = f"https://widget.profticket.ru/api/event/schedule-item/?company_id={company_id}&show_id={show_id}&event_id={event_id}"

    json_url_array.append(json_url)


def work(url):
    """ Requesting JSON data (free seats) """
    print("Запускаем мониторинг: " + url) 

    while True:
        try:
            # Sending requests in order to get two responses (old and new)
            response = requests.get(url)
            json_data = json.loads(response.text)
            number_of_seats = json_data["response"]["event"]["free_places_count"]

            time.sleep(interval)

            response = requests.get(url)
            json_data = json.loads(response.text)
            new_number_of_seats = json_data["response"]["event"]["free_places_count"]

            if new_number_of_seats > number_of_seats:
                print("Новые билеты по " + url)

                for i in range(3):
                    playsound("success.mp3")
                    time.sleep(1) 
        except Exception:
            print("\n\n!!!ВОЗНИКЛА НЕИЗВЕСТНАЯ ОШИБКА!!!")

            for i in range(5):
                playsound("error.mp3")
                time.sleep(1)

            exit()


# Spawning our threads
for i in json_url_array:
    t = threading.Thread(target=work, args=(i,))
    t.start()
    time.sleep(1)
