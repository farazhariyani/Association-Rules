# conda install -c conda-forge mlxtend
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from collections import Counter
import matplotlib.pyplot as plt

#Load dataset
data = []
with open("my_movies.csv") as f:
    data = f.read()

#Exploratory Data Analysis
data = data.split("\n") 

data_list = []
for i in data:
    data_list.append(i.split(","))

data_list = [i for item in data_list for i in item]

item_frequencies = Counter(data_list)
item_frequencies = sorted(item_frequencies.items(), key = lambda x:x[1])
frequencies = list(reversed([i[1] for i in item_frequencies]))
items = list(reversed([i[0] for i in item_frequencies]))

#plotting graph
plt.bar(height = frequencies[0:11], x = list(range(0, 11)), color = 'rgbkymc')
plt.xticks(list(range(0, 11), ), items[0:11])
plt.xlabel("items")
plt.ylabel("Count")
plt.show()

data_series = pd.DataFrame(pd.Series(data_list))
data_series = data_series.iloc[:9835, :] # removing the last empty transaction
data_series.columns = ["transactions"]
X = data_series['transactions'].str.join(sep = '*').str.get_dummies(sep = '*') 

frequent_itemsets = apriori(X, min_support = 0.0075, max_len = 4, use_colnames = True)
frequent_itemsets.sort_values('support', ascending = False, inplace = True)

#plotting graph
plt.bar(x = list(range(0, 11)), height = frequent_itemsets.support[0:11], color ='rgmyk')
plt.xticks(list(range(0, 11)), frequent_itemsets.itemsets[0:11])
plt.xlabel('item-sets')
plt.ylabel('support')
plt.show()

rules = association_rules(frequent_itemsets, metric = "lift", min_threshold = 1)
rules.head(20)
rules.sort_values('lift', ascending = False).head(10)

#Remove redundancy
def to_list(i):
    return (sorted(list(i)))

ma_X = rules.antecedents.apply(to_list) + rules.consequents.apply(to_list) 
ma_X = ma_X.apply(sorted)

#Removing duplicate values
rules_sets = list(ma_X)
unique_rules_sets = [list(m) for m in set(tuple(i) for i in rules_sets)]
index_rules = []

for i in unique_rules_sets:
    index_rules.append(rules_sets.index(i))

rules_no_redudancy = rules.iloc[index_rules, :]
rules_no_redudancy.sort_values('lift', ascending = False).head(10)