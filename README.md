# AzureEnum
Ce script Python permet d’énumérer des utilisateurs d’un domaine Azure AD et de brute force des mots de passe sur un ou plusieurs comptes.
Il utilise les endpoints publics Microsoft pour vérifier l’existence des utilisateurs et tenter une connexion avec un mot de passe.


# Fonctionnalités :
- Récupération automatique du tenant Azure AD à partir du domaine
- Énumération interactive des utilisateurs à partir d’une wordlist
- Brute force de mot de passe sur un utilisateur ou plusieurs utilisateurs
- Support d’un mot de passe unique ou d’une wordlist de mots de passe
- Sauvegarde des résultats d’énumération dans un fichier JSON horodaté

