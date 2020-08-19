def code_featstructures_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree['sem']['query']
    f = '?f'
    arrival_location = '?sa'
    arrival_time = '?ta'
    departure_location = '?sd'
    departure_time = '?td'
    runtime='?r'
    busname=''
    #[<ApplicationExpression ARRIVE1(a3,f2,TIME(t2,20:00HR))>, <AndExpression (bus1(f2) & DEST(f2,NAME(h3,'Hue')))>, <ApplicationExpression WH(f2,WHICH1)>]
    verb_expression, bus_expression, wh_expression = logical_expression['vp'],logical_expression['np'],logical_expression['wh']
    gap = '?' + logical_tree['gap']
    cityDict={'Huế':'HUE','Đà_Nẵng':'DANANG','Hồ_Chí_Minh':'HCMC','Đà_nẵng':'DANANG'}
    #---------Check bus Expression------------#
    #     if destNpFlag and not(busNameNpFlag):
    #     np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
    # else:
    #     np=FeatStruct(the=FeatStruct(bus=bVar,busname=FeatStruct(h=h_BusName,name=busName)))
    try:
        np_variables = bus_expression['dest']['bus']
    except:
        np_variables = bus_expression['the']['bus']
    
    np_preds = [key for key in bus_expression]

     #Get bus variable (f1 or f2 or ...)
    if 'f' in np_variables:
        f = '?'+ np_variables 
    #-------------Check Verb expression-------------#
    verb_pred_list = [key for key in verb_expression]

    try:
        if 'dest' in np_preds:
            #DEST(f (NAME(a,B)))
            if bus_expression!='':
                try:
                    arrival_location = cityDict[bus_expression['dest']['dest']['name']['name']]
                except:
                    arrival_location = cityDict[bus_expression['the']['busname']['name']]
            else:
                arrival_location = ''
                
        elif  'dest' in verb_pred_list:
            #DEST(f (NAME(a,B)))
            if verb_expression['dest']['destName']['f']!='':
                arrival_location = cityDict[verb_expression['dest']['destName']['name']['name']]
            # else:
            #     if 'ARRIVE1' in str(verb_expression.first):
            #         arrival_location = verb_expression.second.constants().pop().name.replace("'","")
            #     else:
            #         arrival_location = verb_expression.second.constants().pop().name.replace("'","")
        # np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
        try:
            busname=bus_expression['the']['busname']['name']
            if gap=='?r2':
                runtime=gap
        except:
            busname=np_preds['dest']['dest']['name']['name']
            if gap=='?r2':
                runtime=gap
        # if 'SOURCE' in np_preds:
        #     #SOURCE(f, NAME(a,B))
        #     departure_location = list(bus_expression.constants())[0].name.replace("'","")

        if 'source' in verb_pred_list:
            #SOURCE(f, NAME(a,B))
            if verb_expression['source']['bus']!='':
                departure_location = cityDict[verb_expression['source']['sourceName']['name']]
            # else:
            #     if 'DEPART1' in str(verb_expression.first):
            #         departure_location = verb_expression.first.constants().pop().name.replace("'","")
            #     else:
            #         departure_location = verb_expression.second.constants().pop().name.replace("'","")
    except:
        if 'dest' in verb_pred_list:
            #DEST(f (NAME(a,B)))
            arrival_location = cityDict[verb_expression['dest']['destName']['name']['name']]
        else:
            pass
            #SOURCE(f, NAME(a,B))
            # departure_location = cityDict[bus_expression['dest']['dest']['name']['name']]
            
    #In case of this assignment, this condition will be always TRUE
    #because time must be specified or be asked in all questions
    try:
        # if 'TIME' in verb_pred_list:
        #     time_expression = verb_expression.args[2]
        #     if len(time_expression.args) == 1:
        #         #TIME(t)
        #         time = str(time_expression.args[0])
        #     else:
        #         #TIME(t,HOUR) (ex: TIME(t1,1600HR))
        #         time = str(time_expression.args[1])
                
            #ARRIVE or DEPART?
            
        if 'arrive' in verb_pred_list:
            #ARRIVE1(v,f,t)
            time=verb_expression['arrive']['t']['time_var']
            arrival_time = time if time not in gap else gap
        elif 'depart' in verb_pred_list:
            #DEPART1(v,f,t)
            time=verb_expression['depart']['t']['time_var']
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
    