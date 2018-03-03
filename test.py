import math
import scipy
from scipy.stats import gamma
from scipy.stats import poisson

demand = 40
prob = .10
lost_sales_probability = {}

memo_dict = {}

def memo_gamma(key, shape, scale):
        if shape == 0:
                return 0
        else:
                if key in memo_dict:
                        return memo_dict[key]
                else:
                        memo_dict[key] = gamma.cdf(key, shape, 0, scale)
                        return memo_dict[key]


def calculate_demand_probability_table(beta, mieu):
        poisson_st_dev = mieu**(1/2)
        poisson_bound = round(mieu + poisson_st_dev*3) 
        demand_probability_table = []
        
        for i in range(0,poisson_bound):
                poisson_prob = poisson.pmf(i, mieu)
                initial_val = .5
                #print(memo_gamma(initial_val, i, beta))
                while (memo_gamma(initial_val, i, beta) - memo_gamma(initial_val-0.5, i, beta) > 0.01):
                        if len(demand_probability_table) == 0:
                                print("true")
                                demand_probability_table.append([(initial_val-.25)*i])
                                demand_probability_table.append([poisson_prob*memo_gamma(initial_val, i, beta)])
                        else:
                                print("false")
                                demand_probability_table[0].append((initial_val-.25)*i)
                                demand_probability_table[1].append(poisson_prob*memo_gamma(initial_val, i, beta))

                        initial_val+=0.5                                       
        return demand_probability_table


def calculate_inventory_table(demand_table, curr_inventory):
        for i in range(0, len(demand_table[0])-1):
                demand_table[0][i] = curr_inventory - demand_table[0][i]

        return demand_table

demand_table = calculate_demand_probability_table(0.8,3)

print(calculate_inventory_table(demand_table, 14))

##def create_lost_sales_probability_table(demand, prob, inventory_table):

####	for i in range(0,len(inventory_table[0])):
##		lost_sales = max(demand-inventory_table[0][i],0)
##		if lost_sales in lost_sales_probability:
##			lost_sales_probability[lost_sales][1]+=inventory_table[1][i]
##		else:
##			lost_sales_probability[lost_sales] = [prob,inventory_table[1][i]]


##create_lost_sales_probability_table(demand, prob, inventory_table)

##print(lost_sales_probability)
