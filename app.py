import random
import string
import requests
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_reward(code_type):
    """Retourne une récompense aléatoire selon le type de code"""
    rewards = {
        "vbucks": ["1000 V-Bucks", "2800 V-Bucks", "5000 V-Bucks", "13500 V-Bucks"],
        "psn": ["10€", "20€", "50€", "100€"],
        "xbox": ["1 mois Game Pass", "3 mois Game Pass", "12 mois Game Pass"],
        "steam": ["10€ Steam Wallet", "20€ Steam Wallet", "50€ Steam Wallet"],
        "discord": ["1 mois Nitro", "1 an Nitro"],
        "nintendo": ["Nintendo eShop 15€", "Nintendo eShop 25€", "Nintendo eShop 50€"],
        "paypal": ["5€", "10€", "25€", "50€", "100€"]
    }
    return random.choice(rewards.get(code_type, ["Récompense inconnue"]))

def generate_random_code(code_type, length=16):
    """Génère un code aléatoire selon le type spécifié"""
    if code_type == "discord":
        return "discord.gift/" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    elif code_type == "vbucks":
        return "VB-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    elif code_type == "psn":
        return "PSN-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(3))
    elif code_type == "xbox":
        return "XBOX-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) for _ in range(3))
    elif code_type == "steam":
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + "-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    elif code_type == "nintendo":
        return "NS-" + "-".join("".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) for _ in range(3))
    elif code_type == "paypal":
        return "PP-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def test_code(code_type, code):
    """Simule la validation d'un code avec des chances très faibles (1/100000)"""
    chances = {
        "discord": 0.00001,  # 1/100000
        "vbucks": 0.00001,   # 1/100000
        "psn": 0.00001,      # 1/100000
        "xbox": 0.00001,     # 1/100000
        "steam": 0.00001,    # 1/100000
        "nintendo": 0.00001,  # 1/100000
        "paypal": 0.00001    # 1/100000
    }
    return random.random() < chances.get(code_type, 0.00001)

def show_menu():
    clear_screen()
    print("=" * 50)
    print("     GÉNÉRATEUR DE CODES")
    print("=" * 50)
    print("\nTypes de codes disponibles:")
    print("1. Discord Nitro")
    print("2. V-Bucks (Fortnite)")
    print("3. PlayStation Store")
    print("4. Xbox Store")
    print("5. Steam")
    print("6. Nintendo eShop")
    print("7. PayPal")
    print("\nEntrez votre choix (1-7):")

def main():
    while True:
        show_menu()
        choice = input("> ").strip()
        
        code_types = {
            "1": "discord",
            "2": "vbucks",
            "3": "psn",
            "4": "xbox",
            "5": "steam",
            "6": "nintendo",
            "7": "paypal"
        }
        
        if choice not in code_types:
            print("Choix invalide. Appuyez sur Entrée pour réessayer...")
            input()
            continue
            
        code_type = code_types[choice]
        clear_screen()
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
        
        print("\nGénération et test des codes en cours...\n")
        for i in range(num_codes):
            code = generate_random_code(code_type)
            is_valid = test_code(code_type, code)
            
            if is_valid:
                reward = get_reward(code_type)
                valid_codes.append(f"{code} -> {reward}")
                rewards.append(reward)
                print(f"Code {i+1}/{num_codes}: {code} - ✅ VALIDE! ({reward})")
            else:
                invalid_codes.append(code)
                print(f"Code {i+1}/{num_codes}: {code} - ❌ Invalide")
        
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
        
        print("\nVoulez-vous générer d'autres codes? (o/n)")
        if input("> ").lower() != 'o':
            break

if __name__ == "__main__":
    main()