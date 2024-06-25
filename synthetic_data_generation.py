import random
import numpy as np

def generate_testcase(k):
    total_customers = random.randint(10, 20)
    total_cs = random.randint(3, 5)
    max_distance = 7.19

    cid = []
    payload = []
    deadline =[]
    for i in range(total_customers):
        cid.append(i + 1)
        w = round(random.uniform(1, 30), 2)
        d=random.randint(9, 20)
        payload.append(w)
        deadline.append(d)
    
    cs_within_range = {(i + 1): random.sample(range(1, total_cs + 1), random.randint(1, total_cs)) for i in range(total_customers)}
    #print(cs_within_range)
    n = total_customers + total_cs + 1
    distance_mat = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                distance_mat[i][j] = 0
            else:
                if i == 0:
                    type = 'depot'
                elif i <= total_customers:
                    type = 'customer'
                else:
                    type = 'cs'

                if j == 0:
                    target_type = 'depot'
                elif j <= total_customers:
                    target_type = 'customer'
                else:
                    target_type = 'cs'
                if type == 'depot' and target_type == 'customer':
                    # Distance from depot to customer
                    distance = round(random.uniform(1, max_distance), 2)
                    distance_mat[i][j] = distance
                    distance_mat[j][i] = distance
                
                if type == 'depot' and target_type == 'cs':
                    # Distance from depot to customer
                    distance = round(random.uniform(1, 20), 2)
                    distance_mat[i][j] = distance
                    distance_mat[j][i] = distance
                    
                elif type == 'customer' and target_type == 'customer':
                    distance = round(random.uniform(0.1, 20), 2)
                    distance_mat[i][j] = distance
                    distance_mat[j][i] = distance
                    

                elif type == 'customer' and target_type == 'cs':
                    customer_index = i - 1
                    cs_index = j - total_customers - 1
                    if (customer_index + 1) in cs_within_range and cs_index + 1 in cs_within_range[(customer_index + 1)]:
                        distance = round(random.uniform(1, max_distance), 2)
                    else:
                        distance = round(random.uniform(max_distance + 0.01, 20), 2)
                    distance_mat[i][j] = distance
                    distance_mat[j][i] = distance

                elif type == 'cs' and target_type == 'cs':
                    # Distance between CS (random or fixed as needed)
                    if i != j:
                        distance = round(random.uniform(1, 20), 2)
                        distance_mat[i][j] = distance
                        distance_mat[j][i] = distance

    with open(f"testcase{k}.txt", "w") as file:
        file.write(f"{total_customers} {total_cs}\n")

        for i in range(total_customers):
            file.write(f"{cid[i]} {payload[i]} {deadline[i]}\n")

        for i in range(n):
            for j in range(n):
                file.write(f"{distance_mat[i][j]:.2f}\t")
            file.write("\n")

total_testcases = 100
for k in range(total_testcases):
    generate_testcase(k + 1)
