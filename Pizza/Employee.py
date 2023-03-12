
from Functions import *



while True:
    print("MyPizza çalışan paneline hoş geldiniz. Lütfen kullanıcı adı ve parolanızı giriniz.")
    userName = input("Kullanıcı Adı: ")
    password = input("Parola: ")

    while AdminControl(userName, password):
        print(f"""
            |=========İşlemler==========|
            |                           |                 
            |  1 --> Pizza Ekle         |  
            |  2 --> Sos Ekle           |  
            |  3 --> Gün Raporu Al      |
            |  4 --> Satış Oranları     |
            |  5 --> Çıkış              |  
            |                           |                 
            |===========================|
            """)
        prss = input("Lütfen yapmak istediğiniz işlemi seçiniz. ")

        while prss:
            if prss == "1":
                AddPizza()
                break
            elif prss == "2":
                AddSouces()
                break
            elif prss == "3":
                GetReport()
                break
            elif prss == "4":
                SalesRates()
                break
            elif prss == "5":
                break
            else:
                print("Hatalı giriş yapıldı!!! ")
                prss = input("Lütfen yapmak istediğiniz işlemi seçiniz. ")
        break