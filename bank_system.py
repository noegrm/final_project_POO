# Projet POO : Système bancaire

#Ensemble des imports
from datetime import datetime
import getpass


# Partie 1 : Mise en place des CLASSES UTILISATEURS

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
    Utilisation de l'héritage pour mettre en place un client
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
    Utilisation de l'héritage pour mettre en place un administrateur.
    Hérite de User.
    """

    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.role = "admin"

# classe cmpte bancaire

class Account:
    """
    Classe de base pour un compte bancaire.
    """

    _account_counter = 1  # attribut de classe pour générer les id

    def __init__(self, owner_username: str, initial_balance: float = 0.0):
        self.account_id = f"ACC{Account._account_counter:04d}"
        Account._account_counter += 1

        self.owner = owner_username
        self.__balance = initial_balance  #  attribut privé
        self.is_frozen = False
        self.created_at = datetime.now()


    # Méthodes protégées / publiques


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
        Polymorphisme
        """
        pass

    def __str__(self):
        status = "Gelé" if self.is_frozen else "Actif"
        return (
            f"{self.account_id} | Propriétaire : {self.owner} | "
            f"Solde : {self.__balance:.2f} € | {status}"
        )



# Compte courant

class CurrentAccount(Account):
    """
    Mise en place des frais mensuels.
    """

    def __init__(self, owner_username: str, initial_balance: float = 0.0):
        super().__init__(owner_username, initial_balance)
        self.monthly_fee = 5.0# -5 euros par mois

    def apply_monthly_process(self):
        if not self.is_frozen:
            if self.get_balance() >= self.monthly_fee:
                self.withdraw(self.monthly_fee)


# Compte épargne

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



# Classe transaction

class Transaction:
    """
    Représente une transaction bancaire.
    """

    _transaction_counter = 1  # attribut de classe pour ID unique

    def __init__(
        self,
        transaction_type: str,
        amount: float,
        status: str,
        description: str = "",
        source_account: str = None,
        destination_account: str = None,
    ):
        self.transaction_id = f"TX{Transaction._transaction_counter:05d}"
        Transaction._transaction_counter += 1

        self.timestamp = datetime.now()
        self.transaction_type = transaction_type  # DEPOT, RETRAIT, VIREMENT, SYSTEM
        self.amount = amount
        self.status = status  # SUCCESS / FAILED
        self.description = description
        self.source_account = source_account
        self.destination_account = destination_account

    def __str__(self):
        return (
            f"[{self.transaction_id}] "
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{self.transaction_type} | "
            f"Montant : {self.amount:.2f} € | "
            f"Statut : {self.status} | "
            f"{self.description}"
        )
"""
if __name__ == "__main__":
    t1 = Transaction(
        transaction_type="DEPOT",
        amount=100,
        status="SUCCESS",
        description="Dépôt initial",
        destination_account="ACC0001"
    )

    t2 = Transaction(
        transaction_type="RETRAIT",
        amount=50,
        status="FAILED",
        description="Solde insuffisant",
        source_account="ACC0001"
    )

    print(t1)
    print(t2)

"""

# Mise en place du système centrale

