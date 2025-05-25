import random
import string
import requests
import time
import os
import hashlib
from datetime import datetime
import concurrent.futures
import numpy as np
import re
from threading import Lock
import json

# Constantes de sécurité et raisons d'invalidité
SECURITY_CONSTANTS = {
    "MAX_ATTEMPTS": 1000000,
    "RATE_LIMIT": 10000,
    "SECURITY_LEVEL": "HIGH"
}

SECURITY_SETTINGS = {
    "proxy_rotation": True,
    "stealth_mode": True,
    "anti_detection": True,
    "geo_validation": True,
    "vulnerability_scan": True
}

INVALID_REASONS = [
    "Code expiré", "Format invalide", "Déjà utilisé",
    "Region incorrecte", "Code bloqué", "Limite dépassée",
    "Serveur indisponible", "Format non reconnu", 
    "IP blacklistée", "Compte suspendu"
]

# Configuration des forums hackeurs
HACKER_FORUMS = {
    "darknet_plaza": "Connexion au forum DarkNet Plaza...",
    "code_hunters": "Accès à CodeHunters Elite Forum...",
    "ghost_network": "Infiltration Ghost Network...",
    "cyber_shadows": "Connexion à CyberShadows Exchange...",
    "zero_day": "Connexion au Zero Day Market...",
    "shadow_net": "Accès à Shadow Network..."
}

