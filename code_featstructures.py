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

def mainLogic(doc):
    destFlag=False
    arriveFlag=False
    sourceVpFlag=False
    destVpFlag=False

    (f,typeWh)=('f2','WHICH1') if (subtree_matcher(doc,'det',text='nào') !='') else ('?f','HOWLONG1')
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
        cityTokenText=['Hồ Chí Minh','Hà Nội','Huế']
        cityTokenDep=['compound','nmod','obl']
        for cT in cityTokenText:
            for cD in cityTokenDep:
                temp=subtree_matcher(doc,cD,cT)
                if temp !='':
                    destNpFlag=True
                    nameArrive= temp
                    break 
    elif (gap=='r2'):
        if (subtree_matcher(doc,'ROOT',text='đến'))!='':
            arriveFlag=True
            a='a3'

            time=subtree_matcher(doc,'xcomp')
            if time!='':    
                t='t2'
            else:
                t='?t'
                time='?time'

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


        
        
                    
    if arriveFlag and not(destVpFlag) and not(sourceVpFlag):                
        vp=FeatStruct(arrive=FeatStruct(a=a,f=f,t=FeatStruct(t_var=t,time_var=time)))
    else:
        vp=FeatStruct(
            depart=FeatStruct(d=d,f=f,t=FeatStruct(t_var=t,time_var=time)),
            source=FeatStruct(bus=Variable('?f'),source=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h6',name=nameDepart)))
            arrive=FeatStruct(a=a,f=f,t=FeatStruct(t_var=t,time_var=time))
            dest=FeatStruct(bus=Variable('?f'),source=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h4',name=nameArrive)))
        )

    if destNpFlag:
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
    wh=FeatStruct(whType=FeatStruct(f=Variable('?f'),type=typeWh))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')
    result=featStruct(gap,sem,var,arriveFlag=arriveFlag,destFlag=destFlag)
    print(result)    
    return result     
            
def featStruct(gapUp,semUp,varUp,arriveFlag=False,destFlag=False):
    gap=Variable('?gap')
    if arriveFlag:
        vp=FeatStruct(arrive=FeatStruct(a=Variable('?a'),f=Variable('?f'),t=FeatStruct(t_var=Variable('?t'),time_var=Variable('?time'))))
    if destFlag:
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?h'),name=Variable('?name')))))
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
    # paraUpdate.unify(para)['sem']['query']['vp']['arrive']['f']
    return paraUpdate.unify(para)
