# final_project_POO


# Utilisation de Github pour travailler de manière collaborative 
# Lien : https://github.com/noegrm/final_project_POO

Développé par : SOMASSOUNDARAME Srijan, MFABOUM Anaïs, GERME Noé, RICHARD Alexia 

Projet POO – Système Bancaire en Python

Présentation du projet :

Ce projet consiste à développer un  "système bancaire" en Python en utilisant les principes de la programmation orientée objet vu en cours.

Le programme fonctionne en ligne de commande et permet de se connecter soit en tant que client, soit en tant qu’administrateur, avec des fonctionnalités différentes selon le rôle.

## Concepts de programmation utilisés

Dans le projet on retrouve ce qu'on a vu en cours : 

* Programmation Orientée Objet
* Encapsulation (attributs protégés / privés)
* Héritage
* Polymorphisme
* Attributs et méthodes de classe
* Gestion d’un menu en console
* Séparation claire des responsabilités entre les classes

---

## Organisation du projet

Nous avons décide de mettre le code dans un seuk fichier nommé bank_system.py

## Imports utilisés

Voici les principaux modules importés et leur utilité :

- datetime : permet de gérer les dates (création des comptes, horodatage des transactions)
- getpass: permet de cacher le mot de passe lors de la saisie dans le terminal (selon l’environnement)


## Gestion des utilisateurs

1.Classe `User`

Classe de base pour tous les utilisateurs du système.

Attributs :
`username` : nom d’utilisateur
`_password` : mot de passe (protégé et utilisation de getpass pour ne pas voir quand l'utilisateur tape)
`role` : type d’utilisateur (admin ou client)

Méthodes :

`check_password()` : vérifie si le mot de passe est correct

### Classe `Client` (hérite de `User`)

Représente un client de la banque.

Attributs supplémentaires :

`accounts` : liste des comptes bancaires du client

Méthodes :
`add_account()` : ajoute un compte au client
`list_accounts()` : retourne la liste des comptes

## Classe `Admin` (hérite de `User`)

Représente un administrateur du système.

L’administrateur peut :

- créer des clients
- créer des comptes
- geler/dégeler des comptes
- lancer le traitement mensuel
- consulter toutes les transactions

Gestion des comptes bancaires

### Classe `Account`

Classe de base pour tous les comptes bancaires.

Attributs principaux :

-`account_id` : identifiant unique du compte
-`owner` : propriétaire du compte
-`__balance` : solde du compte (privé)
-`is_frozen` : indique si le compte est gelé
-`created_at` : date de création

Méthodes :

- `deposit()` : dépôt d’argent
- `withdraw()` : retrait d’argent
- `get_balance()` : retourne le solde
- `freeze()` / `unfreeze()` : gèle ou dégèle le compte
- `apply_monthly_process()` : méthode prévue pour être redéfinie

### Classe `CurrentAccount` (hérite de `Account`)

Compte courant avec des **frais mensuels**.

- Un montant fixe est retiré chaque mois
- La méthode `apply_monthly_process()` est redéfinie

### Classe `SavingsAccount` (hérite de `Account`)

Compte épargne avec intérêts mensuels (même si dans notre cas on ne peut pas vraiment le faire donc on enlève 5euros à la création du compte"

- Un pourcentage d’intérêt est ajouté chaque mois
- Utilise également le polymorphisme avec `apply_monthly_process()`

## Gestion des transactions

### Classe `Transaction`

Chaque opération bancaire génère une transaction.

Attributs :

- `transaction_id` : identifiant unique
- `timestamp` : date et heure
- `transaction_type` : dépôt, retrait, virement, système
- `amount` : montant concerné
- `status` : succès ou échec
- `description` : description de l’opération
- `source_account` / `destination_account` : comptes concernés

Même les opérations échouées sont enregistrées, ce qui permet une traçabilité complète. Commme ça nous les voyons dans l'historiques.

## 🏛️ Classe centrale `BankSystem`

C’est la classe principale qui gère tout le fonctionnement du programme.

Responsabilités :

- gestion des utilisateurs
- gestion des comptes
- gestion des transactions
- authentification
- affichage des menus
- logique métier

Le programme démarre depuis cette classe.

## 🧪 Données de démonstration

Au lancement du programme, des données sont déjà créées :

Administrateur :

  -identifiant : `admin`
  - mot de passe : `admin123`

Client :

- identifiant : `alice`
-  mot de passe : `alice123`

 Comptes pour Alice :

1 compte courant
1 compte épargne

Cela permet de tester directement le programme sans créer de données manuellement.


## Lancement du programme

Dans le terminal :


python3 bank_system.py

