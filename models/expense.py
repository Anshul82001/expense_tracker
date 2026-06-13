from datetime import date
class Expense:
    def __init__(self,expense_id:int, category:str, amount:float, description:str, expense_date:date=None)->None:
        self.expense_id=expense_id
        self.category=category
        self.amount=amount
        self.description=description
        self.expense_date=expense_date or date.today()

    def __repr__(self)->str:
        return f"Expense(expense_id:{self.expense_id}, category:'{self.category}', amount:'{self.amount}', description:'{self.description}', expense_date: '{self.expense_date}')"
