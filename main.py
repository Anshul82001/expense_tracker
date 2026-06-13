from datetime import date
from services.tracker import ExpenseTracker
from exceptions.errors import InvalidAmountError, InvalidCategoryError
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    owner = os.getenv("TRACKER_OWNER","Default")
    data_path = os.getenv("DATA_PATH","data/expense.csv")
    tracker = ExpenseTracker(owner,data_path)

    # add expenses
    tracker.add_expense("Food", 250, "Lunch", date(2026, 6, 1))
    tracker.add_expense("Transport", 80, "Metro", date(2026, 6, 1))

    # analyze
    tracker.show_all()
    tracker.summary_by_category()
    tracker.daily_summary()
    tracker.top_expense(3)

    # save
    tracker.save_to_csv()


if __name__ == "__main__":
    main()