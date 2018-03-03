import math
import scipy
from scipy.stats import gamma
from scipy.stats import poisson
import operator

class Product:

        def __init__(self, kod, supplier):
                self.kod = kod
                self.supplier = supplier
                self.lead_time_inventory_table = {}
                self.lead_time_plus_one_inventory_table = {}
                self.lost_sales_probability = {}
                self.memo_dict = {}
                self.memo_financing_cost = {}
                self.memo_lost_sales = {}
                
        ##product data here:
        ##demand distribution params (beta, mieu) -  don't know which model we are going to use
        ##average_daily_demand (units)
        ##curr_inventory (units)
        ##demand_growth
        ##average_purchase_price (od kazdej rolki/najmniejszej jednostki, jaka mozna kupic od dostawcy)
        ##average_selling_price (od kazdej rolki/najmniejszej jednostki, jaka mozna kupic od dostawcy)
        ##client_credit_days
        ##lead_time_plus_one_inventory_table = {level (units), probability}
        ##lead_time_inventory_table = {level (units), probability}
        ##one_day_demand_table = {demand (units), probability}
        ##minimum_purchase_amount (units)
        ##discrete = TRUE or FALSE
        
        def calculate_financing_inventory_cost(self, purchase_quantity, rate):
                #if(str(purchase_quantity) + "-" + str(rate) in self.memo_financing_cost):
                #        return self.memo_financing_cost[str(purchase_quantity) + "-" + str(rate)]
                #else:
                total_cost = 0
                for inv_level, prob in self.lead_time_plus_one_inventory_table.items():
                
                        estimated_first_cust_payment = inv_level/self.average_daily_demand + self.client_credit_days
                        tmp_cost = 0

                        for i in range(self.supplier.credit_days, int(estimated_first_cust_payment)-1):
                                tmp_cost += (purchase_quantity*self.average_purchase_price*rate / (1+rate)**i)

                        ##print(int(estimated_first_cust_payment))
                        ##print(int(estimated_first_cust_payment + purchase_quantity/self.average_daily_demand))
                        start_point = int(estimated_first_cust_payment)
                        end_point = int(estimated_first_cust_payment + purchase_quantity/self.average_daily_demand)
                        #for i in range(int(estimated_first_cust_payment), int(estimated_first_cust_payment + purchase_quantity/self.average_daily_demand)):
                        for i in range(start_point, end_point):
                                quantity_to_finance = purchase_quantity - self.average_daily_demand*(i-estimated_first_cust_payment+1)
                                tmp_cost += (quantity_to_finance * self.average_purchase_price * rate / (1+rate)**i)
                                
                        total_cost += tmp_cost*prob
                self.memo_financing_cost[str(purchase_quantity) + "-" + str(rate)] = total_cost
                return total_cost

        def calculate_financing_inventory_cost1(self, purchase_quantity, rate):
                inv_level = sum(v*prob for v,prob in self.lead_time_plus_one_inventory_table.items())
                estimated_first_cust_payment = inv_level/self.average_daily_demand + self.client_credit_days
                tmp_cost = 0

                for i in range(self.supplier.credit_days, int(estimated_first_cust_payment)-1):
                        tmp_cost += (purchase_quantity*self.average_purchase_price*rate / (1+rate)**i)
                        
                start_point = int(estimated_first_cust_payment)
                end_point = int(estimated_first_cust_payment + purchase_quantity/self.average_daily_demand)
                for i in range(start_point, end_point):
                        quantity_to_finance = purchase_quantity - self.average_daily_demand*(i-estimated_first_cust_payment+1)
                        tmp_cost += (quantity_to_finance * self.average_purchase_price * rate / (1+rate)**i)
                        
                return tmp_cost

        def calculate_cost_of_lost_sales(self, purchase_quantity):
                if(purchase_quantity in self.memo_lost_sales):
                        return self.memo_lost_sales[purchase_quantity]
                else:
                        total_cost = 0
                        for loss, prob in self.lost_sales_probability.items():
                                new_loss = min(-loss+purchase_quantity, 0)
                                total_cost += (prob*new_loss * (self.average_purchase_price - self.average_selling_price))
                        self.memo_lost_sales[purchase_quantity] = total_cost
                        return total_cost
                
        def build_demand_probability_table(self, mieu):
                poisson_st_dev = mieu**(1/2)
                poisson_bound = round(mieu + poisson_st_dev*5) 
                demand_probability_table = []
                
                for i in range(0,poisson_bound):
                        poisson_prob = poisson.pmf(i, mieu) ##might have to change this to drawing the value from a table we create using PEWMA model
                        gamma_x = .5
                        while (self.memo_gamma(gamma_x, i, self.beta) - self.memo_gamma(gamma_x-0.5, i, self.beta) > 0.001 or gamma_x < i*self.beta):
                                if len(demand_probability_table) == 0:
                                        demand_probability_table.append([gamma_x-.25])
                                        demand_probability_table.append([poisson_prob*(self.memo_gamma(gamma_x, i, self.beta) - self.memo_gamma(gamma_x-0.5, i, self.beta))])
                                        ##variable += poisson_prob*(memo_gamma(gamma_x, i, beta) - memo_gamma(gamma_x-0.5, i, beta))
                                else:
                                        demand_probability_table[0].append(gamma_x-.25)
                                        demand_probability_table[1].append(poisson_prob*(self.memo_gamma(gamma_x, i, self.beta) - self.memo_gamma(gamma_x-0.5, i, self.beta)))
                                        ##variable += poisson_prob*(memo_gamma(gamma_x, i, beta) - memo_gamma(gamma_x-0.5, i, beta))
                                gamma_x+=0.5
                return demand_probability_table

        def build_demand_probability_table(self, mieu):
                poisson_st_dev = mieu**(1/2)
                poisson_bound = round(mieu + poisson_st_dev*6) 
                demand_probability_table = []
                
                for i in range(1,poisson_bound):
                        poisson_prob = poisson.pmf(i, mieu) ##might have to change this to drawing the value from a table we create using PEWMA model
                        ##print(str(i) + "," +str(poisson_prob))

                        gamma_prob = self.memo_gamma(1.5, i, self.beta) - self.memo_gamma(0, i, self.beta)
                        if len(demand_probability_table) < 1:
                                demand_probability_table.append([1.0])
                                demand_probability_table.append([poisson_prob*(gamma_prob)])
                        else:
                                demand_probability_table[0].append(1.0)
                                demand_probability_table[1].append(poisson_prob*(gamma_prob))

                        gamma_x = 2.5
                        gamma_prob = self.memo_gamma(gamma_x, i, self.beta) - self.memo_gamma(gamma_x-1, i, self.beta)
                        while (gamma_prob > 0.001 or gamma_x < i*self.beta):
                                demand_probability_table[0].append(gamma_x-.5)
                                demand_probability_table[1].append(poisson_prob*(gamma_prob))
                                gamma_x+=1
                                gamma_prob = self.memo_gamma(gamma_x, i, self.beta) - self.memo_gamma(gamma_x-1, i, self.beta)
                                
                return demand_probability_table

        def build_inventory_table(self, mieu):
                tmp_dict = {}
                demand_table = self.build_demand_probability_table(mieu)
                total_prob_processed = 0
                for i in range(0, len(demand_table[0])):
                        inv_level = max(self.curr_inventory - demand_table[0][i], 0)
                        if inv_level in tmp_dict:    
                                tmp_dict[inv_level] += demand_table[1][i]
                        else:
                                tmp_dict[inv_level] = demand_table[1][i]
                        total_prob_processed += demand_table[1][i]
                tmp_dict[self.curr_inventory] = 1-total_prob_processed
                return tmp_dict

        def build_lost_sales_probability_table(self):
                dt = self.build_demand_probability_table(self.mieu/self.supplier.lead_time)
                ##print(dt)
                for i in range(0,len(dt[0])):
                        outer_prob = dt[1][i]
                        for level, prob in self.lead_time_inventory_table.items():
                                lost_sales = max(dt[0][i]-level,0)
                                if lost_sales in self.lost_sales_probability:
                                        self.lost_sales_probability[lost_sales]+= (prob*outer_prob)
                                else:
                                        self.lost_sales_probability[lost_sales]= (prob*outer_prob)

        def memo_gamma(self, key, shape, scale):
                if shape == 0:
                        return 0
                else:
                        if str(key) + "-" + str(shape) + "-" + str(scale) in self.memo_dict:
                                return self.memo_dict[str(key) + "-" + str(shape) + "-" + str(scale)]
                        else:
                                self.memo_dict[str(key) + "-" + str(shape) + "-" + str(scale)] = gamma.cdf(key, shape, 0, scale)
                                return self.memo_dict[str(key) + "-" + str(shape) + "-" + str(scale)]
