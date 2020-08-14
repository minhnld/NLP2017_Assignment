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
    y = '' 
    # iterate through all the tokens in the input sentence 
    for tok in doc: 
        # extract subject
        if text=='': 
            if tok.dep_.endswith(dep): 
                y = tok.text
        else:
            if tok.dep_.endswith(dep) and tok.text==text:
                y = tok.text 
    return y
def checkHead(doc,text):
    y=''
    for tok in doc: 
        # extract subject
        if text==tok.text:
            y=tok.head.text
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

    (f,typeWh)=('f2','WHICH1') if (subtree_matcher(doc,'det',text='nào') !='') else ('h1','HOWLONG1')
    
    if (typeWh=='WHICH1'):
        gap=f
    else:
        #Runtime (HOWLONG1 case)
        gap='r2'

    if (gap=='f2'):
        if subtree_matcher(doc,'case',text='đến')!='':
            arriveFlag=True
            a='a3'
            time=subtree_matcher(doc,'xcomp')
            if time!='':    
                t='t2'
            else:
                t='?t'
            cityTokenText=['Hồ_Chí_Minh','Hà_Nội','Huế','Đà_nẵng']
            cityTokenDep=['compound','nmod','obl']
            ################################################
            if subtree_matcher(doc,'ROOT',text='xuất_phát')!='' or subtree_matcher(doc,'ROOT',text='đi')!='':
                departFlag=True
                d='d3'
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)
                        if (temp !='') and (checkHead(doc,temp)!='đi'):
                            destVpFlag=True
                            nameArrive= temp
                        elif (temp !='') and (checkHead(doc,temp)=='đi'):
                            sourceVpFlag=True
                            nameDepart= temp
            else:
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)
                        if temp !='':
                            destNpFlag=True
                            nameArrive= temp
                            break
                    else:
                        # Continue if the inner loop wasn't broken.
                        continue
                        # Inner loop was broken, break the outer.
                    break

        elif subtree_matcher(doc,'ROOT',text='xuất_phát')!='' or subtree_matcher(doc,'ROOT',text='đi')!='':
            departFlag=True
            d='d3'
            timeDepart=subtree_matcher(doc,'xcomp')
            if time!='':    
                t='t2'
            else:
                t='?t'
            cityTokenText=['Hồ_Chí_Minh','Hà_Nội','Huế']
            cityTokenDep=['compound','nmod','obl']
            for cT in cityTokenText:
                for cD in cityTokenDep:
                    temp=subtree_matcher(doc,cD,cT)
                    if temp !='':
                        departVpFlag=True
                        nameDepart= temp
                        break
                else:
                    # Continue if the inner loop wasn't broken.
                    continue
                    # Inner loop was broken, break the outer.
                break
            
        # print(destNpFlag)
        # Variable('?hDest'),name=Variable('?nameDest')
    elif (gap=='r2'):
        if (subtree_matcher(doc,'ROOT',text='đến'))!='':
            arriveFlag=True
            a='a3'

            time='time'
            t='t'
            nameArrive=subtree_matcher(doc,'obj')
            if nameArrive!='':    
                h='h4'
                destVpFlag=True
            else:
                h='?h'

            if subtree_matcher(doc,'case',text='từ')!='':
                d='d3'    
                nameDepart=subtree_matcher(doc,'nmod')
                if (nameDepart!=''):
                    sourceVpFlag
            
            busName=subtree_matcher(doc,'compound')
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

    # np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?h'),name=Variable('?name')))))
    if destNpFlag and not(busNameNpFlag):
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
    else:
        np=FeatStruct(the=FeatStruct(bus=bVar,busname=FeatStruct(h=h_BusName,name=busName)))
    # print(np)
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(vp)
    wh=FeatStruct(whType=FeatStruct(f=f,type=typeWh))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    # arriveFlag=False
    # sourceVpFlag=False
    # destVpFlag=False
    # busNameNpFlag=False

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


# ################################
#     if arriveFlag:
#         vp=FeatStruct(arrive=FeatStruct(a=Variable('?a'),f=Variable('?f'),t=FeatStruct(t_var=Variable('?t'),time_var=Variable('?time'))))
#     if destFlag:
#         np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?h'),name=Variable('?name')))))

    wh=FeatStruct(whType=FeatStruct(f=Variable('?f'),type=Variable('?type')))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    para = FeatStruct(
        gap=gap,
        sem=sem,
        var=var
    )
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(para)

    paraUpdate=FeatStruct(
        gap=gapUp,
        sem=semUp,
        var=varUp
    )    
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(paraUpdate)
    # paraUpdate.unify(para)['sem']['query']['vp']['arrive']['f']
    return paraUpdate.unify(para)
