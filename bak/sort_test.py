#coding:utf8
'''
--: {'new': [1065, 65, 90, 81], 'old': [1065, 65, 90, 81], 'name': '3FC4D95910C049F6B31E095012ED1DCB'}
--: {'new': [897, 65, 88, 82], 'old': [897, 65, 88, 82], 'name': 'CADE209D85244BDE82CFAF33A11A9758'}
--: {'new': [456, 53, 155, 46], 'old': [456, 53, 155, 46], 'name': 'C29B9AE5D04E4A0AA6D66233BE6337EF'}
--: {'new': [243, 52, 155, 46], 'old': [243, 52, 155, 46], 'name': '2196FC9BE9764955879F8112B5D3FAA8'}
--: {'new': [25, 52, 160, 44], 'old': [25, 52, 160, 44], 'name': '015BFEDE64284A82B71FC43B2304491C'}
'''
from operator import itemgetter,attrgetter

a = (897, 65, 88, 82)
b = (459, 53, 155, 46)
c = (270, 52, 155, 46)
d = (25,  3, 160 ,44)
e = (25,  1, 160 ,44)
f = (25,  2, 160 ,44)

list1 = [a,b,c,d,e,f]
print list1

list2 = sorted(list1,key=lambda e:e[0])
print list2

#用operator
list3 = sorted(list1,key=itemgetter(0,1))
print list3



from math import sqrt
x0,y0 = 0,3
x1,y1 = 4,0

print y1*y1
print sqrt((x0-x1)*(x0-x1) + (y0-y1)*(y0-y1))

            














