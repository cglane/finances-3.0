from transactions.models import Transaction
import csv

def convert_to_float(amount):
    if type(amount) == str:
        return float(amount.replace(",", ""))
    else:
        return float(amount)
    
def _add_row_db(r_d):
    if r_d.get("amount"):
        try:
            query = Transaction.objects.filter(
                date=r_d["date"],
                amount=convert_to_float(r_d["amount"]),
                description=r_d["description"],
            ).all()

            if not query:
                data_obj = {
                "date": r_d.get("date"),
                "amount": r_d.get("amount"),
                "location": r_d.get("location"),
                "description": r_d.get("description"),
                "source": r_d.get("source")
            }
                Transaction.objects.create(**data_obj)

        except Exception as e:
            print(r_d, "row")
            print("Error adding transaction", e)
    else:
        print("No Amount Value")


def upload_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            _add_row_db(row)
