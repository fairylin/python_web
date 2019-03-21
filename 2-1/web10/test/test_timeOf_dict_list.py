import time

query_list = [-60000,-6000,-600,-60,-6,0,6,60,600,6000,60000]

l = []
d = {}

for i in range(10000000):
    l.append(i)
    d[i] = 1

start_time1 = time.time()
for v in query_list:
    if v in l:
        # print(v,)
        continue
end_time1 = time.time()

start_time2 = time.time()
for v in query_list:
    if v in d:
        # print(v,)
        continue
end_time2 = time.time()

print('list search time is:%f' % (end_time1 - start_time1))
print('list search time is:%f' % (end_time2 - start_time2))
