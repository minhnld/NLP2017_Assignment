from __future__ import print_function
from nltk.featstruct import FeatStruct
from nltk.sem.logic import Variable, VariableExpression, Expression
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
gap=Variable('?gap')
vp=FeatStruct(arrive=FeatStruct(a=Variable('?a'),f=Variable('?f'),t=Variable('?t')))
np=FeatStruct(dest=FeatStruct(flight=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(f=Variable('?f'),name=Variable('?name')))))
wh=FeatStruct(whType=FeatStruct(f=Variable('?f'),type=Variable('?type')))
sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
var=Variable('?var')

para = FeatStruct(
    gap=gap,
    sem=sem,
    var=var
)
print(para)
vpUp=vp=FeatStruct(arrive=FeatStruct(a=Variable('a3'),f=Variable('f2'),t=Variable('?t')))
paraUpdate=FeatStruct(
    gap='f2',
    sem=FeatStruct(query=FeatStruct(vp=vpUp,np=np,wh=wh))
)    
# paraUpdate.unify(para)['sem']['query']['vp']['arrive']['f']
# print(paraUpdate.unify(para))