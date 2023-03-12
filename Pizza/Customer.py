
from Functions import *

im.execute("""Select TypeName From TypeOfPizza""")


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
                    choiseSauce = sm[sm["Soslar"] == sauce].values[0][0]
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