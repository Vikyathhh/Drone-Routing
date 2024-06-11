import random
import numpy as np


def generate_testcase(k):
    total_customers = random.randint(10,20)
    total_drones = random.randint(2,5)
    total_cs = random.randint(3,5)
    
    #print(total_customers,total_drones,total_cs)

    cid=[]
    payload = []
    for i in range(total_customers):
        cid.append(i)
        w=round(random.uniform(1,20),2)
        payload.append(w)

    #for i in range(total_customers):
        #print(cid[i]+1, " ",payload[i])
     
    distance_mat=np.zeros((total_customers,total_customers))

    for i in range(total_customers):
        for j in range(i, total_customers):
            if i == j:
                distance_mat[i][j] = 0
            else:
                distance = round(random.uniform(1, 15), 2)  
                distance_mat[i][j] = distance
                distance_mat[j][i] = distance

    
    with open((f"testcase{k}.txt"), "w") as file:
        file.write(f"{total_customers} {total_drones} {total_cs}\n")
    
        for i in range(total_customers):
            file.write(f"{cid[i] + 1} {payload[i]}\n")
    
        for i in range(total_customers):
            for j in range(total_customers):
                file.write(f"{distance_mat[i][j]:.2f}\t")
            file.write("\n")
       
total_testcases =100
for k in range(total_testcases):
    generate_testcase(k+1)
