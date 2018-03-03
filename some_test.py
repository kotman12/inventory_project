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