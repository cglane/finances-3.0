from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import pandas as pd
import numpy as np
from django.contrib.auth.models import User
# from training.lib import preAmex, preCapitolOne, preFinances
from transactions.models import Transaction
from django.conf import settings

class PredictionModel(object):
    def __init__(self, custom_user=None):
        if custom_user and custom_user != settings.DEFAULT_USER:
            user_ids = [settings.DEFAULT_USER, custom_user]
        else:
            user_ids = [settings.DEFAULT_USER]
        self.df = pd.DataFrame(
            list(
                Transaction.objects.filter(user__in=user_ids, location__isnull=False, description__isnull=False).values()
            )
        )

    def train_source(self):
        ##Train Vectorizer

        location_list = self.df['location'].tolist()
        location_list = self.vectorizer.fit_transform(location_list).toarray().tolist()
        ##Add amount to vectors
        amount_list = self.df['amount'].tolist()
        train_list = [list(x) + [amount_list[itr]] for itr, x in enumerate(location_list)]
        ##Initialize Linear SVC
        self.source_clf = svm.LinearSVC(random_state=0)
        self.source_clf.fit(train_list, self.df['source'])
        return self.vectorizer, self.source_clf

    def train_descriptions(self):
        self.vectorizer = CountVectorizer()
        ##Train Vectorizer
        location_list = self.df['location'].tolist()
        location_list = self.vectorizer.fit_transform(location_list).toarray().tolist()
        ##Add amount to vectors
        amount_list  = self.df['amount'].tolist()
        train_list = [list(x) + [amount_list[itr]] for itr, x in enumerate(location_list)]
        ##Initialize Linear SVC
        self.description_clf = svm.LinearSVC(random_state=0)
        self.description_clf.fit(train_list, self.df['description'])
        return self.vectorizer, self.description_clf

    def describe_transactions(self, transactions, user_id):
        """"Expecting transaction to be in format
            {date: '', amount: '', location: '', description: '', source: ''}
        """
        rtrnList = []
        for item in transactions:
            item_found = Transaction.objects.filter(
                date=item['date'],
                location=item['location'],
                amount=item['amount'],
                user_id=user_id
            )
            if not item_found:
                ##Vectorize location
                location_list = self.vectorizer.transform([item['location']]).toarray().tolist()[0]
                ##Add Amount to vector
                location_list.append(float(item['amount']))
                ##Predict based on Vector + amount
                description = self.description_clf.predict([location_list])[0]
                source = self.source_clf.predict([location_list])[0]
                item.update({'description': description})
                item.update({'source': source})
                item.update({'notes': ''})
                rtrnList.append(item)
        if rtrnList:
            keys = list(rtrnList[0].keys())
            rows = [list(x.values()) for x in rtrnList]
            return keys , rows
        raise ValueError('No new transactions')