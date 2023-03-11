import sqlite3 as sql
import numpy as np
import pandas as pd

db = sql.connect('pizza.db')
im = db.cursor()
im.execute("""Select TypeName From TypeOfPizza""")

typeOfPizzas = []
while True:
    try:
        for type in im.fetchone():
            typeOfPizzas.append(type)
    except:
        break

class Pizzas:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class VeganPizzas(Pizzas):
    type = "Vegan"

class MangalPizzas(Pizzas):
    type = "Mangal"

class DenizdenPizzas(Pizzas):
    type = "Denizden"

class Sauces:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class Orders:
    def __init__(self, customerName, pizza, size, sauces, price):
        self.customerName = customerName
        self.pizza = pizza
        self.size = size
        self.sauces = sauces
        self.price = price

def AddPizza():
    cevap = True
    while cevap:
       for type in typeOfPizzas:
            print(type)
            print()
       type = input(
           "Eklemek istediğiniz pizza türü hangisidir ? (Çıkış yapmak için Exit yazınız.)").lower().capitalize()
       if type == "Exit":
           break

       while True:
            if type in typeOfPizzas:
                print(f"Pizza türünüz {type}.")
                if type == 'Vegan':
                    newPizza = VeganPizzas("", "", "")
                    break
                elif type == 'Mangal':
                    newPizza = MangalPizzas("", "", "")
                    break
                else:
                    newPizza = DenizdenPizzas("", "", "")
                    break
            if type not in typeOfPizzas:
                print(f"Elimizde {type} türü bulunmamaktadır.")

       while True:
           name = input("Lütfen yeni Pizza adını giriniz: ")
           yol = input("Yeni pizzamızın adı " + name + " onaylıyor musunuz? (yes or no)").lower()
           if (yol == "yes"):
               newPizza.description = input("Açıklama: ")
               newPizza.name = name
               newPizza.price = (int)(input("Fiyat: "))

               veriler = (newPizza.name, newPizza.description, newPizza.price, newPizza.type)
               komut = """ INSERT INTO Pizzas(PizzaName, PizzaDescription, Price, PizzaType) VALUES(?, ?, ?, ?)"""

               im.execute(komut, veriler)
               db.commit()
               break

           elif (yol == "no"):
               yol2 = 1
               while (yol2 == 1 or yol2 == 2):
                   yol2 = input("Lütfen işleminizi seçiniz ? \n1- Yeni İsim\n2- Çıkış\n")
                   if yol2 == "1":
                       pass
                   elif yol2 == "2":
                       break
                   else:
                       yol2 = 1
                       print("Lütfen ilgili cevabı veriniz.")
               if yol2 == "2":
                   break

           else:
               print("Lütfen ilgili cevabı veriniz.")

def PizzaMenu():
    pizzalar = {}
    turler = {}
    siralar = {}
    im.execute("""Select * From Pizzas""")
    veriler = im.fetchall()
    for pizza in veriler:
        siralar[pizza[0]] = pizza[1]
    for pizza in veriler:
        pizzalar[pizza[0]] = pizza[3]
    for pizza in veriler:
        turler[pizza[0]] = pizza[4]

    data = dict(Pizzalar=siralar, Fiyat=pizzalar, Tür=turler)
    menu = pd.DataFrame(data)
    print(menu)
    return menu

def AddSouces():
       while True:
           name = input("Lütfen yeni sos adını giriniz: ")
           yol = input("Yeni sosumuzun adı " + name + " onaylıyor musunuz? (yes or no)").lower()
           if (yol == "yes"):
               newSouce = Sauces("", "", "")
               newSouce.description = input("Açıklama: ")
               newSouce.name = name
               newSouce.price = (float)(input("Fiyat: "))

               veriler = (newSouce.name, newSouce.description, newSouce.price)
               komut = """ INSERT INTO Sauces(Name, Description, Price) VALUES(?, ?, ?)"""

               im.execute(komut, veriler)
               db.commit()
               break

           elif (yol == "no"):
               yol2 = 1
               while (yol2 == 1 or yol2 == 2):
                   yol2 = input("Lütfen işleminizi seçiniz ? \n1- Yeni İsim\n2- Çıkış\n")
                   if yol2 == "1":
                       pass
                   elif yol2 == "2":
                       break
                   else:
                       yol2 = 1
                       print("Lütfen ilgili cevabı veriniz.")
               if yol2 == "2":
                   break

           else:
               print("Lütfen ilgili cevabı veriniz.")

def SaucesMenu():
    soslar = {}
    siralar = {}
    im.execute("""Select * From Sauces""")
    veriler = im.fetchall()
    for sos in veriler:
        siralar[sos[0]] = sos[1]
    for sos in veriler:
        soslar[sos[0]] = sos[3]

    data = dict(Soslar=siralar, Fiyat=soslar)
    menu = pd.DataFrame(data)
    print(menu)
    return menu

def PizzaPrice(pizza):
    fiyatlar = {}
    im.execute("""Select * From Size """)
    veriler = im.fetchall()

    for fiyat in veriler:
        fiyatlar[fiyat[1]] = fiyat[2]

    data = dict(Fiyat=fiyatlar)
    oran = pd.DataFrame(data).sort_values(by='Fiyat', ascending=True)

    pizzaFiyat = pizza[0][1]

    fiyat = pizzaFiyat*oran
    print(fiyat)
    print()

