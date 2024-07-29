from tradingview_ta import TA_Handler, Interval


sayi = int(input("Kaç Adet Hisse İncelemek İstersiniz? "))

hisseler = []
rating = 0

def rating_func(x):
    global rating
    rating = rating + x
    #return rating

for a in range(sayi):
    x = input("{}.Hisseyi Giriniz-->".format(a+1))
    hisseler.append(x)

for i in hisseler:
    urun = i
    hisse = TA_Handler(
        symbol=urun,
        screener="Turkey",
        exchange="BIST",
        interval=Interval.INTERVAL_1_WEEK
    )

    data1 = hisse.get_analysis().indicators
    data2 = hisse.get_analysis().moving_averages
    data3 = hisse.get_analysis().oscillators
    data4 = hisse.get_analysis().summary

    print("\n\nİncelenen Hisse-->",urun.upper())
#1 signal summary
    oran = data4['BUY'] / (data4['BUY'] + data4['SELL'] + data4['NEUTRAL']) * 100
    if oran > 50:
        print("1. İndikatörlerden gelen AL/SAT sinyali oranı"," ","%",oran,"AL")
        rating_func(2/10)
    elif oran < 50:
        print("1. İndikatörlerden gelen AL/SAT sinyali oranı", " ", "%", 100-oran, "SAT")
    else:
        print("1. İndikatörlerden gelen AL/SAT sinyali oranı"," ","%",oran,"NÖTR")
        rating_func(1/10)


#2 ADX result
    if data1['ADX'] >= 30:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Yüksek")
        rating_func(2/10)
    elif 25 < data1['ADX'] < 30:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Potansiyeli Var")
        rating_func(2/10)
    elif 15 <= data1['ADX'] < 25:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Normal/NÖTR")
        rating_func(1/10)
    else:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Düşük")
#2.1 ADX DI+/DI- signals
    if data1['ADX-DI[1]'] > data1['ADX+DI[1]'] and data1['ADX+DI'] > data1['ADX-DI']:
        print("   Yükseliş Trendi Başlangıcı!!!")
        rating_func(8/10)
    elif data1['ADX-DI[1]'] < data1['ADX+DI[1]'] and data1['ADX+DI'] < data1['ADX-DI']:
        print("   Düşüş Trendi Başlangıcı!!!")
    else:
        if data1['ADX+DI[1]'] < data1['ADX+DI']:
            print("   Yükseliş Potansiyeli")
            rating_func(2/10)
            if data1['ADX+DI'] >= 45:
                print("   Aşırı fiyatlanmış! Yükseliş Trendi bitime yakın...")
                rating_func(1/10)
        else:
            if data1['ADX-DI'] > data1['ADX+DI']:
                print("   Düşüş Trendi Devam!")
            else:
                print("   Düşüş/Düzeltme Potansiyeli")

#3 LOW-HIGH values
    print("3. Bu Haftaki Değerler..:","LOW-->",data1['low']," ","HIGH-->",data1['high'])

#4 CCI20 result
    if 100 < data1['CCI20']:
        if data1['CCI20[1]'] < 100 and data1['CCI20'] > 100:
            print("4. Aşırı Alınmış Bölgeye Geçmiş!")
            rating_func(1/10)
        else:
            print("4. CCI20 Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")","  ","Aşırı Alınmış Bölgede!")
            rating_func(0)
    elif -100 < data1['CCI20'] < 100:
        print("4. CCI20 Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")", "  ", "Alım/Satım Dengeli Bölge.")
        rating_func(2/10)
    else:
        if data1['CCI20[1]'] > -100 and data1['CCI20'] < -100:
            print("4. Aşırı Satılmış Bölgeye Geçmiş!")
            rating_func(1/10)
        else:
            print("4. CCI20 Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")", "  ", "Aşırı Satılmış Bölgede!")
            rating_func(1/10)


#4.1 CCI20 trend signals
    if data1['CCI20[1]'] < 0 and data1['CCI20'] > 0:
        print("   Yükseliş Trendi Oluşumu!!!")
        rating_func(8/10)
    elif data1['CCI20[1]'] > 0 and data1['CCI20'] < 0:
        print("   Düşüş Trendi Oluşumu!!!")
        rating_func(0)
    else:
        if data1['CCI20[1]'] > 100 and data1['CCI20'] < 100:
            print("   Aşırı Alınmış Bölgeden çıkmış. Satış başlamış...")
            rating_func(1/10)
        if data1['CCI20[1]'] < -100 and data1['CCI20'] > -100:
            print("   Aşırı Satılmış Bölgeden çıkmış. Alış başlamış...")
            rating_func(6/10)
        if data1['CCI20'] - data1['CCI20[1]'] < 0:
            print("   Düşüş/Düzeltme Potansiyeli")
            rating_func(1/10)
        else:
            if data1['CCI20'] > -100:
                print("   Yükseliş Potansiyeli Oluşmaya Başlamış...")
                rating_func(3/10)
            else:
                print("   Yükseliş Potansiyeli Henüz Oluşmamış...")
                rating_func(2/10)

#5 RSI
    if data1['RSI'] > 70:
        if data1['RSI[1]'] < 70 and data1['RSI'] > 70:
            print("5. Aşırı Alınmış Bölgeye Girmiş. Tehlikeli Fiyata Ulaşmış!")
            rating_func(1/10)
        else:
            print("5. RSI Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")", "  ", "Aşırı Alınmış Bölgede!")
            rating_func(0)
    elif 30 < data1['RSI'] < 70:
        print("5. RSI Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")", "  ", "Alım/Satım Dengeli Bölge.")
        if data1['RSI'] > data1['RSI[1]']:
            rating_func(1/10)
        else:
            rating_func(3/10)
        rating_func(3/10)
    else:
        if data1['RSI[1]'] > 30 and data1['RSI'] < 30:
            print("5. Aşırı Satılmış Bölgeye Geçmiş! Dip Noktasına Ulaşılmak Üzere!")
            rating_func(8/10)
        else:
            print("5. RSI Değeri(ESKİ, YENİ)-->","(",data1['RSI[1]'],",",data1['RSI'],")", "  ", "Aşırı Satılmış Bölgede!")
            rating_func(9/10)

    print(urun.upper(),"Hissesinin Yukarıdaki Göstergelerden Aldığı Puanı-->", int(rating*20))
    print("MAX PUAN = 62\n")
    print("40'ın üstü çok iyidir.\n21-40 iyidir.\n16-21 arası nötr.\n16'ün altı kötü.")
    rating = 0
p = input("Çıkmak için ENTER'a basın")
