import json,sys
sys.path.insert(0,'scripts')
from blueprint_src import CH
VC=[28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35]
bad=0
for n in range(1,49):
    t=json.load(open(f'txt/{n:02d}.json'))
    assert len(t)==VC[n-1]
    ch=CH[n]; secs=ch[3]; pts=ch[4]
    for name,lst in (('sec',[(a,z) for a,z,_ in secs]),('pts',[(a,z) for _,a,z,_ in pts])):
        if lst[0][0]!=1 or lst[-1][1]!=VC[n-1] or any(lst[i][0]!=lst[i-1][1]+1 for i in range(1,len(lst))):
            print(n,name,'非連續/未覆蓋',lst); bad+=1
    if not 4<=len(secs)<=7 or len(pts)!=3: print(n,'數量');bad+=1
    for p,a,z,q in pts:
        txt=''.join(t[a-1:z])
        if q not in txt: print(n,f'引句不在{a}-{z}:',q); bad+=1
print('bad',bad)
