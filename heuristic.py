import numpy as np

# Load input data
def read_input_data():
    with open('test.txt', 'r') as file:
        lines = file.readlines()
    
    n_customers, n_cs = map(int, lines[0].strip().split())
    customers = []
    for i in range(1, n_customers + 1):
        cid, payload, deadline = map(float, lines[i].strip().split())
        customers.append({'id': int(cid), 'payload': payload, 'deadline': deadline})
    
    dist_matrix = []
    for line in lines[n_customers + 1:]:
        dist_matrix.append(list(map(float, line.strip().split())))
    
    return n_customers, n_cs, customers, np.array(dist_matrix)

# Get drone specifications
def read_drone_specs():
    with open('drone_specs.txt', 'r') as file:
        lines = file.readlines()
    
    max_payload = float(lines[0].strip())
    speed = float(lines[1].strip())
   
    battery_capacity = float(lines[2].strip())
    energy_consumption_rate = float(lines[3].strip())
    
    discharge_rate = float(lines[4].strip())
    
    return max_payload, speed, battery_capacity, energy_consumption_rate, discharge_rate

# Group customers into clusters
def cluster_customers(customers, n_clusters, max_payload):
    sorted_customers = sorted(customers, key=lambda x: (x['payload']))
   
   
    clusters = [[] for _ in range(n_clusters)]
    current_payloads = [0] * n_clusters
    
    for customer in sorted_customers:
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


# Balance cluster sizes
    while True:
        max_size = max(len(cluster) for cluster in clusters)
        min_size = min(len(cluster) for cluster in clusters)
     
        if max_size - min_size <= 1:
            break
        
        largest_index = next(i for i, cluster in enumerate(clusters) if len(cluster) == max_size)
        smallest_index = next(i for i, cluster in enumerate(clusters) if len(cluster) == min_size)
        
        largest_cluster = clusters[largest_index]
        smallest_cluster = clusters[smallest_index]
        
        for cust in largest_cluster:
            if (current_payloads[smallest_index] + cust['payload'] <= max_payload):
                largest_cluster.remove(cust)
                smallest_cluster.append(cust)
                
                current_payloads[smallest_index] += cust['payload']
                current_payloads[largest_index] -= cust['payload']
                break

    drone_assignment = {i: clusters[i] for i in range(n_clusters)}
    return drone_assignment



# Finding nearest charging station
def nearest_cs(curr_location, dist_matrix, charging_stations):
    closest_cs = min(charging_stations, key=lambda cs: dist_matrix[curr_location][cs])
    return closest_cs



# Function to calculate delivery time
def calculate_delivery_time(distance, speed):
    return (distance / speed) * 60 



# Create routes and calculate delivery times
def create_routes(drone_assignments, dist_matrix, battery_capacity, energy_consumption_rate, charging_stations, speed):
    route_plans = {}
    
    for drone_id, customers in drone_assignments.items():
        battery = battery_capacity
        total_time = 0  # Total delivery time
       
        route = []
        last_location = 0  # Start from the depot
        
        for customer in customers:
            cust_id = customer['id']
            dist_to_cust = dist_matrix[last_location][cust_id]
           
            time_to_deliver = calculate_delivery_time(dist_to_cust, speed)
            
            total_time += time_to_deliver
            
            # Record delivery details
            route.append({
                'customer_id': cust_id,
                'payload': customer['payload'],
                'distance_to_customer': dist_to_cust,
                'delivery_time': total_time
            })
            
            last_location = cust_id
        
        # Calculate time to return to depot
        dist_to_depot = dist_matrix[last_location][0]
       
        return_time = calculate_delivery_time(dist_to_depot, speed)
        
        total_time += return_time
        
        route.append({
            'action': 'return_to_depot',
            'distance_to_depot': dist_to_depot,
            'return_time': return_time,
            'total_time': total_time
        })
        
        route_plans[drone_id] = route
    
    return route_plans



# Main Code
n_customers, n_cs, customers, dist_matrix = read_input_data()
max_payload, speed, battery_capacity, energy_consumption_rate, discharge_rate = read_drone_specs()

num_drones = 5

charging_stations = list(range(n_customers + 1, n_customers + 1 + n_cs))
drone_assignments = cluster_customers(customers, num_drones, max_payload)


# Print clusters and payloads
for drone_id, cluster in drone_assignments.items():
    print(f"Drone {drone_id + 1}: {[cust['id'] for cust in cluster]} with total payload {sum(cust['payload'] for cust in cluster)}")
print("\n")


# Generate and print routes
routes = create_routes(drone_assignments, dist_matrix, battery_capacity, energy_consumption_rate, charging_stations, speed)

for drone_id, route in routes.items():
    print(f"Drone {drone_id + 1}:")
  
    last_location = 0
    for step in route:
       
        if 'customer_id' in step:
            delivery_time = step['delivery_time']
            print(f"Delivered to Customer {step['customer_id']} - Payload: {step['payload']} kg, Distance: {step['distance_to_customer']:.2f} km, Delivery Time: {delivery_time:.2f} minutes")
            last_location = step['customer_id']
      
        elif 'charging_station_index' in step:
            charging_station_id = step['charging_station_index']
            print(f"Travel to Charging Station {charging_station_id - n_customers + 1}") 
      
        elif 'action' in step and step['action'] == 'return_to_depot':
            return_time = step['return_time']
            print(f"Return to Depot - Distance: {step['distance_to_depot']:.2f} km, Return Time: {return_time:.2f} minutes, Total Time: {step['total_time']:.2f} minutes")
    print()
