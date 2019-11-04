from datetime import datetime

d1 = datetime.now()
# d2 = datetime.datetime(2009, 10, 7)
# dayCount = (d1 - d2).days
# print(d1)
# print(type(2009, 10, 7))
# a = '2018-5-22 07:33'
# d2 = datetime.datetime(a.replace('-', ', ').strip(' 07:33'))
# # print(d2)
# print(a.replace('-', ', ').strip(' 07:33'))

d1 = datetime.now()
d3 = '2018-5-22 07:33'.split(' ')[0]
a = datetime.strptime("%s" % d3, "%Y-%m-%d")

# delta = d1 - a
# print((d1 - a).days)
