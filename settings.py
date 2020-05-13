simulation_type = "split"

parameters_classic = {
    "h":1,
    "rate":3,
    "alpha":0.001,
    "pas":0.5,
    "total time":50,
    "algo":"BRW",
    "nb user":100,
    "init wallet":50,
    "mean cost":10
}

parameters_split = {
    "h": 1,
    "rate": 3,
    "alpha": 0.001,
    "pas": 1,
    "total time": 20,
    "coef div":0.3,
    "algo":"BRW",
    "nb users":10,
    "partition time":10,
    "join time":30,
    "init wallet":50,
    "mean cost":10
}

if simulation_type == "split":
    parameters = parameters_split

elif simulation_type == "classic":
    parameters = parameters_classic