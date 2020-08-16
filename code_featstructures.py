from __future__ import print_function
from nltk.featstruct import FeatStruct
from nltk.sem.logic import Variable, VariableExpression, Expression
from spacy_parser import spacy_viet
# Natural Language Toolkit: code_featstructures
# fs1 =FeatStruct(arRive=FeatStruct(aVar=Variable('?x')), busNum=FeatStruct(bVar=Variable('?x')))
# print(fs1)

# fs2 = FeatStruct(arRive=FeatStruct(aVar="MINH"), busNum=FeatStruct(bVar='?x'))

# fs2.unify(fs1)

# para = FeatStruct(
#     gap='<f2>',
#     sem='<WHQUERY(ARRIVE1(a3,f2,TIME(t2,20:00HR)),(FLIGHT1(f2) & DEST(f2,NAME(h3,"Hue"))),WH(f2,WHICH1))>',
#     var='<a3>'
#     )
def subtree_matcher(doc,dep,text=''): 
    y = [] 
    # iterate through all the tokens in the input sentence 
    for tok in doc: 
        # extract subject
        if text=='': 
            if tok.dep_.endswith(dep): 
                y.append(tok.text)
        else:
            if tok.dep_.endswith(dep) and tok.text==text:
                y=tok.text
                break
    return y

def checkHead(doc,text):
    y=''
    for tok in doc: 
        # extract subject
        if text==tok.text:
            y=tok.head.text
    return y
def searchChild(doc,tag):
    y=''
    for tok in doc: 
        # extract subject
        if str(tok.dep_)==tag:
            y=tok.children
            return y
    return y

