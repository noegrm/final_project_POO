from datetime import datetime


# =========================================================
# Projet POO – Système Bancaire
# Fichier : bank_system.py
# =========================================================


# ---------------------------------------------------------
# CLASSES UTILISATEURS
# ---------------------------------------------------------

class User:
    """
    Classe de base représentant un utilisateur du système.
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self._password = password  # attribut protégé
        self.role = "user"

    def check_password(self, password: str) -> bool:
        """
        Vérifie si le mot de passe fourni est correct.
        """
        return self._password == password

    def __str__(self):
        return f"Utilisateur : {self.username} ({self.role})"


class Client(User):
    """
    Classe représentant un client de la banque.
    Hérite de User.
    """

    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "client"
        self.accounts = []  # liste des comptes du client

    def add_account(self, account):
        self.accounts.append(account)

    def list_accounts(self):
        return self.accounts


class Admin(User):
    """
    Classe représentant un administrateur.
    Hérite de User.
    """

    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "admin"

# ---------------------------------------------------------
# CLASSES COMPTES BANCAIRES
# ---------------------------------------------------------

class Account:
    """
    Classe de base pour un compte bancaire.
    """

    _account_counter = 1  # attribut de classe pour générer les IDs

    def __init__(self, owner_username: str, initial_balance: float = 0.0):
        self.account_id = f"ACC{Account._account_counter:04d}"
        Account._account_counter += 1

        self.owner = owner_username
        self.__balance = initial_balance  # 🔒 attribut privé
        self.is_frozen = False
        self.created_at = datetime.now()

    # -----------------------------
    # Méthodes protégées / publiques
    # -----------------------------

    def get_balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> bool:
        if self.is_frozen:
            print("❌ Compte gelé. Dépôt impossible.")
            return False

        if amount <= 0:
            print("❌ Montant invalide.")
            return False

        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        if self.is_frozen:
            print("❌ Compte gelé. Retrait impossible.")
            return False

        if amount <= 0:
            print("❌ Montant invalide.")
            return False

        if amount > self.__balance:
            print("❌ Solde insuffisant.")
            return False

        self.__balance -= amount
        return True

    def freeze(self):
        self.is_frozen = True

    def unfreeze(self):
        self.is_frozen = False

    def apply_monthly_process(self):
        """
        Méthode destinée à être redéfinie (polymorphisme).
        """
        pass

    def __str__(self):
        status = "Gelé" if self.is_frozen else "Actif"
        return (
            f"{self.account_id} | Propriétaire : {self.owner} | "
            f"Solde : {self.__balance:.2f} € | {status}"
        )


# ---------------------------------------------------------
# COMPTE COURANT
# ---------------------------------------------------------

class CurrentAccount(Account):
    """
    Compte courant avec frais mensuels.
    """

    def __init__(self, owner_username: str, initial_balance: float = 0.0):
        super().__init__(owner_username, initial_balance)
        self.monthly_fee = 5.0

    def apply_monthly_process(self):
        if not self.is_frozen:
            if self.get_balance() >= self.monthly_fee:
                self.withdraw(self.monthly_fee)


# ---------------------------------------------------------
# COMPTE ÉPARGNE
# ---------------------------------------------------------

class SavingsAccount(Account):
    """
    Compte épargne avec intérêts mensuels.
    """

    def __init__(self, owner_username: str, initial_balance: float = 0.0):
        super().__init__(owner_username, initial_balance)
        self.interest_rate = 0.02  # 2 % mensuel

    def apply_monthly_process(self):
        if not self.is_frozen:
            interest = self.get_balance() * self.interest_rate
            self.deposit(interest)

