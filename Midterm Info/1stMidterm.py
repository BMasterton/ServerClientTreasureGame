# def total_populations(dictList:[{}]):
#     newList = []
#     for dic in dictList:
#         total = 0
#         for k,v in dic.items():
#             total += v
#         newList.append(total)
#     return newList
#
#
#
# print( total_populations(  [  {'Canada': 1000, 'USA': 100000},   {'Brazil': 9999, 'Chile': 666}  ]  ) )

from functools import reduce
def max_name_length(nameList:[[]]):
    #trying to figure out how i access the iteration of each accululator check, 0 is a substitute, x and y dont work
    newlist= reduce(lambda x,y: x if len(x[0]) > len(y[0]) else y, nameList)
    print(newlist)
    newerList = reduce(lambda x,y: x if len(x) > len(y) else y, newlist)
    print(newerList)
    return len(newerList)



print(max_name_length([['alice', 'bob', 'eve'], ['dan', 'jim', 'john']]))