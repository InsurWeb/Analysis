# Analysis Bot

Analysis Bot est un bot Telegram conçu pour effectuer diverses analyses et recherches à partir de sources publiques et d'API externes.

## Fonctionnalités

- **Commandes disponibles** : Le bot prend en charge plusieurs commandes pour effectuer des analyses, des recherches et des actions administratives.
- **Vérification des crédits** : Certaines commandes nécessitent des crédits. Le bot vérifie automatiquement les crédits de l'utilisateur avant d'exécuter ces commandes.
- **Accès administrateur** : Certaines commandes sont réservées aux administrateurs du bot.
- **Enregistrement des journaux** : Toutes les commandes et les événements importants sont enregistrés dans les journaux pour un suivi ultérieur.

## Commandes disponibles

- `/start` : Démarre le bot et affiche un message de bienvenue.
- `/help` : Affiche la liste des commandes disponibles et leurs descriptions.
- `/myid` : Voir son id.
- `/admin` : Affiche toutes les commandes administratives disponibles (réservées aux administrateurs).

## Configuration requise

- **Python** : Le bot est écrit en Python. Assurez-vous d'avoir Python installé sur votre système.
- **Bibliothèque Telebot** : Le bot utilise la bibliothèque Telebot pour interagir avec l'API Telegram. Vous pouvez l'installer en exécutant `pip install telebot`.

## Utilisation

1. Clonez ce dépôt sur votre machine locale.
2. Configurez votre jeton d'API Telegram dans le fichier `main.py`.
3. Exécutez le script `main.py` pour démarrer le bot.
4. Commencez à interagir avec le bot en utilisant les commandes disponibles.

## Auteur

- Bot créé par [Insur](https://github.com/InsurWeb).

## Licence

Ce projet est sous licence MIT.
