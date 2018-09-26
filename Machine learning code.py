import csv
import json
import numpy as nm
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from tkinter import *


def draw():
    temp = "33"
    hum = "50"
    soil = "500"
    light = "1000"

    root = Tk()

    root.title("IOT GUI Test")
    root.geometry("500x200")

    app = Frame(root)
    app.grid()

    label1 = Label(app, text="Temperature: " + temp)
    label1.grid()
    label2 = Label(app, text="Humidity: " + hum + " %")
    label2.grid()
    label3 = Label(app, text="Soil Moisture: " + soil)
    label3.grid()
    label4 = Label(app, text="Light Intensity: " + light)
    label4.grid()

    root.mainloop("34")


def learning():
    balance_data = pd.read_csv("Input.csv", sep=',', header=None)
    train_data = pd.read_csv("sheets1.csv", sep=',', header=None)
    print(balance_data)

    print("Train Dataset Lenght:: ", len(balance_data))
    print("Train Dataset Shape:: ", balance_data.shape)

    print("Dataset Lenght:: ", len(train_data))
    print("Dataset Shape:: ", train_data.shape)
    print("Dataset:: ")
    # print(balance_data.head())
    # print(train_data)


    X = balance_data.values[:, 1:5]
    Y = balance_data.values[:, 0]
    data_to = (train_data.values[-2:-1, 1:5])
    print(data_to)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.7, random_state=100)
    clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100,
                                      max_depth=3, min_samples_leaf=5)
    clf_gini.fit(X_train, y_train)

    DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=3,
                           max_features=None, max_leaf_nodes=None, min_samples_leaf=5,
                           min_samples_split=2, min_weight_fraction_leaf=0.0,
                           presort=False, random_state=100, splitter='best')
    clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=100,
                                         max_depth=3, min_samples_leaf=5)
    clf_entropy.fit(X_train, y_train)
    for val in data_to:
        #   print(val)
        #   print(clf_gini.predict([val]))
        val1 = []
        val1.append(val)
        val2 = nm.append(clf_gini.predict([val]), val1[0])
        # print(val2)
        myList = ','.join(map(str, val2))
        fd = open('Input.csv', 'a')
        fd.write(myList)
        fd.close()
        # draw()

        y_pred = clf_gini.predict(X_test)
        print("Accuracy is ", accuracy_score(y_test, y_pred) * 100)


def sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
    # (json_key['client_email'], json_key['private_key'].encode(), scope) # get email and key from creds

    file = gspread.authorize(credentials)  # authenticate with Google
    sheet = file.open("Iot data").sheet1  # open sheet

    print()
    # print(sheet.get_all_records())

    with open("sheets1.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sheet.get_all_values())

    learning()


if __name__ == "__main__":
    sheets()
