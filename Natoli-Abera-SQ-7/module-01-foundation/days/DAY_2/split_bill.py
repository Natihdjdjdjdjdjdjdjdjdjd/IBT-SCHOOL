# let store the total bill and no of people

total_bill = 3000
no_people = 4

# let write the function
def split_bill(total,people,tip_rate=0.10):
    tip=total*tip_rate
    total_with_tip=total+tip
    share_with_freinds=total_with_tip/people
    return share_with_freinds
 

 #now let as store our return value

per_person=split_bill(total_bill,no_people) 

#let create names of the 4 friends
friends= ["Natoli","Abera","Yosef","Hana"]
 #let use loop and try to print there result for each person share
 
for friend in friends:
   print(friend,"should pay",per_person,"ETB")
