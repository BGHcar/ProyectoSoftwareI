class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def remove_account(self, account):
        self.accounts.remove(account)

    def get_accounts(self):
        return self.accounts

    def __repr__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}', accounts={self.accounts})"
