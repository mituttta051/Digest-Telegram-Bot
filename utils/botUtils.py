from datetime import datetime

from utils.databaseUtils import getAllMessages


def getPeriodInSeconds(date):
    return (datetime.now() - datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")).total_seconds()


def getMessagesLastWeek(id):
    return list(filter(lambda x: getPeriodInSeconds(x[1]) / 3600 / 24 <= 7, getAllMessages(id)))