cpgroups = [
                {
                    "cpgroup_id": 1, 
            
                    "cps": [
                            {
                                "cp_example": 1, 
                                "idade_de_rompimento": 7, 
                                "carga": 23.42,
                            },
                            
                            {
                                "cp_example": 2, 
                                "idade_de_rompimento": 7, 
                                "carga": 23.42,
                            },
                            {
                               "cp_example": 3, 
                                "idade_de_rompimento": 28, 
                                "carga": 25.4,
                            },
                            {
                                "cp_example": 4, 
                                "idade_de_rompimento": 28, 
                                "carga": 24.5,
                            }
                ]
            },
            
                {
                    "cpgroup_id": 2, 
            
                    "cps": [
                            {
                                "cp_example": 1, 
                                "idade_de_rompimento": 7, 
                                "carga": 23.42,
                            },
                            
                            {
                                "cp_example": 2, 
                                "idade_de_rompimento": 7, 
                                "carga": 3.42,
                            },
                            {
                                "cp_example": 3, 
                                "idade_de_rompimento": 28, 
                                "carga": 5.4,
                            },
                            {
                                "cp_example": 4, 
                                "idade_de_rompimento": 30, 
                                "carga": 24.5,
                            }
                ]
            
            }
]

for cpgroup in cpgroups:
    for cp in cpgroup['cps']:
        cp_resistence = cp["carga"] * 10000 / 7854
        if cp["idade_de_rompimento"] == 7:
            if cp_resistence >= .7 * 30:
                print("ok")
            else:
                print("rafa o cp de id: {} está comprometido".format(cp["cp_example"]))

        if cp["idade_de_rompimento"] >= 28:
            if cp_resistence >= 30:
                print("ok")
            else:
                print("rafa o cp de id: {} está comprometido".format(cp["cp_example"]))

