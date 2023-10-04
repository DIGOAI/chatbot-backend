class Receipt(object):
    """Class to represent a receipt emitted by bank transfer.

    Parameters:
    user_name (str): The name of the user
    date (str): The date of the receipt
    amount (str): The amount of the receipt
    office (str): The office of the receipt
    """

    def __init__(self, user_name: str, date: str, amount: str, office: str):
        self.user_name = user_name
        self.date = date
        self.amount = amount
        self.office = office

    def __str__(self):
        return f"Receipt({self.user_name}, {self.date}, {self.amount}, {self.office})"
