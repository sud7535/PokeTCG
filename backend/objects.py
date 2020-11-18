#!/usr/bin/env python3
import sqlite3
import os.path
import json
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "poke.db")

def oppnent_random(user):
    no = getRandomPoke(user)
    o=[]
    while len(o)<=20:
        random.seed(datetime.now())
        z = random.randrange(1, 252)
        if z not in o and z not in no:
            o.append(z)
    return o


def adminoppnent_random(user):
    no = adminGetRandomPoke(user)
    o=[]
    while len(o)<=20:
        random.seed(datetime.now())
        z = random.randrange(1, 252)
        if z not in o and z not in no:
            o.append(z)
    return o

def getPoke(num):
    with sqlite3.connect('backend/poke.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM pokedex where Rank = ?", (num,))
        obj = list(dict.fromkeys(c.fetchall()))
    return obj[0]


class Pokedex():
    def __init__(self,num):
        obj = getPoke(num)
        self.rank = obj[0]
        self.name = obj[1]
        self.height = obj[2]
        self.weight = obj[3]
        self.hp = obj[4]
        self.attack = obj[5]
        self.defense = obj[6]
        self.sattack = obj[7]
        self.sdefense = obj[8]
        self.speed = obj[9]
        self.url = '/static/img/'+obj[0]+'.png'
    def to_list(self):
        lists =[self.rank,self.name,self.height,self.weight,self.hp,self.attack,self.defense,
                self.sattack,self.sdefense,self.speed,self.url]
        return lists


def getobjects(user):
    pokearray_json= []
    pokearray = []
    arr = getRandomPoke(user)[:20]
    for i in arr:
        tempobj = Pokedex(i[0])
        pokearray.append(tempobj)
        pokearray_json.append(tempobj.to_list())
    return pokearray,pokearray_json


def getobjects_of_opponent(user):
    pokearray_json= []
    pokearray = []
    for i in oppnent_random(user):
        tempobj = Pokedex(i)
        pokearray.append(tempobj)
        pokearray_json.append(tempobj.to_list())
    return pokearray,pokearray_json

def checkAcc(username,password):
    with sqlite3.connect('backend/poke.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT password FROM accounts where name = ? AND pokeId = 0''',[username])
        key = c.fetchall()
        try:
            if (key[0][0] == password):
                print("checkAcc success")
                return True
        except:
            return False

def adminaddCards(username,arr):
    with sqlite3.connect('poke.db') as conn:
        c = conn.cursor()
        for i in arr:
            c.execute('''INSERT INTO accounts(name,password,pokeId) VALUES (?,"Me nahi bataunga",?)''',[username,i])
        conn.commit()

def addCards(username,arr):
    print(username)
    with sqlite3.connect('backend/poke.db') as conn:
        c = conn.cursor()
        for i in arr:
            c.execute('''INSERT INTO accounts(name,password,pokeId) VALUES (?,"Me nahi bataunga",?)''',[username,int(i)])
        conn.commit()

def subCards(username,arr):
    with sqlite3.connect('backend/poke.db') as conn:
        c = conn.cursor()
        for i in arr:
            c.execute('''DELETE FROM accounts WHERE name = ? AND pokeId = ?''',[username,int(i)])
        conn.commit()

def getRandomPoke(user):
    with sqlite3.connect('backend/poke.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT DISTINCT pokeId FROM accounts WHERE name = ? AND pokeId != 0''',[user])
        obj = list(dict.fromkeys(c.fetchall()))
        random.shuffle(obj)

    return (obj)

def adminGetRandomPoke(user):
    with sqlite3.connect('poke.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT pokeId FROM accounts WHERE name = ? AND pokeId != 0''',[user])
        obj = list(dict.fromkeys(c.fetchall()))
        random.shuffle(obj)

    return (obj)
def createAccount():
    x=input("Username:")
    y=input("Password:")
    with sqlite3.connect('poke.db') as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO accounts(name,password,pokeId) VALUES (?,?,0)''',[x,y,])
        print("Account Created")
        conn.commit()
    addCards(x,adminoppnent_random(x))
    print("Added 20 Cards to get you started")



def addToCard():
    print("Select user:")
    x= input()
    adminaddCards(x,adminoppnent_random(x))
    print("Cards Successfully added")

def admin():
    print("1. Create Account:")
    print("2. Add cards")
    i = int(input())
    if (i == 1):
        createAccount()
    elif (i==2):
        addToCard()
    else:
        print("Select valid option. Exiting....")

