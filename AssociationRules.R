library(readr)
library(arules)

data <- read_csv("my_movies.csv")
View(data)

inspect(data[1:4]) # showing only top 10 transactions
class(data) # book is in transactions format

summary(data)

# making rules using apriori algorithm 
# Keep changing support and confidence values to obtain different rules

# Building rules using apriori algorithm
#1
arules1 <- apriori(data, parameter = list(support = 0.002, confidence = 0.75, minlen = 2))
#2
arules2 <- apriori(data, parameter = list(support = 0.6, confidence = 0.85, minlen = 3))
#3
arules3 <- apriori(data, parameter = list(support = 0.2, confidence = 0.98, minlen = 5))

arules1 #2, 3

# Viewing rules based on lift value
# to view we use inspect .. sort arules by lift ratio
inspect(head(sort(arules1, by = "lift"))) #2, 3

# Overal quality 
head(quality(arules1)) #2, 3

# Different Ways of Visualizing Rules 
# arules2, arules3
plot(arules1)
#reduce overplotting
plot(arules1, jitter = 0)
windows()
plot(arules1, method = "grouped")
# for good visualization try plotting only few rules
plot(arules1[1:10], method = "graph") 

#writing csv file | arules2, arules3
write(arules1, file = "a_rules-data-1.csv", sep = ",")

#get working directory
getwd()