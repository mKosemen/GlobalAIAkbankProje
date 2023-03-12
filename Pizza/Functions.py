import numpy as np
import pandas as pd
from dbClass import *
from Classes import *
from datetime import date


#Çalışan işlemleri
def AdminControl(userName, password):
    kullanicilar = {}
    parolalar = {}
    adlar = {}
    soyadlar = {}

    im.execute("""Select * From Employees """)
    veriler = im.fetchall()

    for user in veriler:
        kullanicilar[user[0]] = user[1]
    for key in veriler:
        parolalar[key[0]] = key[2]
    for name in veriler:
        adlar[name[0]] = name[3]
    for surname in veriler:
        soyadlar[surname[0]] = surname[4]

    data = dict(Kullanıcı=kullanicilar, Parola=parolalar, Ad=adlar, Soyad=soyadlar)
    admin = pd.DataFrame(data)

    if userName in admin["Kullanıcı"].values:
        psw = (admin[admin["Kullanıcı"] == userName].values[0][1])
        if password == psw:
            employeeFullName = admin[admin["Kullanıcı"] == userName].values[0][2]+" "\
                               +admin[admin["Kullanıcı"] == userName].values[0][3]
            print(f"Hoş geldiniz {employeeFullName}. ")
            return True
        else:
            print("Kullanıcı adı ya da şifreniz hatalı lütfen tekrar deneyiniz.")
            print()
    else:
        print("Kullanıcı adı ya da şifreniz hatalı lütfen tekrar deneyiniz.")
        print()

def TypeControl():
    typeOfPizzas = []
    im.execute("""Select TypeName From TypeOfPizza""")
    veriler = im.fetchall()
    for p in veriler:
        typeOfPizzas.append(p[0])
    return typeOfPizzas

def AddPizza():
    typeOfPizzas = TypeControl()
    while True:
       for type in typeOfPizzas:
            print(type)
            print()
       type = input(
           "Eklemek istediğiniz pizza türü hangisidir ? (Çıkış yapmak için Exit yazınız.)").lower().title()

       while True:
           if type == "Exit":
               break
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
           type = (input(
               "Eklemek istediğiniz pizza türü hangisidir ? (Çıkış yapmak için Exit yazınız.)")).lower().title()


       while True:
           name = (input("Lütfen yeni Pizza adını giriniz: ")).lower().title()
           yol = (input("Yeni pizzamızın adı " + name + " onaylıyor musunuz? (Evet ya da Hayır)")).lower().title()
           if (yol == "Evet"):

               newPizza.description = input("Açıklama: ")
               newPizza.name = name
               newPizza.price = (float)(input("Fiyat: "))


               veriler = (newPizza.name, newPizza.description, newPizza.price, newPizza.type)
               komut = """ INSERT INTO Pizzas(PizzaName, PizzaDescription, Price, PizzaType) VALUES(?, ?, ?, ?)"""

               im.execute(komut, veriler)
               db.commit()
               db.close()
               break

           elif (yol == "Hayır"):
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

def AddSouces():
    while True:
        name = input("Lütfen yeni sos adını giriniz: ").lower().title()
        yol = input("Yeni sosumuzun adı " + name + " onaylıyor musunuz? (Evet ya da Hayır)").lower().title()
        if (yol == "Evet"):
            newSouce = Sauces("", "", "")
            newSouce.description = input("Açıklama: ")
            newSouce.name = name
            newSouce.price = (float)(input("Fiyat: "))

            veriler = (newSouce.name, newSouce.description, newSouce.price)
            komut = """ INSERT INTO Sauces(SaucesName, Description, Price) VALUES(?, ?, ?)"""

            im.execute(komut, veriler)
            db.commit()
            db.close()
            break

        elif (yol == "Hayır"):
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

def GetReport():
    pizza = {}
    size = {}
    sauce = {}
    price ={}

    an = date.today()
    bugun = date.strftime(an, '%x')

    im.execute(""f"Select * From Orders Where OrderDate == '{bugun}' """)
    veriler = im.fetchall()

    for p in veriler:
        pizza[p[0]] = p[2]
    for b in veriler:
        size[b[0]] = b[3]
    for s in veriler:
        sauce[s[0]] = s[4]
    for p in veriler:
        price[p[0]] = p[5]

    totalPrice =sum(price.values())

    data = dict(Pizzalar=pizza, Boyut=size, Soslar=sauce, Fiyat=price)
    gunlukSatis = pd.DataFrame(data)

    print(gunlukSatis)
    print(f"\nGünün Hasılatı: {totalPrice} ₺")

def SalesRates():
    pizza = {}
    im.execute("""Select Pizza, count(Pizza) as [Satış Adedi] From Orders GROUP BY Pizza""")
    pizzaVeriler = im.fetchall()

    for p in pizzaVeriler:
        pizza[p[0]] = p[1]

    data = dict(Satış_Adeti=pizza)
    pizzaSatisOranlari = pd.DataFrame(data)
    print(pizzaSatisOranlari)
    print()

    size = {}
    im.execute("""Select PizzaSize, count(PizzaSize) as [Satış Adedi] From Orders GROUP BY PizzaSize""")
    boyutVeriler = im.fetchall()

    for b in boyutVeriler:
        size[b[0]] = b[1]

    data = dict(Satış_Adeti=size)
    boyutSatisOranlari = pd.DataFrame(data)
    print(boyutSatisOranlari)
    print()

    sauce = {}
    im.execute("""Select Sauces, count(Sauces) as [Satış Adedi] From Orders GROUP BY Sauces""")
    sosVeriler = im.fetchall()

    for s in sosVeriler:
        sauce[s[0]] = s[1]

    data = dict(Satış_Adeti=sauce)
    sosSatisOranlari = pd.DataFrame(data)

    print(sosSatisOranlari)
    print()




#Müşteri işlemleri
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
        print(sauce)
        im.execute(""f"Select Price From Sauces Where SaucesName == '{sauce}'""")
        veriler = im.fetchall()

        sosFiyat = veriler[0][0]

    pizzaFiyat = pizza[0][1]
    oran = size[0][1]

    fiyat = (pizzaFiyat+sosFiyat)*oran

    db.close()
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
    newOrder = Orders("", "", "", "", "", "")
    newOrder.customerName =musteri
    newOrder.pizza = pizza[0][0]
    newOrder.size = boyut[0][0]
    newOrder.sauces = sos
    newOrder.price = fiyat

    an = date.today()
    newOrder.date = date.strftime(an, '%x')

    veriler = (newOrder.customerName, newOrder.pizza, newOrder.size, newOrder.sauces, newOrder.price, newOrder.date)
    komut = """ INSERT INTO Orders(CustomerName, Pizza, PizzaSize, Sauces, Price, OrderDate) VALUES(?, ?, ?, ?, ?, ?)"""

    im.execute(komut, veriler)
    db.commit()
    db.close()

