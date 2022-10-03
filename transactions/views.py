import json
import traceback
import pygsheets
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.views import APIView

from transactions.machine_learning import PredictionModel
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.lib import (amexCSV, CapitolOneCSV, BOACSV)
from django.conf import settings
from time import sleep
from transactions.import_helpers import convert_to_float
gc = pygsheets.authorize(outh_file="client_secret.json", outh_nonlocal=True)
ALL_PREDICTIONS = {}


def train_predictions(custom_user):
    ALL_PREDICTIONS[custom_user] = PredictionModel(custom_user)
    ALL_PREDICTIONS[custom_user].train_descriptions()
    ALL_PREDICTIONS[custom_user].train_source()
    print("All Training done")


###Train for all users


def train_all_predictions():
    print("Training Predictions")
    users = User.objects.all()
    for custom_user in users:
        train_predictions(custom_user.id)





class MainView(TemplateView):
    template_name = "base.html"


def serialize_dict(obj):
    serializer = TransactionSerializer(data=obj)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@csrf_exempt
def sheets_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    sheets = gc.list_ssheets()
    return JsonResponse(sheets, safe=False)

    # return JsonResponse([], status=400)


class Authorize(APIView):
    """
    List all code snippetss, or create a new snippet.
    """

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)

        name = data["profileObj"]["email"]
        password = name + data["profileObj"]["googleId"]
        email = data["profileObj"]["email"]

        user = User.objects.get(email=email)

        if not user:
            try:
                user = User.objects.create_user(name, email, password)
            except:
                return JsonResponse(status=400)
        ##Train model
        return JsonResponse({"success": True, "userId": user.id}, status=200)


class ReadCSV(APIView):
    """Receive list of csv lines from browser and parse
    based on the credit card company
    """

    def post(self, request):
        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)
        user_id = data.get("userId", settings.DEFAULT_USER)
        print(len(ALL_PREDICTIONS), "all")
        pred = ALL_PREDICTIONS.get(int(user_id), ALL_PREDICTIONS[1])
        if data["type"]:
            if data["type"] == "AMEX":
                fileParser = amexCSV(data["csvList"])
                print('file parse')
                dict_list = fileParser.readFile()
                print(dict_list, 'dict list')
            elif data["type"] == "CapitolOne":
                fileParser = CapitolOneCSV(data["csvList"])
                dict_list = fileParser.readFile()
            elif data["type"] == "BOA":
                fileParser = BOACSV(data["csvList"])
                dict_list = fileParser.readFile()
            try:
                keys, rows = pred.describe_transactions(dict_list, user_id)
                return JsonResponse(
                    {"keys": keys, "rows": rows}, status=200, safe=False
                )
            except ValueError as e:
                import traceback
                traceback.print_exc()
                return JsonResponse({"success": "false", "msg": str(e)}, status=400)
        return JsonResponse({"success": "false", "msg": "wrong type"}, status=400)


class UpdateData(APIView):


    def post(self, request):
        """Receive a rows from data table and add to new google sheet & add to DB"""

        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)
        if isinstance(data["tableRows"], list):
            spread_sheet = gc.create(data["title"])
            wks = spread_sheet[0]
            user_id = settings.DEFAULT_USER
            for row in data["tableRows"]:
                data_dict = dict(zip(data["tableKeys"], row))
                data_dict["amount"] = convert_to_float(data_dict["amount"])
                data_dict.update({"user_id": user_id})
                exists_db = Transaction.objects.filter(
                    date=data_dict.get("date"),
                    amount=data_dict.get("amount"),
                    location=data_dict.get("location"),
                    user_id=user_id,
                )
                if not exists_db:
                    wks.append_table(values=row)
                    transaction = Transaction(**data_dict)
                    transaction.save()
                sleep(1)
            return JsonResponse({"success": "true"}, status=200)
        return JsonResponse({"success": "false"}, status=400)

    def put(self, request):
        """Receive a rows from data table and add to existing google sheet & add to DB"""

        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)
        user_id = settings.DEFAULT_USER
        try:
            if isinstance(data["tableRows"], list):
                spread_sheet = gc.open(data["title"])
                wks = spread_sheet[0]
                for row in data["tableRows"]:
                    data_dict = dict(zip(data["tableKeys"], row))
                    data_dict["amount"] = convert_to_float(data_dict["amount"])
                    data_dict.update({"user_id": user_id})
                    exists_db = Transaction.objects.filter(
                        date=data_dict.get("date"),
                        amount=data_dict.get("amount"),
                        location=data_dict.get("location"),
                        user_id=user_id,
                    )
                    if not exists_db:
                        wks.append_table(values=row)
                        transaction = Transaction(**data_dict)
                        transaction.save()
                    sleep(1)
                return JsonResponse({"success": "true"}, status=200)
        except Exception as e:
            import traceback
            print(e)
            traceback.print_exc
        return JsonResponse({"success": "false"}, status=400)
