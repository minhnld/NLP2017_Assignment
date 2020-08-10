def parse_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree.label()['SEM']
    f = '?f'
    arrival_location = '?sa'
    arrival_time = '?ta'
    departure_location = '?sd'
    departure_time = '?td'
    runtime='?r'
    busname=''
    #[<ApplicationExpression ARRIVE1(a3,f2,TIME(t2,20:00HR))>, <AndExpression (bus1(f2) & DEST(f2,NAME(h3,'Hue')))>, <ApplicationExpression WH(f2,WHICH1)>]
    verb_expression, bus_expression, wh_expression = logical_expression.args
    gap = '?' + str(logical_tree.label()['GAP'])
    
    #---------Check bus Expression------------#
    np_variables = bus_expression.variables()
    np_preds = [pred.name for pred in bus_expression.predicates()]

     #Get bus variable (f1 or f2 or ...)
    f = '?'+ [variable.name for variable in np_variables if 'f' in variable.name][0]
    #-------------Check Verb expression-------------#
    verb_pred_list = [pred.name for pred in verb_expression.predicates()]

    try:
        if 'DEST' in np_preds:
            #DEST(f (NAME(a,B)))
            if len(list(bus_expression.constants()))==1:
                arrival_location = list(bus_expression.constants())[0].name.replace("'","")
            else:
                arrival_location = list(bus_expression.constants())[1].name.replace("'","")        
        elif  'DEST' in verb_pred_list:
            #DEST(f (NAME(a,B)))
            if len(list(verb_expression.constants()))==1:
                arrival_location = list(verb_expression.constants())[0].name.replace("'","")
            else:
                if 'ARRIVE1' in str(verb_expression.first):
                    arrival_location = verb_expression.second.constants().pop().name.replace("'","")
                else:
                    arrival_location = verb_expression.second.constants().pop().name.replace("'","")

        if 'BUSNAME' in np_preds:
            busname=list(bus_expression.constants())[0].name.replace("'","")
            runtime=gap

        if 'SOURCE' in np_preds:
            #SOURCE(f, NAME(a,B))
            departure_location = list(bus_expression.constants())[0].name.replace("'","")
        elif 'SOURCE' in verb_pred_list:
            #SOURCE(f, NAME(a,B))
            if len(list(verb_expression.constants()))==1:
                departure_location = list(verb_expression.constants())[0].name.replace("'","")
            else:
                if 'DEPART1' in str(verb_expression.first):
                    departure_location = verb_expression.first.constants().pop().name.replace("'","")
                else:
                    departure_location = verb_expression.second.constants().pop().name.replace("'","")

    except:
        if 'DEST' in verb_pred_list:
            #DEST(f (NAME(a,B)))
            arrival_location = list(verb_expression.constants())[0].name.replace("'","")
        else:
            #SOURCE(f, NAME(a,B))
            departure_location = list(verb_expression.constants())[0].name.replace("'","")
            
    #In case of this assignment, this condition will be always TRUE
    #because time must be specified or be asked in all questions
    try:
        if 'TIME' in verb_pred_list:
            time_expression = verb_expression.args[2]
            if len(time_expression.args) == 1:
                #TIME(t)
                time = str(time_expression.args[0])
            else:
                #TIME(t,HOUR) (ex: TIME(t1,1600HR))
                time = str(time_expression.args[1])
                
            #ARRIVE or DEPART?
            
        if 'ARRIVE1' in verb_pred_list:
            #ARRIVE1(v,f,t)
            arrival_time = time if time not in gap else gap
        elif 'DEPART1' in verb_pred_list:
            #DEPART1(v,f,t)
            departure_time = time if time not in gap else gap
        else:
            #RUN-TIME
            pass
    except:
        pass
    
    #--------Fill with parsed values-----------------#
    bus = "(BUS {})".format(f)
    arrival = "(ATIME {} {} {})".format(f, arrival_location, arrival_time)
    departure = "(DTIME {} {} {})".format(f, departure_location, departure_time)
    runtimeprint = "(RUNTIME {} {} {} {})".format(f,busname, departure_location, arrival_location)
    proceduce = "(PRINT-ALL {}{}{}{}{})".format(gap, bus, arrival, departure,runtimeprint)
    
    return {'query': gap,
            'bus': f,
            'arrival_location': arrival_location,
            'arrival_time': arrival_time,
            'departure_location': departure_location,
            'departure_time': departure_time,
            'str': proceduce,
            'busname':busname,
            'runtime':runtime}
    