def TotalPrice(pizza, sauce, size):
    if sauce == "Sos Seçilmedi":
        sosFiyat = 0.00
    else:
        sosFiyat = sauce

    pizzaFiyat = pizza[0][1]
    oran = size[0][1]

    fiyat = (pizzaFiyat+sosFiyat)*oran

    print()
    return fiyat

def SizeControl():
    boyutlar = {}
    oranlar ={}
    im.execute("""Select * From Size """)
    veriler = im.fetchall()

    for boyut in veriler:
        boyutlar[boyut[0]] = boyut[1]
    for boyut in veriler:
        oranlar[boyut[0]] = boyut[2]

    data = dict(Boyut=boyutlar, Oran=oranlar)
    boyut = pd.DataFrame(data)

    return boyut

def OrderControl(musteri, pizza, boyut, sos, fiyat):
    print(f"""
    |=======Sipariş Özeti==============
     Sayın {musteri}                                    
        Pizza:{pizza[0][0]}              
        Boyut: {boyut[0][0]}             
        Ekstra Sos: {sos}          
        Tutar: {fiyat}                   
     Afiyet olsun...                                    
    |==================================|
    """)

def AddOrder(musteri, pizza, boyut, sos, fiyat):
    newOrder = Orders("", "", "", "", "")
    newOrder.customerName =musteri
    newOrder.pizza = pizza[0][0]
    newOrder.size = boyut[0][0]
    newOrder.sauces = sos
    newOrder.price = fiyat

    veriler = (newOrder.customerName, newOrder.pizza, newOrder.size, newOrder.sauces, newOrder.price)
    komut = """ INSERT INTO Orders(CustomerName, Pizza, PizzaSize, Sauces, Price) VALUES(?, ?, ?, ?, ?)"""

    im.execute(komut, veriler)
    db.commit()


print("Merhaba, MyPizza'a hoş geldiniz.")

customerName = ""
choisePizza = ""
choiseSauce = ""
choiseSize = ""
fiyat = ""

while True:
    if customerName == "":
        customerName = (input("Lütfen pizza seçiminizi yapmadan önce isminizi bizimle pylaşınız: ")).lower().title()
        print()

    pm = PizzaMenu()
    sc = SizeControl()

    while True:
        pizza = (input(f"'{customerName}' Hangi Pizzayı sipariş etmek istesiniz? ")).lower().title()

        if pizza in pm["Pizzalar"].values:
            print(f"Sipariş verdiğiniz pizza {pizza}.")
            choisePizza = pm[pm["Pizzalar"] == pizza].values

            PizzaPrice(choisePizza)

            size = (input(f"Lütfen seçmiş olduğunuz '{pizza}' pizzanın boyutunu seçiniz.")).lower().title()

            while True:
                if size in sc["Boyut"].values:
                    print(f"Seçtiğiniz pizza boyutu {size}.")

                    choiseSize = sc[sc["Boyut"] == size].values

                    break
                else:
                    print("Lütfen geçerli bir boyut giriniz.")
                    size = (input(f"Lütfen seçmiş olduğunuz '{pizza}' pizzanın boyutunu seçiniz.")).lower().title()
            break
        else:
            print(f"Üzgünüz istediğiniz {pizza} elimizde bulunmamaktadır.")

    qry = (input("Pizzanıza sos sipariş etmek ister misiniz? (Lütfen 'Evet' yada 'Hayır' olarak cevap veriniz. "))\
        .lower().title()

    while True:
        if qry == 'Evet':
            while True:
                sm = SaucesMenu()
                sauce = (input("Lütfen sosunuzu seçiniz? ")).lower().title()
                if sauce in sm["Soslar"].values:
                    print(f"Seçtiğiniz sos {sauce}.")
                    choiseSauce = sm[sm["Soslar"] == sauce].values[0][1]
                    qry = 'Hayır'

                    fiyat = TotalPrice(choisePizza, choiseSauce, choiseSize)
                    break
                else:
                    print(f"Üzgünüz istediğiniz {sauce} elimizde bulunmamaktadır.")
            if qry == 'Hayır':
                break
        elif qry == 'Hayır':
            choiseSauce = "Sos Seçilmedi"
            fiyat = TotalPrice(choisePizza, choiseSauce, choiseSize)
            break
        else:
            print("Lütfen doğru cevap veriniz.")
            qry = (
                input("Pizzanıza sos sipariş etmek ister misiniz? (Lütfen 'Evet' yada 'Hayır' olarak cevap veriniz. ")) \
                .lower().title()

    OrderControl(customerName, choisePizza, choiseSize, choiseSauce, fiyat)

    qry = (input("Siparişinizi onaylıyor musunuz ? (Evet/Hayır) ")).lower().title()
    while True:
        if qry == "Evet":
            AddOrder(customerName, choisePizza, choiseSize, choiseSauce, fiyat)
            break
        elif qry == "Hayır":
            break
        else:
            print("Lütfen doğru cevap veriniz.")
            qry = (input("Siparişinizi onaylıyor musunuz ? (Evet/Hayır) ")).lower().title()

    qry = (input("Tekrar sipariş vermek ister misiniz ? (Evet/Hayır) ")).lower().title()
    while True:
        if qry == "Evet":
            break
        elif qry == "Hayır":
            break
        else:
            print("Lütfen doğru cevap veriniz.")
            qry = (input("Tekrar sipariş vermek ister misiniz ? (Evet/Hayır) ")).lower().title()

    if qry == "Evet":
        pass
    elif qry == "Hayır":
        print("Tekrar Bekleriz.")
        break