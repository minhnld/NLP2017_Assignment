"""
© 2017 Hoàng Lê Hải Thanh (Thanh Hoang Le Hai) aka GhostBB
If there are any problems, contact me at mail@hoanglehaithanh.com or 1413492@hcmut.edu.vn 
This project is under [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Inherit from NLTK)
"""

raw_database = [    
                    "(BUS B1)",
                    "(ATIME B1 HUE 22:00HR)",
                    "(DTIME B1 HCMC 10:00HR)",
                    "(BUS B2)",
                    "(ATIME B2 HUE 22:30HR)",
                    "(DTIME B2 HCMC 12:30HR)",
                    "(BUS B3)",
                    "(ATIME B3 HCMC 5:00HR)",
                    "(DTIME B3 DANANG 17:30HR)",
                    "(BUS B4)",
                    "(ATIME B4 HCMC 5:30HR)",
                    "(DTIME B4 DANANG 17:30HR)",
                    "(BUS B5)",
                    "(ATIME B5 DANANG 13:30HR)",
                    "(DTIME B5 HUE 08:30HR)",
                    "(BUS B6)",
                    "(ATIME B6 DANANG 9:30HR)",
                    "(DTIME B6 HUE 5:30HR)",
                    "(BUS B7)",
                    "(ATIME B7 HCMC 20:30HR)",
                    "(DTIME B7 HUE 8:30HR)"
                ]

def categorize_database(database):
    """
    Categorize raw database to collections of bus, ATIME and DTIME
    ----------------------------------------------------------------
    Args:
        database: raw database from assignments (List of string values)
    """
    #Remove ( )
    buss = [data.replace('(','').replace(')','') for data in database if 'BUS' in data]
    arrival_times = [data.replace('(','').replace(')','') for data in database if 'ATIME' in data]
    departure_times = [data.replace('(','').replace(')','') for data in database if 'DTIME' in data]
    return {'bus': buss, 
            'arrival':arrival_times, 
            'departure':departure_times}

def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """
    procedure_semantics = semantics
    database = categorize_database(raw_database)
    
    #remove unknown args: ?t ?f ?s
    query =  procedure_semantics['query']
    result_type = 'bus'
    
    for arg in list(procedure_semantics.keys()):
        if '?' in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ''
        elif procedure_semantics[arg] == query and arg != 'query':
            #arrive or depart time
            procedure_semantics[arg] = ''
            result_type = arg
                 
    #Iterate after bus, ATIME and DTIME to have result
    bus_check_result = [f.split()[1] for f in database['bus'] if procedure_semantics['bus'] in f]

    arrival_bus_result = [a.split()[1] for a in database['arrival']
                            if procedure_semantics['arrival_location'] in a
                            and procedure_semantics['arrival_time'] in a
                            and a.split()[1] in bus_check_result]

    departure_bus_result = [d.split()[1] for d in database['departure'] 
                              if procedure_semantics['departure_location'] in d
                              and procedure_semantics['departure_time'] in d
                              and d.split()[1] in arrival_bus_result]

    if result_type == 'bus':
        result = departure_bus_result
    elif result_type == 'arrival_time':
        result = [a.split()[3] for a in database['arrival'] if a.split()[1] in departure_bus_result]
    else:
        result = [d.split()[3] for d in database['departure'] if d.split()[1] in departure_bus_result]
    return result