def mainLogic(doc):
    departFlag=False
    departVpFlag=False
    arriveFlag=False
    sourceVpFlag=False
    destVpFlag=False
    busNameNpFlag=False
    destNpFlag=False
    d=''
    t=''
    a=''
    time=''
    nameDepart=''
    nameArrive=''
    bVar=''
    h_BusName=''
    busName=''
    timeDepart=''
    cityTokenText=['Hồ_Chí_Minh','Hà_Nội','Huế','Đà_nẵng','Đà_Nẵng']
    busTokenText=['B1','B2','B3','B4','B5','B6','B7','B8']
    cityTokenDep=['compound','nmod','obl']

    (f,typeWh)=('f2','WHICH1') if (subtree_matcher(doc,'det',text='nào') !=[]) else ('h1','HOWLONG1')
    
    if (typeWh=='WHICH1'):
        gap=f
    else:
        #Runtime (HOWLONG1 case)
        gap='r2'

    if (gap=='f2'):
        if subtree_matcher(doc,'case',text='đến')!=[] or subtree_matcher(doc,'ccomp',text='đến')!=[]:
            arriveFlag=True
            a='a3'
            # time=subtree_matcher(doc,'nummod')[0] if (len(subtree_matcher(doc,'nummod'))==1) else subtree_matcher(doc,'nummod')
            # print([i.text for i in searchChild(doc,'ROOT')])
            try:
                time=[i.text for i in searchChild(doc,'ROOT') if 'HR' in i.text][0]
            except:
                time=''
            if time!='':    
                t='t2'
            else:
                t='?t'
            ################################################
            if subtree_matcher(doc,'ROOT',text='đi')!=[]:
                departFlag=True
                d='d3'
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)
                        tempHead=checkHead(doc,temp)
                        try:
                            tempChild=[i.text for i in searchChild(doc,cD)]
                        except:
                            tempChild=''
                            
                        if (temp !=[]) and (tempHead!='đi'):
                            destVpFlag=True
                            nameArrive= temp
                        elif (temp !=[]) and (tempHead=='đi') and ('từ' in tempChild):
                            sourceVpFlag=True
                            nameDepart= temp
                        elif (temp !=[]) and (tempHead=='đi') and ('đến' in tempChild):
                            destVpFlag=True
                            nameArrive= temp                            
            # elif subtree_matcher(doc,'ROOT',text='xuất_phát')!=[]:
            #     departFlag=True
            #     d='d3'
            #     for cT in cityTokenText:
            #         for cD in cityTokenDep:
            #             temp=subtree_matcher(doc,cD,cT)
            #             tempHead=checkHead(doc,temp)
            #             # try:
            #             #     tempChild=[i.text for i in searchChild(doc,cD)]
            #             # except:
            #             #     tempChild=''
            #             if (temp !=[]) and (tempHead!='xuất_phát'):
            #                 destVpFlag=True
            #                 nameDepart= temp
            #             # elif (temp !=[]) and (tempHead=='xuất_phát') and ('từ' in tempChild):
            #             #     sourceVpFlag=True
            #             #     nameDepart= temp
            #             # elif (temp !=[]) and (tempHead=='xuất_phát') and ('đến' in tempChild):
            #             #     destVpFlag=True
            #             #     nameArrive= temp                   
            else:
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)
                        if temp !=[]:
                            destNpFlag=True
                            nameArrive= temp
                            break
                    else:
                        # Continue if the inner loop wasn't broken.
                        continue
                        # Inner loop was broken, break the outer.
                    break
        elif subtree_matcher(doc,'ROOT',text='xuất_phát')!=[]:
            departFlag=True
            d='d3'
            for cT in cityTokenText:
                for cD in cityTokenDep:
                    temp=subtree_matcher(doc,cD,cT)
                    tempHead=checkHead(doc,temp)
                    # try:
                    #     tempChild=[i.text for i in searchChild(doc,cD)]
                    # except:
                    #     tempChild=''
                    if (temp !=[]) and (tempHead!='xuất_phát'):
                        departVpFlag=True
                        nameDepart= temp
                    # elif (temp !=[]) and (tempHead=='xuất_phát') and ('từ' in tempChild):
                    #     sourceVpFlag=True
                    #     nameDepart= temp
                    # elif (temp !=[]) and (tempHead=='xuất_phát') and ('đến' in tempChild):
                    #     destVpFlag=True
                    #     nameArrive= temp    
        # print(destNpFlag)
        # Variable('?hDest'),name=Variable('?nameDest')
    elif (gap=='r2'):
        if (subtree_matcher(doc,'ROOT',text='đến'))!=[]:
            arriveFlag=True
            a='a3'

            time='?time'
            t='?t'
            
            nameArrive=subtree_matcher(doc,'obj')[0] if (len(subtree_matcher(doc,'obj'))==1) else subtree_matcher(doc,'obj')
            if type(nameArrive)==list:
                for obj in nameArrive:
                    if obj in cityTokenText:
                        nameArrive=obj
                        break
                
            if nameArrive!='':    
                h='h4'
                destVpFlag=True
            else:
                h='?h'

            if subtree_matcher(doc,'case',text='từ')!=[]:
                d='d3'    
                nameDepart=checkHead(doc,'từ')
                if (nameDepart!=''):
                    sourceVpFlag
            listObj=subtree_matcher(doc,'obj')
            listCompound=subtree_matcher(doc,'compound')

            for sub in listObj:
                if sub in busTokenText:
                    busName=sub

            if busName=='':
                for sub in listCompound :
                    if sub in busTokenText:
                        busName=sub

            if busName!='':
                busNameNpFlag=True
                bVar='f2'
                h_BusName='h3'

    if arriveFlag and not(destVpFlag) and not(sourceVpFlag):                
        vp=FeatStruct(
            arrive=FeatStruct(a=a,f=f,t=FeatStruct(t_var=t,time_var=time))
            )
    elif departFlag and departVpFlag:
        vp=FeatStruct(
            depart=FeatStruct(d='d3',f='f1',t=FeatStruct(t_var=t,time_var=time)),
            source=FeatStruct(bus='h3',sourceName=FeatStruct(f=Variable('?h'),name=nameDepart))
        )
    else:
        vp=FeatStruct(
            depart=FeatStruct(d='d3',f='f1',t=FeatStruct(t_var=t,time_var=time)),
            source=FeatStruct(bus='h4',sourceName=FeatStruct(f=Variable('?h'),name=nameDepart)),
            arrive=FeatStruct(a='a3',f='f2',t=FeatStruct(t_var=t,time_var=time)),
            dest=FeatStruct(destName=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h6',name=nameArrive)))
        )

    if destNpFlag and not(busNameNpFlag):
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
    else:
        np=FeatStruct(the=FeatStruct(bus=bVar,busname=FeatStruct(h=h_BusName,name=busName)))
        
    wh=FeatStruct(whType=FeatStruct(f=f,type=typeWh))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    result=featStruct(gap,sem,var,arriveFlag=arriveFlag,destVpFlag=destVpFlag,sourceVpFlag=sourceVpFlag,busNameNpFlag=busNameNpFlag,destNpFlag=destNpFlag,departFlag=departFlag,departVpFlag=departVpFlag)
    print(result)    
    return result     
            
def featStruct(gapUp,semUp,varUp,arriveFlag=False,destVpFlag=False,sourceVpFlag=False,busNameNpFlag=False,destNpFlag=False,departFlag=False,departVpFlag=False):
    gap=Variable('?gap')


    if arriveFlag and not(destVpFlag) and not(sourceVpFlag):                
        vp=FeatStruct(
            arrive=FeatStruct(a=Variable('?a'),f=Variable('?f'),t=FeatStruct(t_var=Variable('?t'),time_var=Variable('?time')))
        )
    elif departFlag and departVpFlag:
        vp=FeatStruct(
            depart=FeatStruct(d=Variable('?d'),f=Variable('?fDep'),t=FeatStruct(t_var=Variable('?t_var_dep'),time_var=Variable('?timeDepart'))),
            source=FeatStruct(bus=Variable('?h'),sourceName=FeatStruct(f=Variable('?h'),name=Variable('?nameSource')))
        )
    else:
        vp=FeatStruct(
            depart=FeatStruct(d=Variable('?d'),f=Variable('?fDep'),t=FeatStruct(t_var=Variable('?t_var_dep'),time_var=Variable('?timeDepart'))),
            source=FeatStruct(bus=Variable('?h'),sourceName=FeatStruct(f=Variable('?h'),name=Variable('?nameSource'))),
            arrive=FeatStruct(a=Variable('?a'),f=Variable('?fArr'),t=FeatStruct(t_var=Variable('?t_var_arr'),time_var=Variable('?timeArrive'))),
            dest=FeatStruct(destName=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?hDest'),name=Variable('?nameDest'))))
        )

    if destNpFlag and not(busNameNpFlag):
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?h'),name=Variable('?name')))))
    else:
        np=FeatStruct(the=FeatStruct(bus=Variable('?b'),busname=FeatStruct(h=Variable('?h_BusName'),name=Variable('?busName'))))

    wh=FeatStruct(whType=FeatStruct(f=Variable('?f'),type=Variable('?type')))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    para = FeatStruct(
        gap=gap,
        sem=sem,
        var=var
    )
    paraUpdate=FeatStruct(
        gap=gapUp,
        sem=semUp,
        var=varUp
    )    
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(paraUpdate)
    # paraUpdate.unify(para)['sem']['query']['vp']['arrive']['f']
    return paraUpdate.unify(para)
