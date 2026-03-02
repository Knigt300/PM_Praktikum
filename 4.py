# Auslastung

def gate_usage(log):
    gates = {}
    for case in log:
        for event in log[case]:
            gate = event ['object_gate']
            if gate != "":
                if gate in gates:
                    gates[gate] += 1
                else:
                    gates[gate] = 1
                    
        return gates
    
    
    
# Zahlugsart

def payment_methods(log):
    methods = {}
    for case in log:
        for event in log[case]:
            pay = event['attribute_payment']
            if pay != "":
                if pay in methods:
                    methods[pay] += 1
                else:
                    methods[pay] = 1
    return methods