class BankSystem:
    def __init__(self):
        self.users = {}
        self.accounts = {}
        self.transactions = []
        self.current_user = None

        self._init_demo_data()

    # Données de démonstration
    def _init_demo_data(self):
        admin = Admin("admin", "admin123")
        alice = Client("alice", "alice123")

        self.users[admin.username] = admin
        self.users[alice.username] = alice

        acc1 = CurrentAccount("alice", 500)
        acc2 = SavingsAccount("alice", 1000)

        self.accounts[acc1.account_id] = acc1
        self.accounts[acc2.account_id] = acc2

        alice.add_account(acc1)
        alice.add_account(acc2)

    # Authentification
    def login(self):
        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")

        user = self.users.get(username)

        if user and user.check_password(password):
            self.current_user = user
            print(f"\n✅ Connexion réussie ({user.role})\n")
            return True

        print("❌ Identifiants incorrects")
        return False

    def logout(self):
        self.current_user = None
        print("\n🔒 Déconnexion effectuée\n")

    # Menu principal
    def run(self):
        while True:
            print("\n=== SYSTEME BANCAIRE ===")
            print("1. Connexion")
            print("2. Quitter")

            choix = input("Choix : ")

            if choix == "1":
                if self.login():
                    if self.current_user.role == "client":
                        self.menu_client()
                    elif self.current_user.role == "admin":
                        self.menu_admin()
            elif choix == "2":
                print("Au revoir ! 👋")
                break
            else:
                print("Choix invalide")

    # menu client
    def menu_client(self):
        while True:
            print("\n--- MENU CLIENT ---")
            print("1. Lister mes comptes")
            print("2. Dépôt")
            print("3. Retrait")
            print("4. Virement")
            print("5. Historique des transactions")
            print("6. Déconnexion")

            choix = input("Choix : ")

            if choix == "1":
                for acc in self.current_user.list_accounts():
                    print(acc)

            elif choix == "2":
                self._deposit()

            elif choix == "3":
                self._withdraw()

            elif choix == "4":
                self._transfer()

            elif choix == "5":
                self._list_transactions()

            elif choix == "6":
                self.logout()
                break

            else:
                print("Choix invalide")

    #Menu admin
    def menu_admin(self):
        while True:
            print("\n--- MENU ADMIN ---")
            print("1. Créer un client")
            print("2. Créer un compte")
            print("3. Geler / Dégeler un compte")
            print("4. Traitement mensuel")
            print("5. Voir toutes les transactions")
            print("6. Déconnexion")

            choix = input("Choix : ")

            if choix == "1":
                self._create_client()

            elif choix == "2":
                self._create_account()

            elif choix == "3":
                self._toggle_freeze()

            elif choix == "4":
                self._monthly_process()

            elif choix == "5":
                self._list_transactions(all_users=True)

            elif choix == "6":
                self.logout()
                break

            else:
                print("Choix invalide")

    # Operation client
    def _deposit(self):
        acc_id = input("ID du compte : ")
        amount = float(input("Montant : "))

        acc = self.accounts.get(acc_id)

        if acc and acc.deposit(amount):
            self.transactions.append(
                Transaction("DEPOT", amount, "SUCCESS", "Dépôt", None, acc_id)
            )
            print("✅ Dépôt effectué")
        else:
            self.transactions.append(
                Transaction("DEPOT", amount, "FAILED", "Échec dépôt", None, acc_id)
            )

    def _withdraw(self):
        acc_id = input("ID du compte : ")
        amount = float(input("Montant : "))

        acc = self.accounts.get(acc_id)

        if acc and acc.withdraw(amount):
            self.transactions.append(
                Transaction("RETRAIT", amount, "SUCCESS", "Retrait", acc_id, None)
            )
            print("✅ Retrait effectué")
        else:
            self.transactions.append(
                Transaction("RETRAIT", amount, "FAILED", "Échec retrait", acc_id, None)
            )

    def _transfer(self):
        src = input("Compte source : ")
        dst = input("Compte destination : ")
        amount = float(input("Montant : "))

        acc_src = self.accounts.get(src)
        acc_dst = self.accounts.get(dst)

        if acc_src and acc_dst and acc_src.withdraw(amount):
            acc_dst.deposit(amount)
            self.transactions.append(
                Transaction("VIREMENT", amount, "SUCCESS", "Virement", src, dst)
            )
            print("✅ Virement effectué")
        else:
            self.transactions.append(
                Transaction("VIREMENT", amount, "FAILED", "Échec virement", src, dst)
            )

    # Opération admin
    def _create_client(self):
        username = input("Nom utilisateur : ")
        password = getpass.getpass("Mot de passe : ")

        self.users[username] = Client(username, password)
        print("✅ Client créé")

    def _create_account(self):
        username = input("Client : ")
        acc_type = input("Type (courant/epargne) : ")
        balance = float(input("Solde initial : "))

        client = self.users.get(username)

        if not isinstance(client, Client):
            print("❌ Client introuvable")
            return

        if acc_type == "courant":
            acc = CurrentAccount(username, balance)
        else:
            acc = SavingsAccount(username, balance)

        self.accounts[acc.account_id] = acc
        client.add_account(acc)

        print(f"✅ Compte créé : {acc.account_id}")

    def _toggle_freeze(self):
        acc_id = input("ID du compte : ")
        acc = self.accounts.get(acc_id)

        if acc:
            if acc.is_frozen:
                acc.unfreeze()
                print("Compte dégelé")
            else:
                acc.freeze()
                print("Compte gelé")

    def _monthly_process(self):
        for acc in self.accounts.values():
            acc.apply_monthly_process()

        self.transactions.append(
            Transaction("SYSTEM", 0, "SUCCESS", "Traitement mensuel")
        )
        print("✅ Traitement mensuel effectué")

    # transaction
    def _list_transactions(self, all_users=False):
        for t in self.transactions:
            print(t)

if __name__ == "__main__":
    bank = BankSystem()
    bank.run()


