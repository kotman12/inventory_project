
import numpy as np
import pandas as pd
import math
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.cov_struct import (Exchangeable,
    Independence,Autoregressive)
from statsmodels.genmod.families import Poisson
fam = Poisson()
ind = Independence()


df = pd.read_csv("file:///C:/Users/Luke/Documents/drugi_test.csv")


count = 0
for i in range(60, len(df)):
    df_tmp = df.head(i).tail(60)
    model1 = GEE.from_formula("liczba ~ indeks", "indeks", df_tmp, cov_struct=ind, family=fam)
    results = model1.fit()

    if i>117 and i<120:
        print(df_tmp.get_value(60,"indeks"))
    if results.pvalues.Intercept < 0.05 and results.pvalues.indeks < 0.05:
        suma = 0
        for n in range(1, 15):
            suma += math.exp(results.params.Intercept + results.params.indeks*(i+n))
        print(str(i)+": " + str(suma))
    else:
        prediction = df_tmp.mean().liczba*15
        print(str(i)+": " + str(prediction))
