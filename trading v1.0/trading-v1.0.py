from tradingview_ta import TA_Handler, Interval

sayi = int(input("Kaç Adet Hisse İncelemek İstersiniz? "))

hisseler = []


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
#1
    oran = data4['BUY'] / (data4['BUY'] + data4['SELL'] + data4['NEUTRAL']) * 100
    if oran >= 50:
        print("1. İndikatörlerden gelen AL sinyali oranı"," ","%",oran,"AL")
    else:
        print("1. İndikatörlerden gelen SAT sinyali oranı", " ", "%", 100-oran, "SAT")


#2
    if data1['ADX'] >= 50:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Yüksek")
    elif 20 <= data1['ADX'] < 50:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Normal")
    else:
        print("2. ADX-->",data1['ADX'],"  ","Trend Oluşturma Gücü Düşük")

#3
    print("3. Bu Haftaki Değerler..:","LOW-->",data1['low']," ","HIGH-->",data1['high'])


#4
    if 100 < data1['CCI20']:
        print("4. CCI20 Değeri-->",data1['CCI20[1]'],data1['CCI20'],"  ","Aşırı Alınmış Bölgede!","  ","Gelen Sinyal-->",data3['COMPUTE']['CCI'])
    elif -100 < data1['CCI20'] < 100:
        print("4. CCI20 Değeri-->",data1['CCI20[1]'], data1['CCI20'], "  ", "Alım/Satım Dengeli Bölge.", "  ", "Gelen Sinyal-->",data3['COMPUTE']['CCI'])
    else:
        print("4. CCI20 Değeri-->",data1['CCI20[1]'], data1['CCI20'], "  ", "Aşırı Satılmış Bölgede!", "  ", "Gelen Sinyal-->",data3['COMPUTE']['CCI'])

    if data1['CCI20[1]'] < 0 and data1['CCI20'] > 0:
        print("   Yükseliş Trendi Oluşumu!!!")
    elif data1['CCI20[1]'] > 0 and data1['CCI20'] < 0:
        print("   Düşüş Trendi Oluşumu!!!")
    else:
        print("   Var Olan Trend Devam.")


input("Çıkmak için ENTER'a basın")