HACKER_MESSAGES = [
    "Scan des vulnérabilités en cours...",
    "Rotation des proxies activée...",
    "Nouveaux serveurs détectés...",
    "Mise à jour des patterns de sécurité...",
    "Analyse des logs système en cours...",
    "Bypass de sécurité détecté...",
    "Nouveaux patterns identifiés...",
    "Base de données mise à jour...",
    "Connexion via tunnel sécurisé...",
    "Vérification des nœuds TOR..."
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_reward(code_type):
    """Retourne une récompense aléatoire selon le type de code"""
    rewards = {
        "vbucks": ["1000 V-Bucks", "2800 V-Bucks", "5000 V-Bucks", "13500 V-Bucks"],
        "psn": ["10€", "20€", "50€", "100€", "GTA V", "FIFA 24", "Spider-Man 2", "God of War Ragnarök", "FC24", 
                "Assassin's Creed Mirage", "Call of Duty MW3", "Resident Evil 4", "Final Fantasy XVI", 
                "Lies of P", "Mortal Kombat 1", "Street Fighter 6", "Armored Core VI"],
        "xbox": ["1 mois Game Pass", "3 mois Game Pass", "12 mois Game Pass", "Forza Horizon 5", "Starfield", 
                "Halo Infinite", "Diablo IV", "Sea of Thieves", "Hogwarts Legacy", "Hi-Fi Rush", "Forza Motorsport",
                "Minecraft Legends", "Redfall", "Pentiment", "Age of Empires IV"],
        "steam": [
            "10€", "20€", "50€", "100€", 
            "Red Dead Redemption 2", "Cyberpunk 2077", "Baldur's Gate 3",
            "Counter-Strike 2", "EA FC 24", "Lethal Company", "Elden Ring",
            "Dead Space Remake", "Resident Evil 4", "Street Fighter 6",
            "Cities: Skylines II", "Starfield", "Armored Core VI",
            "Lies of P", "Party Animals", "Mortal Kombat 1",
            "The Texas Chain Saw Massacre", "Remnant II", "Diablo IV",
            "Atomic Heart", "Hogwarts Legacy", "The Last of Us Part I",
            "Destiny 2: Lightfall", "Sons of the Forest", "Wo Long: Fallen Dynasty",
            "Star Wars Jedi: Survivor", "Alan Wake 2", "Starfield"
        ],
        "discord": ["1 mois Nitro", "1 an Nitro", "1 an Nitro + Boost", "3 mois Nitro"],
        "nintendo": ["15€", "25€", "50€", "Zelda: Tears of the Kingdom", "Super Mario Wonder", 
                    "Pokemon Écarlate/Violet", "Mario Kart 8", "Pikmin 4", "Advance Wars 1+2",
                    "Metroid Prime Remastered", "Fire Emblem Engage", "Octopath Traveler II",
                    "Bayonetta Origins", "Pokemon Stadium", "GoldenEye 007"],
        "paypal": ["5€", "10€", "25€", "50€", "100€", "250€", "500€"],
        "bitcoin": ["0.0001 BTC", "0.001 BTC", "0.01 BTC", "0.1 BTC"],
        "amazon": ["10€", "15€", "20€", "25€", "30€", "50€", "100€"],
        "ubisoft": ["10€", "20€", "50€", "AC Mirage", "Avatar", "The Crew Motorfest"],
        "epic": ["10€", "25€", "50€", "Fortnite OG Pack", "Alan Wake 2", "Lords of the Fallen"],
        "battlenet": ["20€", "50€", "Diablo IV", "Overwatch 2 Credits", "WoW Game Time", "CoD Points"],
        "gog": ["10€", "25€", "Cyberpunk 2077", "Baldur's Gate", "System Shock"]
    }
    return random.choice(rewards.get(code_type, ["Récompense inconnue"]))

def generate_random_code(code_type, length=16):
    """Génère un code aléatoire selon le type spécifié"""
    if code_type == "bitcoin":
        return "bc1" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(40))
    elif code_type == "amazon":
        return "AMZN-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(3))
    elif code_type == "ubisoft":
        return "UPLAY-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(4))
    elif code_type == "epic":
        return "EPIC-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) for _ in range(3))
    elif code_type == "battlenet":
        return "BNET-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(5))
    elif code_type == "gog":
        return "GOG-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    elif code_type == "discord":
        return "https://discord.gift/" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    elif code_type == "vbucks":
        return "https://fortnite.com/vbucks/" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    elif code_type == "psn":
        return "https://playstation.com/redeem/" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(4))
    elif code_type == "xbox":
        return "https://xbox.com/redeem/" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) for _ in range(5))
    elif code_type == "steam":
        return "https://store.steampowered.com/account/redeemwalletcode/" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
    elif code_type == "nintendo":
        return "https://nintendo.com/redeem/" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(4))
    elif code_type == "paypal":
        return "https://paypal.com/gifts/" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def test_code(code_type, code):
    """Version améliorée du test de code"""
    chances = {
        "discord": 0.00015,   # Amélioré à 1/6666
        "vbucks": 0.00012,    # 1/8333
        "psn": 0.00010,       # 1/10000
        "xbox": 0.00010,      # 1/10000
        "steam": 0.00008,     # 1/12500
        "nintendo": 0.00008,  # 1/12500
        "paypal": 0.00005,    # 1/20000
        "bitcoin": 0.000001,  # 1/1000000
        "amazon": 0.00007     # 1/14285
    }
    
    # Vérification de sécurité du format
    if not is_valid_format(code_type, code):
        return False, "Format invalide"
    
    is_valid = random.random() < chances.get(code_type, 0.00005)
    if not is_valid:
        return False, random.choice(INVALID_REASONS)
    return True, "Code valide"

def is_valid_format(code_type, code):
    """Vérifie le format du code selon son type"""
    patterns = {
        "discord": r"^https://discord\.gift/[A-Za-z0-9]{16}$",
        "vbucks": r"^https://fortnite\.com/vbucks/[A-Z0-9]{16}$",
        "psn": r"^https://playstation\.com/redeem/([A-Z0-9]{4}-){3}[A-Z0-9]{4}$",
        "xbox": r"^https://xbox\.com/redeem/([A-Z0-9]{5}-){5}[A-Z0-9]{5}$",
        "steam": r"^https://store\.steampowered\.com/account/redeemwalletcode/[A-Z0-9]{15}$",
        "nintendo": r"^https://nintendo\.com/redeem/([A-Z0-9]{4}-){3}[A-Z0-9]{4}$",
        "paypal": r"^https://paypal\.com/gifts/[A-Za-z0-9]{16}$",
        "bitcoin": r"^bc1[a-zA-Z0-9]{39,59}$",
        "amazon": r"^AMZN-([A-Z0-9]{4}-){2}[A-Z0-9]{4}$",
        "ubisoft": r"^UPLAY-([A-Z0-9]{4}-){3}[A-Z0-9]{4}$",
        "epic": r"^EPIC-([A-Z0-9]{5}-){2}[A-Z0-9]{5}$",
        "battlenet": r"^BNET-([A-Z0-9]{4}-){4}[A-Z0-9]{4}$",
        "gog": r"^GOG-[A-Z0-9]{20}$"
    }
    return bool(re.match(patterns.get(code_type, r".*"), code))

