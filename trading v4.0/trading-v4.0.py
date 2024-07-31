import colorama
from tradingview_ta import TA_Handler, Interval
from colorama import *
from datetime import *
colorama.init(autoreset=True)

while True:
    rating = 0
    zaman = datetime.now()
    hisseler = []

    def rating_func(x):
        global rating
        rating = rating + x

    def rating_func2(c):
        global count
        count = int(c * 20)
        return count

    def goto():
        return giris_func()
    def giris_func():
        global data1, data2, data3, data4, rating
        giris = input("Haftalık için H, Günlük için G harfini giriniz--> ")
        if giris.upper() == "G":
            sayi = int(input("Kaç Adet Hisse İncelemek İstersiniz? "))
            for a in range(sayi):
                x = input("{}. Hisseyi Giriniz: ".format(a + 1))
                hisseler.append(x)
            for i in hisseler:
                urun = i
                hisse = TA_Handler(
                    symbol=urun,
                    screener="Turkey",
                    exchange="BIST",
                    interval=Interval.INTERVAL_1_DAY
                )

                data1 = hisse.get_analysis().indicators
                data2 = hisse.get_analysis().moving_averages
                data3 = hisse.get_analysis().oscillators
                data4 = hisse.get_analysis().summary
                summary_func()
                adx_func()
                adx_di_func()
                low_high_func()
                cci_func()
                cci_trend_func()
                rsi_func()
                macd_func()
                print(urun.upper(), "Hissesinin Yukarıdaki Göstergelerden Aldığı Puanı-->", rating_func2(rating))
                print(Fore.LIGHTWHITE_EX + Back.BLUE + "MAX PUAN = 72")
                file_func(rating_func2(rating), urun.upper(), result_func(rating_func2(rating)), data1['low'], data1['high'], veri_func_day())
                rating = 0
        elif giris.upper() == "H":
            sayi = int(input("Kaç Adet Hisse İncelemek İstersiniz? "))
            for a in range(sayi):
                x = input("{}. Hisseyi Giriniz: ".format(a + 1))
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
                summary_func()
                adx_func()
                adx_di_func()
                low_high_func()
                cci_func()
                cci_trend_func()
                rsi_func()
                macd_func()
                print(urun.upper(), "Hissesinin Yukarıdaki Göstergelerden Aldığı Puanı-->", rating_func2(rating))
                print(Fore.LIGHTWHITE_EX + Back.BLUE + "MAX PUAN = 72")
                file_func(rating_func2(rating), urun.upper(), result_func(rating_func2(rating)), data1['low'], data1['high'], veri_func_week())
                rating = 0
        else:
            print("Hatalı Harf Girdiniz! Tekrar Giriş Yapınız!!!")
            return goto()

    def veri_func_day():
        global out
        out = str(
            f"{zaman.day}-{zaman.month}-{zaman.year},SAAT-{zaman.hour}.{zaman.minute}.{zaman.second},Interval-{Interval.INTERVAL_1_DAY}")
        return out

    def veri_func_week():
        global out
        out = str(
            f"{zaman.day}-{zaman.month}-{zaman.year},SAAT-{zaman.hour}.{zaman.minute}.{zaman.second},Interval-{Interval.INTERVAL_1_WEEK}")
        return out

    # o: rating puanı/ u: Hisse Adı/ y:rating yorumu/ q:low value/ w:high value/ g:interval/
    def file_func(o, u, y, q, w, g):
        f = open(f"logs/{g}.txt", "a", encoding="utf-8")
        f.write("MAKS PUAN=72\n")
        f.write(f"{u} Hissesi Gösterge Puanları--> " + str(o) + "\n" + f"{y}\n" + f"LOW-->{q} " + f"HIGH-->{w}\n\n")
        f.close()
    def result_func(s):
        if s >= 45:
            sonuc = "Yükseliş trendi başlamış. Kesinlikle Alınmalı."
            print(Fore.BLACK + Back.GREEN + sonuc)
            return sonuc
        elif s >= 28:
            sonuc = "Yükselme Potansiyeli Var. Alınabilir."
            print(Fore.BLACK + Back.LIGHTYELLOW_EX + sonuc)
            return sonuc
        elif s >= 21:
            sonuc = "Henüz Yükseliş Trendine Hazır Değil."
            print(Fore.BLACK + Back.RED + sonuc)
            return sonuc
        else:
            sonuc = "Kötü durumda. Kesinlikle Alınmamalı!"
            print(Fore.BLACK + Back.LIGHTRED_EX + sonuc)
            return sonuc

    def scoring_func():
        sonuc = "45'ın üstü çok iyidir.\n28-45 iyidir.\n21-28 arası nötr.\n21'ün altı kötü.\n"
        return sonuc

    def summary_func():
        # 1 signal summary
        oran = data4['BUY'] / (data4['BUY'] + data4['SELL'] + data4['NEUTRAL']) * 100
        if oran > 50:
            print("\n1. İndikatörlerden gelen AL/SAT sinyali oranı", " ", "%", oran, "AL")
            rating_func(2 / 10)
        elif oran < 50:
            print("\n1. İndikatörlerden gelen AL/SAT sinyali oranı", " ", "%", 100 - oran, "SAT")
        else:
            print("\n1. İndikatörlerden gelen AL/SAT sinyali oranı", " ", "%", oran, "NÖTR")
            rating_func(1 / 10)

    def adx_func():
        # 2 ADX result
        if data1['ADX'] >= 30:
            print("2. ADX-->", data1['ADX'], "  ", "Trend Oluşturma Gücü Yüksek")
            rating_func(2 / 10)
        elif 25 < data1['ADX'] < 30:
            print("2. ADX-->", data1['ADX'], "  ", "Trend Oluşturma Potansiyeli Var")
            rating_func(2 / 10)
        elif 15 <= data1['ADX'] < 25:
            print("2. ADX-->", data1['ADX'], "  ", "Trend Oluşturma Gücü Normal/NÖTR")
            rating_func(1 / 10)
        else:
            print("2. ADX-->", data1['ADX'], "  ", "Trend Oluşturma Gücü Düşük")
    def adx_di_func():
        # 2.1 ADX DI+/DI- signals
        if data1['ADX-DI[1]'] > data1['ADX+DI[1]'] and data1['ADX+DI'] > data1['ADX-DI']:
            print("   Yükseliş Trendi Başlangıcı!!!")
            rating_func(8 / 10)
        elif data1['ADX-DI[1]'] < data1['ADX+DI[1]'] and data1['ADX+DI'] < data1['ADX-DI']:
            print("   Düşüş Trendi Başlangıcı!!!")
        else:
            if data1['ADX+DI[1]'] < data1['ADX+DI']:
                print("   Yükseliş Potansiyeli")
                rating_func(2 / 10)
                if data1['ADX+DI'] >= 45:
                    print("   Aşırı fiyatlanmış! Yükseliş Trendi bitime yakın...")
                    rating_func(1 / 10)
            else:
                if data1['ADX-DI'] > data1['ADX+DI']:
                    print("   Düşüş Trendi Devam!")
                else:
                    print("   Düşüş/Düzeltme Potansiyeli")

    def low_high_func():
        # 3 LOW-HIGH values
        print("3. Bu Haftaki Değerler..:", "LOW-->", data1['low'], " ", "HIGH-->", data1['high'])

    def cci_func():
        # 4 CCI20 result
        if 100 < data1['CCI20']:
            if data1['CCI20[1]'] < 100 and data1['CCI20'] > 100:
                print("4. Aşırı Alınmış Bölgeye Geçmiş!")
                rating_func(1 / 10)
            else:
                print("4. CCI20 Değeri(ESKİ, YENİ)-->", "(", data1['CCI20[1]'], ",", data1['CCI20'], ")", "  ",
                      "Aşırı Alınmış Bölgede!")
                rating_func(0)
        elif -100 < data1['CCI20'] < 100:
            print("4. CCI20 Değeri(ESKİ, YENİ)-->", "(", data1['CCI20[1]'], ",", data1['CCI20'], ")", "  ",
                  "Alım/Satım Dengeli Bölge.")
            rating_func(2 / 10)
        else:
            if data1['CCI20[1]'] > -100 and data1['CCI20'] < -100:
                print("4. Aşırı Satılmış Bölgeye Geçmiş!")
                rating_func(1 / 10)
            else:
                print("4. CCI20 Değeri(ESKİ, YENİ)-->", "(", data1['CCI20[1]'], ",", data1['CCI20'], ")", "  ",
                      "Aşırı Satılmış Bölgede!")
                rating_func(1 / 10)
    def cci_trend_func():
        # 4.1 CCI20 trend signals
        if data1['CCI20[1]'] < 0 and data1['CCI20'] > 0:
            print("   Yükseliş Trendi Oluşumu!!!")
            rating_func(8 / 10)
        elif data1['CCI20[1]'] > 0 and data1['CCI20'] < 0:
            print("   Düşüş Trendi Oluşumu!!!")
            rating_func(0)
        else:
            if data1['CCI20[1]'] > 100 and data1['CCI20'] < 100:
                print("   Aşırı Alınmış Bölgeden çıkmış. Satış başlamış...")
                rating_func(1 / 10)
            if data1['CCI20[1]'] < -100 and data1['CCI20'] > -100:
                print("   Aşırı Satılmış Bölgeden çıkmış. Alış başlamış...")
                rating_func(6 / 10)
            if data1['CCI20'] - data1['CCI20[1]'] < 0:
                print("   Düşüş/Düzeltme Potansiyeli")
                rating_func(1 / 10)
            else:
                if data1['CCI20'] > -100:
                    print("   Yükseliş Potansiyeli Oluşmaya Başlamış...")
                    rating_func(3 / 10)
                else:
                    print("   Yükseliş Potansiyeli Henüz Oluşmamış...")
                    rating_func(2 / 10)
    def rsi_func():
        # 5 RSI
        if data1['RSI'] > 70:
            if data1['RSI[1]'] < 70 and data1['RSI'] > 70:
                print("5. Aşırı Alınmış Bölgeye Girmiş. Tehlikeli Fiyata Ulaşmış!")
                rating_func(1 / 10)
            else:
                print("5. RSI Değeri(ESKİ, YENİ)-->", "(", data1['RSI[1]'], ",", data1['RSI'], ")", "  ",
                      "Aşırı Alınmış Bölgede!")
                rating_func(0)
        elif 30 < data1['RSI'] < 70:
            print("5. RSI Değeri(ESKİ, YENİ)-->", "(", data1['RSI[1]'], ",", data1['RSI'], ")", "  ",
                  "Alım/Satım Dengeli Bölge.")
            if data1['RSI'] > data1['RSI[1]']:
                rating_func(1 / 10)
            else:
                rating_func(3 / 10)
            rating_func(3 / 10)
        else:
            if data1['RSI[1]'] > 30 and data1['RSI'] < 30:
                print("5. Aşırı Satılmış Bölgeye Geçmiş! Dip Noktasına Ulaşılmak Üzere!")
                rating_func(8 / 10)
            else:
                print("5. RSI Değeri(ESKİ, YENİ)-->", "(", data1['RSI[1]'], ",", data1['RSI'], ")", "  ",
                      "Aşırı Satılmış Bölgede!")
                rating_func(9 / 10)
    def macd_func():
        #6 MACD
        macd = data1['MACD.macd']
        macd_signal = data1['MACD.signal']
        if macd <= 0:
            sonuc = "MACD Olumsuz"
            print("6. {} MACD-->{} Signal-->{}".format(sonuc, macd, macd_signal))
            return sonuc
        else:
            rating_func(1 / 10)
            if macd > macd_signal:
                rating_func(4 / 10)
                sonuc = "MACD Olumlu.Alınabilir"
                print("6. {} MACD-->{} Signal-->{}".format(sonuc, macd, macd_signal))
                return sonuc
            else:
                rating_func(2 / 10)
                sonuc = "MACD Nötr.Henüz Hazır sayılmaz"
                print("6. {} MACD-->{} Signal-->{}".format(sonuc, macd, macd_signal))
                return sonuc
####################----------####################
    giris_func()
    p = input("\nÇıkmak için A'ya, yeniden başlatmak için Z'ye basın-->")
    if p.upper() == "A":
        break
    if p.upper() == "Z":
        continue