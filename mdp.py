#Constants
import copy

MAX_TEMP = 25.0
MIN_TEMP = 16.0
OPTIMAL_TEMP = 22.0
ON_COST = 5
OFF_COST = 1.0
HEAT_ON = 1
HEAT_OFF = 0
CONVERGENCE_PARAM = 0.1
actions = {HEAT_OFF, HEAT_ON}

def cost(a):
    if a == HEAT_ON:
        return ON_COST
    else: 
        return OFF_COST

def evaluate_policy(v_values):
    num_states = int((MAX_TEMP - MIN_TEMP)*2+1)
    policy = {}
    for i in range(0, num_states):
        s = index_to_temp(i)
        #print("State: %f" % (s))
        v_prime = {}
        for a in actions:
            v_prime[a] = v_sigma(s, a, v_values)
        policy[s] = "ON" if v_prime[HEAT_ON] < v_prime[HEAT_OFF] else "OFF"
    print("\nOptimal Policy:\n" + str(policy))


def index_to_temp(i):
    return MIN_TEMP + float(i/2.0)

def temp_to_index(s):
    return int((float(s) - MIN_TEMP)*2)

def v_sigma(s, a, v_values):    
    if s == OPTIMAL_TEMP:
        return 0

    if a == HEAT_ON:
        if s == MIN_TEMP:
                return cost(a) + 0.3 * v_values[temp_to_index(s)] + 0.5 * v_values[temp_to_index(s + 0.5)] + 0.2 * v_values[temp_to_index(s + 1.0)]
        elif s == MAX_TEMP: 
            return cost(a) + 0.1 * v_values[temp_to_index(s - 0.5)] + 0.9 * v_values[temp_to_index(s)]
        elif s == MAX_TEMP - 0.5:
            return cost(a) + 0.1 * v_values[temp_to_index(s - 0.5)] + 0.2 * v_values[temp_to_index(s)] + 0.7 * v_values[temp_to_index(s + 0.5) ]
        else:
            return cost(a) + 0.1 * v_values[temp_to_index(s - 0.5)] + 0.2 * v_values[temp_to_index(s)] + 0.5 * v_values[temp_to_index(s + 0.5)] + 0.2 * v_values[temp_to_index(s + 1.0)]
    else: 
        if s == MIN_TEMP:
            return cost(a) + 0.9 * v_values[temp_to_index(s)] + 0.1 * v_values[temp_to_index(s + 0.5)]
        elif s == MAX_TEMP: 
            return cost(a) + 0.7 * v_values[temp_to_index(s - 0.5)] + 0.3 * v_values[temp_to_index(s)]
        else:
            return cost(a) + 0.7 * v_values[temp_to_index(s - 0.5)] + 0.2 * v_values[temp_to_index(s)] + 0.1 * v_values[temp_to_index(s + 0.5)]


def value_iteration():
    num_states = int((MAX_TEMP - MIN_TEMP)*2+1)
    #print("num_states:" + str(num_states))
    v_values = [0] * num_states

    print(v_values)
    while True:
        deltas = []
        v_curr = copy.deepcopy(v_values)

        for i in range(0, num_states):
            v_prime = {}
            s = index_to_temp(i)
            #print("Index: %d  State: %f" % (i, s))
            

            for a in actions:
                v_prime[a] = v_sigma(s, a, v_curr)
                #print("For action A v(s) is " + str(v_prime[a]))
            v_next = min(v_prime.values())
            #print("v_next is " + str(v_next))

            v_values[i] = min(v_prime.values())
            deltas.append(abs(v_next-v_curr[i]))
        print("Updated v_values:\n" + str(v_values))
        print("Change in each state for this iteration:\n" + str(deltas))
        if max(deltas)<CONVERGENCE_PARAM:
            print(v_values)
            break  
    evaluate_policy(v_values)

            
value_iteration()