def show_menu():
    clear_screen()
    print("\033[95m╔" + "═" * 48 + "╗")
    print("║     \033[93mGÉNÉRATEUR DE CODES PREMIUM\033[95m     ║")
    print("╚" + "═" * 48 + "╝\033[0m")
    print("\n\033[96mTypes de codes disponibles:\033[0m")
    print("\033[97m1.  🎮 Discord Nitro")
    print("2.  💰 V-Bucks (Fortnite)")
    print("3.  🎯 PlayStation Store")
    print("4.  🟢 Xbox Store")
    print("5.  🎲 Steam")
    print("6.  🎌 Nintendo eShop")
    print("7.  💵 PayPal")
    print("8.  ₿ Bitcoin")
    print("9.  📦 Amazon")
    print("10. 🎯 Ubisoft Connect")
    print("11. 🎮 Epic Games Store")
    print("12. ⚔️ Battle.net")
    print("13. 🎲 GOG.com\033[0m")
    print("\n\033[93mEntrez votre choix (1-13):\033[0m")

def loading_animation(message, duration):
    """Animation plus rapide"""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(int(duration * 5)):  # Réduit de moitié
        for char in chars:
            print(f"\r\033[96m{char} {message}...\033[0m", end="")
            time.sleep(0.05)  # Réduit à 0.05s
    print()

def generate_secure_api_key():
    """Génère une clé API sécurisée"""
    key_parts = []
    for _ in range(4):
        part = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=8))
        key_parts.append(part)
    return '-'.join(key_parts)

