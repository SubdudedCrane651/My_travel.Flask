from flask import Flask, request, render_template, Response, redirect
import pandas as pd
import os
import io
import random

global menuchoice
menuchoice = True

global datastr
datastr=""

global spent
spent = []
for n in range(5):
    spent.append(0)

global results
results = []
for n in range(2):
    results.append("")

app = Flask('app')

@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    str= ""
    result = Calculate()
    types = ['airfare', 'tansport', 'hotel', 'food', 'misc']
    str=""
    if request.method == "POST":
        if request.form.get("Submit"):
          try:
              choice = request.form['choice']
              if int(choice)==2:
                str=result[0]
              else:
                return redirect("/add")
          except:
              errors.append(
                  "Unable to get URL. Please make sure it's valid and try again."
              )
              print(errors)
    return render_template('index.html',result=str,title="My travel to Walt Disney World",max=1400,labels=types,values=spent)

@app.route('/add', methods=["GET", "POST"])
def add():
    errors = []
    str=""
    if request.method == "POST":
        if request.form.get("Submit"):
          try:
              choice = request.form['choice']
              amount = request.form['amount']
              date = request.form['date']
              Save(date,Type(int(choice)),amount)
              result = Calculate()
              str=result[1]
          except:
              errors.append(
                  "Unable to get URL. Please make sure it's valid and try again."
              )
              print(errors)
    return render_template('add.html',title="Add to expences",result=str) 

def Save(date, type, amount):
    with open('travel.csv', 'a+') as File:
        File.write("\"" + date + "\"," + "\"" + type + "\"," + amount + "\n")


def Type(type):
    print("""        1-Airfaire
        2-Transport
        3-Hotel
        4-Food
        5-Misc""")
    #type = int(input("Type :"))

    switcher = {
        1: "airfare",
        2: "transport",
        3: "hotel",
        4: "food",
        5: "misc",
    }
    return switcher.get(type)

def Convert(data):
  str="<p>"
  for ch in data:
    str+=ch
    if ch=="\n":
      str+="</p><p>"
  str+="</p>"  
  return str

def Calculate():
    result=""
    data = pd.read_csv("travel.csv")
    #types=["airfare","transport","hotel","food","misc"]
    #data2=pd.DataFrame(data, index=types)
    #newdata=data2.sort_index()
    #print(newdata)
    #sumval = data.sum('index' == 'amount')
    #print(sumval)
    total = 0
    airfare_total = 0
    transport_total = 0
    hotel_total = 0
    food_total = 0
    misc_total = 0
    budget = {
        "total": 2613.86,
        "airfare": 570.20,
        "transport": 80,
        "hotel": 0,
        "food": 1420,
        "misc": 543.66
    }
    datastr=Convert(data.to_string())
    #print(datastr)
  
    for index, row in data.iterrows():
        if row['type'] == 'airfare':
            airfare = row['amount']
            airfare_total = airfare_total + airfare
            spent[0] = airfare_total
        if row['type'] == 'transport':
            transport = row['amount']
            transport_total = transport_total + transport
            spent[1] = transport_total
        if row['type'] == 'hotel':
            hotel = row['amount']
            hotel_total = hotel_total + hotel
            spent[2] = hotel_total
        if row['type'] == 'food':
            food = row['amount']
            food_total = food_total + food
            spent[3] = food_total
        if row['type'] == 'misc':
            misc = row['amount']
            misc_total = misc_total + misc
            spent[4] = misc_total

    for i in range(len(data)):
        amount = data.loc[i, 'amount']
        total = total + amount

    result="<p>You have spent " + "${:,.2f}".format(airfare_total) + " in airfare</p>"
    result+="<p>You have spent " + "${:,.2f}".format(transport_total) + " transport</p>"
    result+="<p>You have spent " + "${:,.2f}".format(hotel_total) + " in hotel</p>"
    result+="<p>You have spent " + "${:,.2f}".format(food_total) + " in food</p>"
    result+="<p>You have spent " + "${:,.2f}".format(misc_total) + " in misc</p>"
    result+="<p>You have spent a total of " + "${:,.2f}".format(total)+"</p>"
    result+="<br>"
    result+="<p>You have " + "${:,.2f}".format(budget["airfare"] - airfare_total) +" left over for airfare</p>"
    result+="<p>You have " +"${:,.2f}".format(budget["transport"] - transport_total) + " left over for transport</p>"
    result+="<p>You have " + "${:,.2f}".format(budget["hotel"] - hotel_total) + " left over for hotel</p>"
    result+="<p>You have " + "${:,.2f}".format(budget["food"] - food_total) + " left over for food</p>"
    result+="<p>You have " + "${:,.2f}".format(budget["misc"] - misc_total) + " left over for misc</p>"
    result+="<p>You have a total " + "${:,.2f}".format(budget["total"] - total) + " left over in the budget</p>"

    results[0]=result
    results[1]=datastr
    
    return results

app.run(host='0.0.0.0')
