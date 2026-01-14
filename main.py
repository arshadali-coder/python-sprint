x = int(input("enter no of expenses:"))
list = []
collection = set()
total = 0
for i in range(1,x+1) :
    s = int(input(f"expense {i} amount(₹) :"))
    t = input(f"expense {i} category((Food, Travel, Shopping, Other) :")
    list.append(s)
    collection.add(t)
    total = total + s 
    
dict = {}
for a in range(x) :
    s = list[a-1]
    dict[t] = s
for u in collection :
    highest = max(u)    

print("Highest expense category is :",highest)
    
if s > 500 :
    high = "High expense detected"
avg = avg / x 
if avg >= 200 :
    status = "Controlled Spending"
elif avg <= 400 :
    status = "Moderate Spending"
else :
    status = "High Spending"
  
