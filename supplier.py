import math
import scipy
from scipy.stats import gamma
from scipy.stats import poisson
import operator

class Supplier:

        def __init__(self, nip, credit_days):
                self.nip = nip
                self.prod_collection = []
                self.credit_days = credit_days
                self.constants = {}
                self.koszyk_zakupow = {}
                
        def add_product(self, prod):
                self.prod_collection[prod.kod] = prod


        def build_purchase_basket(self, rate):
                
                sorted_keys = list(self.constants.keys())
                sorted_keys.sort()
                krancowy_koszt = {}
                minimalny_koszt = 0
                koszyk = {}
                
                for prod in self.prod_collection:
                        tmp = prod.calculate_cost_of_lost_sales(0) + prod.calculate_financing_inventory_cost(0, rate)
                        minimalny_koszt += tmp
                        krancowy_koszt[prod.kod] = {"produkt": prod, "ilosc": 0, "koszt" : tmp}
                        koszyk[prod.kod] = 0
                        self.koszyk_zakupow[prod.kod] = 0

                tmp_koszt = minimalny_koszt
                wartosc_koszyku = 0
                ponizej_ostatniego_progu = wartosc_koszyku < sorted_keys[len(sorted_keys)-1]
                obecny_prog = 0
                
                while ponizej_ostatniego_progu or tmp_koszt <= minimalny_koszt:
                        
                        delta = 10000000
                        for prod in list(krancowy_koszt.keys()):
                                tmp_ilosc = krancowy_koszt[prod]["ilosc"]
                                tmp_produkt = krancowy_koszt[prod]["produkt"]
                                tmp_cost = tmp_produkt.calculate_cost_of_lost_sales(tmp_ilosc) + tmp_produkt.calculate_financing_inventory_cost(tmp_ilosc, rate)
                                tmp_cost1 = tmp_produkt.calculate_cost_of_lost_sales(tmp_ilosc+1) + tmp_produkt.calculate_financing_inventory_cost(tmp_ilosc+1, rate)
                                tmp = tmp_cost1 - tmp_cost
                                if tmp < delta:
                                        min_prod = tmp_produkt
                                        delta = tmp
                                
                        ##sorted(krancowy_koszt, key = lambda x : x[2])
                        ##tmp_koszt += krancowy_koszt[0][2]
                        ##print(delta)
                        ##if tmp_koszt <= minimalny_koszt:
                        krancowy_koszt[min_prod.kod]["ilosc"] += 1
                        koszyk[min_prod.kod] = krancowy_koszt[min_prod.kod]["ilosc"]
                        wartosc_koszyku += min_prod.average_purchase_price
                        ponizej_ostatniego_progu = wartosc_koszyku < sorted_keys[len(sorted_keys)-1]
                        ##print(krancowy_koszt[min_prod.kod]["ilosc"])                        
                        if ponizej_ostatniego_progu:
                                if wartosc_koszyku >= sorted_keys[obecny_prog + 1]:
                                       obecny_prog += 1
                        else:
                                obecny_prog = len(sorted_keys) - 1
                                                                
                        stala = self.constants[sorted_keys[obecny_prog]]
                        tmp_koszt += delta
                        
                        if tmp_koszt - stala <= minimalny_koszt:
                                minimalny_koszt = tmp_koszt - stala
                                for klucz in list(koszyk.keys()):
                                        self.koszyk_zakupow[klucz] = koszyk[klucz]
                                        
                


