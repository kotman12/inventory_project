import os
os.chdir('C:\\Users\\Luke\\rzeczy\\Inventory Management')
import produkt as p
import supplier as s

dostawca = s.Supplier("100", 25)
dostawca.lead_time = 12

prod = p.Product("xyz", dostawca)
prod.beta = 1.0
prod.mieu = 2.3
prod.curr_inventory = 8.6
prod.lead_time_inventory_table = prod.build_inventory_table(prod.mieu)
prod.lead_time_plus_one_inventory_table = prod.build_inventory_table(prod.mieu*(prod.supplier.lead_time+1)/prod.supplier.lead_time)
prod.build_lost_sales_probability_table()
prod.average_daily_demand = 0.192
prod.client_credit_days = 40
prod.average_purchase_price = 1700
prod.average_selling_price = 2000

rate = 0.1/365


for i in range(0, 15):
    #prod.curr_inventory = i
    prod.lead_time_inventory_table = prod.build_inventory_table(prod.mieu)
    prod.lead_time_plus_one_inventory_table = prod.build_inventory_table(prod.mieu*(prod.supplier.lead_time+1)/prod.supplier.lead_time)
    cost_of_purchase = prod.calculate_financing_inventory_cost(i, rate)
    lost_sales = prod.calculate_cost_of_lost_sales(i)
    
    #inventory_2 = prod.calculate_financing_inventory_cost1(1, rate)
    #print("cost of purchase divided by profit: " + str(by_profit))
    #print("avg only: " + str(inventory_2))
    #print("diff: " + str(inventory_1-inventory_2))
    
    prod.lead_time_inventory_table = prod.build_inventory_table(prod.mieu*13/12)
    prod.lead_time_plus_one_inventory_table = prod.build_inventory_table(prod.mieu*14/12)
    cost_of_purchase2 = prod.calculate_financing_inventory_cost(i, rate)
    print("cost of purchase (n v n+1): " + str(cost_of_purchase - cost_of_purchase2))
    print("cost of lost sales: " + str(lost_sales))
    print("total: " + str(lost_sales+cost_of_purchase - cost_of_purchase2))
	#print("lost sales :" + str(lost_sales))
	#print("marginal inventory cost :" + str(inventory_1-inventory_2))


prod1 = p.Product("abc", dostawca)
prod1.beta = 0.8
prod1.mieu = 7.3
prod1.curr_inventory = 16
prod1.lead_time_inventory_table = prod1.build_inventory_table(prod1.mieu)
prod1.lead_time_plus_one_inventory_table = prod1.build_inventory_table(prod1.mieu*(prod1.supplier.lead_time+1)/prod1.supplier.lead_time)
prod1.build_lost_sales_probability_table()
prod1.average_daily_demand = 0.45933
prod1.client_credit_days = 20
prod1.average_purchase_price = 1000
prod1.average_selling_price = 3300


rate = 0.1/365
dostawca.constants[0] = -1000
dostawca.constants[15000] = 0
dostawca.prod_collection.append(prod)
dostawca.prod_collection.append(prod1)

dostawca.build_purchase_basket(rate)

for i in range(0, 7):
        print(prod.kod+": "+str(prod.calculate_financing_inventory_cost(i, rate)))
        print(prod.kod+": "+str(prod.calculate_cost_of_lost_sales(i)))

        print(prod1.kod+": "+str(prod1.calculate_financing_inventory_cost(i, rate)))
        print(prod1.kod+": "+str(prod1.calculate_cost_of_lost_sales(i)))

print(dostawca.koszyk_zakupow)
