import datetime
from collections import OrderedDict

class amexCSV(object):
    def __init__(self, csvLines):
        self.csvLines = csvLines
    def getValue(self, rowList):
        value = 0
        if rowList[9]:
            value = rowList[9]
        elif rowList[8]:
            value = rowList[8]
        elif rowList[7]:
            value = rowList[7]
        return float(value) * -1
    def splitRow(self, row):
        rowList = row.split(',')
        if any(rowList):
            ###Remove Day from date string
            date = rowList[0].split('  ')[0]
            d = datetime.datetime.strptime(date, '%m/%d/%Y')
            date = datetime.date.strftime(d, "%Y-%m-%d")
            ##Adding negative sign to value
            amount =  self.getValue(rowList)
            ##Get third item, only text before '-' and not including the "
            location = rowList[2].split(' -')[0][1:]
            if 'ONLINE PAYMENT' not in location:
                return OrderedDict(zip(('date', 'amount', 'location'),(date, amount, location)))

    def readFile(self):
        fileList = []
        if isinstance(self.csvLines, list):
            ##Reverse Order to have oldest transactions first
            for row in self.csvLines:
                formattedRow = self.splitRow(row)
                if formattedRow:
                    fileList.append(formattedRow)
            ###Return the list backwards so it it ends with most recent purchases
            return fileList
        else:            
            return []

class BOACSV(object):
    def __init__(self, csvLines):
        self.csvLines = csvLines
    def splitRow(self, rowList):
        if any(rowList):
            ###Remove Day from date string
            date = rowList[0]
            d = datetime.datetime.strptime(date, '%m/%d/%Y')
            date = datetime.date.strftime(d, "%Y-%m-%d")
            ##Adding negative sign to value
            amount =  rowList[2]
            ##Get first three fields, typically very long
            location = rowList[1]
            ##Don't want to include credit card payment data
            if 'AMERICAN EXPRESS' not in location and 'CAPITAL ONE' not in location:
                return OrderedDict(zip(('date', 'amount', 'location'),(date, amount, location)))

    def readFile(self):
        fileList = []
        if isinstance(self.csvLines, list):
            ##Need to skipp meta data
            for row in reader(self.csvLines[8:]):
                formattedRow = self.splitRow(row)
                if formattedRow:
                    fileList.append(formattedRow)
            ###Return the list backwards so it it ends with most recent purchases
            return fileList
        else:            
            return []



class CapitolOneCSV(object):
    def __init__(self, csvList):
        self.csvList = csvList

    ###Row 7 is for credits but 6 for debits
    def getValue(self,row):
        if row[6]:
            return float(row[6]) * -1
        elif row[7]:
            return float(row[7])

    def readFile(self):
        rtrn_list = []
        if isinstance(self.csvList, list):
                ###Ignore First Column and reverse list
                for row in self.csvList[1:][::-1]:
                    ###Don't want to include credit card payments
                    if "CAPITAL ONE" not in row:
                        rowlist = row.split(',')
                        if any(rowlist):
                            date = rowlist[1]
                            d = datetime.datetime.strptime(date, '%m/%d/%Y')
                            date = datetime.date.strftime(d, "%Y-%m-%d")

                            value = self.getValue(rowlist)
                            location = rowlist[4]
                            rtrn_list.append(
                                OrderedDict(
                                    zip(
                                        ('date', 'amount','location'),
                                        (date,value,location)
                                    )
                                )
                            )
                return rtrn_list
        else:
            return 'CSV list not formatted correctly for CapitolOne Parser'            