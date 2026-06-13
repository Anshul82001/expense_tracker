import yaml
with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

VALID_CATEGORIES=CONFIG["tracker"]['valid_categories']
MAX_EXPENSE_LIMIT=CONFIG['tracker']['max_expense_limit']

