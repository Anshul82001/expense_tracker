import pandas as pd
import numpy as np
from datetime import date
import os

from models.expense import Expense
from exceptions.errors import InvalidAmountError, InvalidCategoryError, EmptyTrackerError
from utils.logger import logger
from config import MAX_EXPENSE_LIMIT, VALID_CATEGORIES

class ExpenseTracker:
    def __init__(self,owner_name,filepath:str='expense.csv'):
        self.owner=owner_name
        self.expenses=[]
        self._next_id=1
        self.filepath  = filepath
        if os.path.exists(filepath):
            self.load_from_csv(filepath)
            print(f"Auto-loaded existing data for {owner_name}")
        else:
            print(f"New tracker created for {owner_name}")

# add_expense(self, category, amount, description) → None
#   creates an Expense object, appends to self.expenses
#   increments self._next_id
# add_expense should now:
# 1. Check amount > 0 → raise InvalidAmountError if not
# 2. Check category.strip() != "" → raise InvalidCategoryError if not
# 3. Check description.strip() != "" → raise InvalidCategoryError if not
# 4. Log info when expense added successfully
# 5. Caller should handle exceptions with try/except

# Also add logging to:
# - save_to_csv → log info
# - load_from_csv → log info
# - show_all if self.expenses is empty → raise EmptyTrackerError
    def add_expense(self, category: str, amount: float,
                description: str, expense_date: date = None) -> None:
        if amount > MAX_EXPENSE_LIMIT:
            raise InvalidAmountError(f"Amount ₹{amount} exceeds limit of ₹{MAX_EXPENSE_LIMIT}")
        if amount <= 0:
            logger.warning(f"Invalid amount: {amount}")
            raise InvalidAmountError(f"Amount must be positive, got {amount}")

        if category.strip() == "":
            logger.warning("Empty category provided")
            raise InvalidCategoryError("Category cannot be empty")

        if description.strip() == "":
            logger.warning("Empty description provided")
            raise InvalidCategoryError("Description cannot be empty")

        self.expenses.append(
            Expense(self._next_id, category, amount, description, expense_date)
        )
        self._next_id += 1
        logger.info(f"Added expense — {category} | ₹{amount} | {description}")

# show_all(self) → None
#   prints all expenses in table format
    def show_all(self)->None:
        print("ID  | Category   | Amount | Description")
        for expense in self.expenses:
            print(f"{expense.expense_id}   | {expense.category}       | {expense.amount}    | {expense.description}")




# total(self) → float
#   returns sum of all expense amounts

    def total(self)->float:
        total_exp=0
        for expense in self.expenses:
            total_exp+=expense.amount
        return total_exp

# by_category(self) → dict
#   returns {category: total_amount} for all categories
#   Hint: normal dict, loop through self.expenses
    def by_category(self) -> dict:
        result = {}
        for expense in self.expenses:
            result[expense.category] = result.get(expense.category, 0) + expense.amount
        return result

    def to_dataframe(self)->pd.DataFrame:
        return pd.DataFrame([{
            "expense_id": e.expense_id,
            "category":   e.category,
            "amount":     e.amount,
            "description": e.description,
            "date":e.expense_date
        }for e in self.expenses])


    # 1. filter_by_category(self, category: str) → None
#    Print all expenses for a given category
#    Hint: df = self.to_dataframe()
#          then filter df where category matches

    def filter_by_category(self,category:str)->None:
        df=self.to_dataframe()
        print(df[df['category']==category])

# 2. summary_by_category(self) → None
#    Print total and % of total spent per category
#    Example:
#    Category    | Total  | % of Spend
#    Food        | 700    | 35.35%
#    Shopping    | 1200   | 60.61%
#    Transport   | 80     | 4.04%

    def summary_by_category(self)->None:
        df=self.to_dataframe()
        expense_total=self.total()
        res = df.groupby('category').agg(
            Total=('amount','sum')
        )
        res['% of Spend']=((res['Total']*100)/expense_total).round(2)
        print(res)


# 3. daily_summary(self) → None
#    Total spent per day
#    Hint: groupby date → sum amount

    def daily_summary(self)->None:
        df=self.to_dataframe()
        print(df.groupby('date')['amount'].sum())

# 4. top_expense(self, n: int = 3) → None
#    Show top N highest expenses
#    Hint: sort by amount descending, head(n)
    def top_expense(self,n:int=3)->None:
        df=self.to_dataframe()
        print(df.sort_values('amount',ascending=False).head(n))

# 5. monthly_summary(self) -> None
#    Total spent per month
#    Hint: df['month'] = pd.to_datetime(df['date']).dt.month
#          then groupby month → sum
    def monthly_summary(self)->None:
        df=self.to_dataframe()
        df['month']=pd.to_datetime(df['date']).dt.strftime("%B")
        print(df.groupby('month')['amount'].sum())

    # 1. save_to_csv(self, filepath: str = "expenses.csv") → None
#    Convert to dataframe using to_dataframe()
#    Save to CSV with index=False
    def save_to_csv(self, filepath: str = None) -> None:
        path = filepath or self.filepath
        self.to_dataframe().to_csv(path, index=False)
        print(f"Saved {len(self.expenses)} expenses to {path}")
        logger.info("Saved csv")


# 2. load_from_csv(self, filepath: str = "expenses.csv") → None
#    Read CSV into dataframe
#    Loop through rows using df.iterrows()
#    For each row — create an Expense object, append to self.expenses
#    Also update self._next_id = max expense_id + 1
#    Hint: for _, row in df.iterrows():
#              self.expenses.append(Expense(...))
    def load_from_csv(self, filepath:str='expenses.csv')->None:
        df=pd.read_csv(filepath)
        for _, row in df.iterrows():
            expense = Expense(
                expense_id   = row['expense_id'],
                category     = row['category'],
                amount       = row['amount'],
                description  = row['description'],
                expense_date = date.fromisoformat(row['date'])  # "2026-06-01" → date object
            )
            self.expenses.append(expense)
        self._next_id=df['expense_id'].max()+1
        logger.info("Loaded from csv")