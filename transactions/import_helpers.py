from transactions.models import Transaction
import csv

def convert_to_float(amount):
    if type(amount) == str:
        return float(amount.replace(",", ""))
    else:
        return float(amount)
    
def _add_row_db(row_dict):
    if row_dict.get("amount"):
        try:
            query = Transaction.objects.filter(
                date=row_dict["date"],
                amount=convert_to_float(row_dict["amount"]),
                description=row_dict["description"],
            ).all()

            if not query:
                Transaction.objects.create(**row_dict)

        except Exception as e:
            print(row_dict, "row")
            print("Error adding transaction", e)
    else:
        print("No Amount Value")


def upload_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            _add_row_db(row)