def animate_decryption(encrypted, final):
    """Animation de décryptage améliorée"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_+=[]{}|;:,.<>?"
    max_len = max(len(encrypted), len(final))
    
    # Animation matrix-style
    for _ in range(3):
        for _ in range(5):
            scrambled = ''.join(random.choice(chars) for _ in range(max_len))
            print(f"\r\033[93m[DÉCRYPTAGE] {scrambled}\033[0m", end='')
            time.sleep(0.05)
    
    # Simulation du décryptage progressif
    result = list('?' * max_len)
    for i in range(max_len):
        for _ in range(3):
            result[i] = random.choice(chars)
            print(f"\r\033[93m[DÉCRYPTAGE] {''.join(result)}\033[0m", end='')
            time.sleep(0.02)
        if i < len(final):
            result[i] = final[i]
    print(f"\r\033[92m[DÉCRYPTÉ] {final}\033[0m")

def decrypt_api_url(encrypted):
    """Simule le décryptage d'une URL d'API avec animation"""
    # Tableau de conversion pour simuler un vrai décryptage
    conversion = {
        "bG9x8HPK2m4R": "discord-secure",
        "kJ9nM2pL4x7Y": "epic-network",
        "wQ5vB8mN3c6X": "psn-gateway",
        "tR4fD7hU9j2M": "xbox-live",
        "zS8gH1nP5v4Y": "steam-api",
        "yE3xC6kL8m2N": "nintendo-net",
        "aW7pH4nJ9f5K": "paypal-secure",
        "mK8dL3pH6n9J": "auth-master",
        "xK9pL4mN7j2H": "unknown-net"
    }
    
    parts = encrypted.split('.')
    decrypted_parts = []
    
    print(f"\n\033[96m[{time.strftime('%H:%M:%S')}] Début du décryptage de la clé API...\033[0m")
    
    # Décrypte chaque partie avec animation
    for part in parts:
        if part in conversion:
            animate_decryption(part, conversion[part])
            decrypted_parts.append(conversion[part])
        else:
            decrypted_parts.append(part)
        time.sleep(0.2)
    
    final_url = ".".join(decrypted_parts)
    print(f"\033[92m[{time.strftime('%H:%M:%S')}] Décryptage terminé: {final_url}\033[0m\n")
    return final_url

def simulate_api_connection(api_type):
    """Version avec décryptage animé"""
    encrypted_apis = {
        "discord": "bG9x8HPK2m4R.api-discord.gateway.secure",
        "vbucks": "kJ9nM2pL4x7Y.epic-auth.endpoint.secure",
        "psn": "wQ5vB8mN3c6X.playstation-verify.endpoint",
        "xbox": "tR4fD7hU9j2M.xbox-auth.live.secure",
        "steam": "zS8gH1nP5v4Y.steam-verify.endpoint",
        "nintendo": "yE3xC6kL8m2N.nintendo-auth.secure",
        "paypal": "aW7pH4nJ9f5K.paypal-gateway.secure",
        "auth": "mK8dL3pH6n9J.auth-gateway.secure"
    }
    
    encrypted = encrypted_apis.get(api_type, "xK9pL4mN7j2H.unknown-gateway.secure")
    server = decrypt_api_url(encrypted)
    connection_time = random.uniform(0.1, 10.0)  # Temps aléatoire entre 0.1 et 1 seconde
    start_time = time.time()
    
    print(f"\033[96m[{time.strftime('%H:%M:%S')}] Tentative de connexion à {server} (temps estimé: {connection_time:.2f}s)\033[0m")
    time.sleep(connection_time)
    
    if random.random() < 0.1:
        print(f"\033[91m[{time.strftime('%H:%M:%S')}] Erreur 429 - Trop de requêtes vers {server} ({connection_time:.2f}s)\033[0m")
        for i in range(3, 0, -1):
            print(f"\r\033[93mNouvelle tentative dans {i}s...\033[0m", end="")
            time.sleep(0.5)
        print("\n")
        return simulate_api_connection(api_type)
    
    elapsed = time.time() - start_time
    print(f"\033[92m[{time.strftime('%H:%M:%S')}] Connecté à {server} ✓ (ping: {elapsed:.3f}s)\033[0m")
    return True

def connection_status():
    """Simule une connexion/déconnexion aléatoire aux serveurs"""
    if random.random() < 0.000001:  # 0.0001% de chance (1 sur 1 million)
        print(f"\033[91m[{time.strftime('%H:%M:%S')}] Perte de connexion détectée\033[0m")
        for i in range(3, 0, -1):
            print(f"\r\033[93mTentative de reconnexion dans {i} secondes...\033[0m", end="")
            time.sleep(0.5)  # Réduit à 0.5s
        print("\n")
        loading_animation("Reconnexion aux serveurs", 1)  # Réduit à 1s
        if random.random() < 0.1:  # 10% de chance d'échec (plus rare)
            print(f"\033[91m[{time.strftime('%H:%M:%S')}] Échec de la connexion - Erreur 502\033[0m")
            loading_animation("Nouvelle tentative", 1)
        print(f"\033[92m[{time.strftime('%H:%M:%S')}] Connexion rétablie ✓\033[0m")

def create_logs_directory():
    """Crée le dossier logs s'il n'existe pas"""
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return logs_dir

def hash_code(code):
    """Hache un code avec SHA-256"""
    return hashlib.sha256(code.encode()).hexdigest()

def secure_write(filepath, content):
    """Écrit le contenu dans un fichier de manière sécurisée"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        # Hache le contenu pour vérification
        with open(filepath, "r", encoding="utf-8") as f:
            content_hash = hashlib.sha256(f.read().encode()).hexdigest()
        # Sauvegarde le hash dans un fichier séparé
        with open(f"{filepath}.hash", "w") as f:
            f.write(content_hash)
    except Exception as e:
        print(f"\033[91mErreur lors de l'écriture du fichier: {e}\033[0m")

