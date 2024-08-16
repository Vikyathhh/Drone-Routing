import numpy as np

# Function to read testcase
def read_input_file():
    with open('test.txt', 'r') as file:
        lines = file.readlines()
    
    total_customers, total_cs = map(int, lines[0].strip().split())
    customers = []
    for i in range(1, total_customers + 1):
        cid, payload, deadline = map(float, lines[i].strip().split())
        customers.append({'id': int(cid), 'payload': payload, 'deadline': deadline})
    
    distance_matrix = []
    for line in lines[total_customers + 1:]:
        distance_matrix.append(list(map(float, line.strip().split())))
    
    return total_customers, total_cs, customers, np.array(distance_matrix)

# Function to read drone specs
def read_drone_specs():
    with open('drone_specs.txt', 'r') as file:
        lines = file.readlines()
    
    max_payload = float(lines[0].strip())
    avg_speed = float(lines[1].strip())
    battery_capacity = float(lines[2].strip())
    energy_consumption_rate = float(lines[3].strip())
    discharging_rate = float(lines[4].strip())
    
    return max_payload, avg_speed, battery_capacity, energy_consumption_rate, discharging_rate

def cluster_customers(customers, n_clusters, max_payload):
    customers_sorted = sorted(customers, key=lambda x: (x['deadline'], x['payload']))
    
    clusters = [[] for _ in range(n_clusters)]
    current_payloads = [0] * n_clusters
    
    for customer in customers_sorted:
        for i in range(n_clusters):
            if current_payloads[i] + customer['payload'] <= max_payload:
                clusters[i].append(customer)
                current_payloads[i] += customer['payload']
                break
        else:
            for i in range(n_clusters):
                if len(clusters[i]) == 0:
                    clusters[i].append(customer)
                    current_payloads[i] += customer['payload']
                    break

    # Redistribute customers to balance clusters
    while True:
        max_size = max(len(cluster) for cluster in clusters)
        min_size = min(len(cluster) for cluster in clusters)

        if max_size - min_size <= 1:
            break  # Clusters are balanced enough
        
        # Find indices of the largest and smallest clusters
        largest_cluster_index = next(i for i, cluster in enumerate(clusters) if len(cluster) == max_size)
        smallest_cluster_index = next(i for i, cluster in enumerate(clusters) if len(cluster) == min_size)

        # Try to move a customer from the largest to the smallest
        largest_cluster = clusters[largest_cluster_index]
        smallest_cluster = clusters[smallest_cluster_index]

        for customer in largest_cluster:
            if (current_payloads[smallest_cluster_index] + customer['payload'] <= max_payload):
                largest_cluster.remove(customer)
                smallest_cluster.append(customer)
                current_payloads[smallest_cluster_index] += customer['payload']
                current_payloads[largest_cluster_index] -= customer['payload']
                break

    return clusters

# Main Execution
total_customers, total_cs, customers, distance_matrix = read_input_file()
max_payload, avg_speed, battery_capacity, energy_consumption_rate, discharging_rate = read_drone_specs()

# Number of drones (clusters)
n_clusters = 3  # Example number of drones
clusters = cluster_customers(customers, n_clusters, max_payload)

# Output the clusters
for idx, cluster in enumerate(clusters):
    print(f"Cluster {idx + 1}: {[customer['id'] for customer in cluster]} with total payload {sum(customer['payload'] for customer in cluster)}")
