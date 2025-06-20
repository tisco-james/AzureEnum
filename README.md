# AzureEnum
Ce script Python permet d’énumérer des utilisateurs d’un domaine Azure AD et de brute force des mots de passe sur un ou plusieurs comptes.
Il utilise les endpoints publics Microsoft pour vérifier l’existence des utilisateurs et tenter une connexion avec un mot de passe.


# Fonctionnalités :
- Récupération automatique du tenant Azure AD à partir du domaine
- Énumération interactive des utilisateurs à partir d’une wordlist
- Brute force de mot de passe sur un utilisateur ou plusieurs utilisateurs
- Support d’un mot de passe unique ou d’une wordlist de mots de passe
- Sauvegarde des résultats d’énumération dans un fichier JSON horodaté



# Notes :
- Le script utilise un client public Azure CLI pour les requêtes OAuth.
- L’énumération vérifie uniquement l’existence des comptes.
- Le brute force tente une connexion OAuth avec les identifiants fournis.
- Utiliser ce script uniquement sur des environnements et domaines dont vous avez l’autorisation.


# Pour exécuter le script depuis la ligne de commande
- Exemple si ton script s’appelle azure.py :
python3 azure.py domaine.fr
- Pour énumérer les utilisateurs (interactif) :
python3 azure.py domaine.fr
(Le script te demandera si tu veux énumérer et le chemin de la wordlist.)
- Pour bruteforcer un utilisateur avec un mot de passe unique :
python3 azure.py domaine.fr -u utilisateur -p motdepasse
- Pour bruteforcer un utilisateur avec une wordlist de mots de passe :
python3 azure.py domaine.fr -u utilisateur -p wordlist_mdp.txt
- Pour bruteforcer plusieurs utilisateurs (wordlist) avec un mot de passe unique :
python3 azure.py domaine.fr -u wordlist_users.txt -p motdepasse
- Pour bruteforcer plusieurs utilisateurs et plusieurs mots de passe (les deux wordlists) :
python3 azure.py domaine.fr -u wordlist_users.txt -p wordlist_passwords.txt