def initialize_log_files(code_type, timestamp):
    """Initialise les fichiers de logs"""
    logs_dir = create_logs_directory()
    session_dir = os.path.join(logs_dir, f"session_{timestamp}")
    os.makedirs(session_dir, exist_ok=True)
    
    valid_path = os.path.join(session_dir, f"codes_valides_{code_type}.txt")
    invalid_path = os.path.join(session_dir, f"codes_invalides_{code_type}.txt")
    report_path = os.path.join(session_dir, f"rapport_{code_type}.txt")
    
    # Initialise les fichiers avec les en-têtes
    for path, header in [
        (valid_path, "=== CODES VALIDES ===\n"),
        (invalid_path, "=== CODES INVALIDES ===\n"),
        (report_path, f"Rapport de génération - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    ]:
        secure_write(path, header)
    
    return valid_path, invalid_path, report_path

def simulate_proxy_rotation():
    """Simule la rotation des proxies"""
    proxies = [f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(3)]
    print(f"\033[93m[PROXY] Rotation vers {random.choice(proxies)}\033[0m")

def activate_stealth_mode():
    """Active le mode furtif"""
    methods = ["Masquage des requêtes", "Randomisation des délais", "Rotation des User-Agents"]
    print(f"\033[94m[STEALTH] {random.choice(methods)}\033[0m")

def process_batch(batch_size, code_type, progress_lock):
    """Version améliorée avec affichage en temps réel"""
    codes = []
    with progress_lock:
        for i in range(batch_size):
            code = generate_random_code(code_type)
            is_valid, reason = test_code(code_type, code)
            
            if SECURITY_SETTINGS["proxy_rotation"] and i % 100 == 0:
                simulate_proxy_rotation()
            
            if SECURITY_SETTINGS["stealth_mode"] and i % 200 == 0:
                activate_stealth_mode()
            
            codes.append((code, is_valid, reason))
            print(f"\r\033[K\033[96mGénération: {i+1}/{batch_size}\033[0m", end="")
            
    return codes

def simulate_hacker_forum():
    """Simule la connexion à un forum de hackers"""
    forum = random.choice(list(HACKER_FORUMS.items()))
    print(f"\n\033[93m[FORUM] {forum[1]}\033[0m")
    loading_animation("Connexion", 1)
    time.sleep(0.5)
    print(f"\033[92m✓ Connecté à {forum[0]}\033[0m")
    
    for _ in range(random.randint(1, 3)):
        time.sleep(random.uniform(0.5, 2))
        message = random.choice(HACKER_MESSAGES)
        print(f"\033[96m[{time.strftime('%H:%M:%S')}] {message}\033[0m")

def main():
    while True:
        show_menu()
        simulate_api_connection("auth")
        simulate_hacker_forum()
        
        code_types = {
            "1": "discord", "2": "vbucks", "3": "psn",
            "4": "xbox", "5": "steam", "6": "nintendo",
            "7": "paypal", "8": "bitcoin", "9": "amazon",
            "10": "ubisoft", "11": "epic", "12": "battlenet",
            "13": "gog"
        }

        choice = input("> ").strip()
        
        if choice not in code_types:
            print("Choix invalide. Appuyez sur Entrée pour réessayer...")
            input()
            continue
            
        code_type = code_types[choice]
        clear_screen()
        simulate_api_connection(code_type)
        
        print(f"Génération de codes {code_type.upper()}")
        print("=" * 50)
        
        try:
            num_codes = int(input("\nCombien de codes voulez-vous générer? "))
            if num_codes <= 0:
                raise ValueError
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            input("\nAppuyez sur Entrée pour continuer...")
            continue
        
        valid_codes = []
        invalid_codes = []
        rewards = []
        
        # Initialisation des fichiers de logs
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        valid_path, invalid_path, report_path = initialize_log_files(code_type, timestamp)
        
        print(f"\n\033[95m[•] Génération et test des codes en cours...\033[0m")
        print(f"\033[96m[i] Temps estimé: {num_codes * 0.02:.1f} secondes\033[0m\n")
        start_gen = time.time()
        
        # Création du rapport en temps réel
        with open(report_path, "a") as report:
            report.write(f"Type de code: {code_type.upper()}\n")
            report.write(f"Nombre total de codes à générer: {num_codes}\n\n")
        
        progress_lock = Lock()
        total_processed = 0
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            batch_size = min(1000, num_codes // 4)  # Taille de lot optimisée
            futures = []
            
            while total_processed < num_codes:
                current_batch_size = min(batch_size, num_codes - total_processed)
                future = executor.submit(process_batch, current_batch_size, code_type, progress_lock)
                futures.append(future)
                total_processed += current_batch_size
                
                # Contrôle de vitesse
                elapsed = time.time() - start_time
                if elapsed > 0:
                    rate = total_processed / elapsed
                    if rate > SECURITY_CONSTANTS["RATE_LIMIT"]:
                        time.sleep(0.1)
            
            for future in concurrent.futures.as_completed(futures):
                for code, is_valid, reason in future.result():
                    hashed_code = hash_code(code)
                    
                    if is_valid:
                        reward = get_reward(code_type)
                        entry = f"{code} -> {reward} (Hash: {hashed_code})\n"
                        with open(valid_path, "a") as f:
                            f.write(entry)
                        rewards.append(reward)
                        print(f"\033[92m✓ Code {len(valid_codes)+len(invalid_codes)+1}/{num_codes}: {code} - VALIDE! ({reward})\033[0m")
                    else:
                        with open(invalid_path, "a") as f:
                            f.write(f"{code} (Hash: {hashed_code}) - Raison: {reason}\n")
                        print(f"\033[91m✗ {code} - {reason}\033[0m")
        
        # Finalisation du rapport
        total_time = time.time() - start_gen
        with open(report_path, "a") as report:
            report.write(f"Temps total: {total_time:.1f} secondes\n")
            report.write(f"Vitesse moyenne: {num_codes/total_time:.1f} codes/seconde\n\n")
            if rewards:
                report.write("Récompenses trouvées:\n")
                for reward in set(rewards):
                    count = rewards.count(reward)
                    report.write(f"- {reward} x{count}\n")
        
        print(f"\n\033[92mGénération terminée en {total_time:.1f} secondes!\033[0m")
        print(f"\033[96mVitesse moyenne: {num_codes/total_time:.1f} codes/seconde\033[0m")
        
        loading_animation("Déconnexion du serveur", 2)
        print("✅ Session terminée")
        
        # Enregistrement et résumé
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        if valid_codes:
            with open(f"codes_valides_{code_type}_{timestamp}.txt", "w") as f:
                f.write("\n".join(valid_codes))
            
            print("\n🎉 Récapitulatif des gains:")
            for reward in set(rewards):
                count = rewards.count(reward)
                print(f"- {reward} x{count}")
        
        print(f"\nCodes valides: {len(valid_codes)}/{num_codes}")
        print(f"Les résultats ont été sauvegardés dans les fichiers correspondants.")
        
        # Calcul des statistiques finales
        stats = {
            "total_codes": num_codes,
            "valid_codes": len(valid_codes),
            "invalid_codes": len(invalid_codes),
            "generation_time": total_time,
            "codes_per_second": num_codes/total_time,
            "rewards": [r for r in rewards if r],
            "timestamp": timestamp,
            "code_type": code_type
        }
        
        # Sauvegarde des stats
        stats_file = f"stats_{timestamp}.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=4)
        
        print("\nVoulez-vous générer d'autres codes? (o/n)")
        if input("> ").lower() != 'o':
            break

if __name__ == "__main__":
    main()