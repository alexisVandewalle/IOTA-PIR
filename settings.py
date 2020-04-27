simulation_type = "split"

parameters_classic = {
    "h":1,
    "rate":3,
    "alpha":0.001,
    "pas":0.5,
    "total time":50,
    "algo":"BRW",
    "nb user":100,
}

parameters_split = {
    "h": 1,
    "rate": 3,
    "alpha": 0.001,
    "pas": 0.5,
    "total time": 50,
    "coef div":0.3,
    "algo":"BRW",
    "nb users":100,
    "partition time":10,
    "join time":30,
}

if simulation_type == "split":
    parameters = parameters_split

elif simulation_type == "classic":
    parameters = parameters_classic