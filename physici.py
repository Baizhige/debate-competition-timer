from functools import reduce
def gra_acce_way1(h1,h2,t1,t2):
    
    g=2*((h2/t2)-(h1/t1))/(t2-t1)
    return g

#print (gra_acce_way1(10.0000,100.0000,0.0729,0.3644))

def gra_acce_way2(h1,h2,h3,t1,t2,t3):
    g=(2/(t3-t1))*((h3-h2)/(t3-t2)-(h2-h1)/(t2-t1))
    return g


#print (gra_acce_way1(10.0000,20.0000,0.0729,0.1234))
#print (gra_acce_way2(40.0000,60.0000,100.0000,0.2021,0.2639,0.3644))

arr_h=[10.00,20.00,30.00,40.00,50.00,60.00,70.00,80.00,90.00,100.00]
#arr_h=list(map(lambda x:x-10,arr_h))
#arr_t=[0.0708,0.1154,0.1564,0.1928,0.2241,0.2545,0.2821,0.3036,0.3334,0.3531]
arr_t=[0.0729,0.1234,0.1655,0.2021,0.2345,0.2639,0.2913,0.3168,0.3417,0.3644]
arr_t=list(map(lambda x:x-0.0085,arr_t))  #误差线性修改
arr_y=[]
lengh=len(arr_h)
temp_g=0
g_sum=0
for i in range(0,lengh):
    arr_y.append(arr_h[i]/arr_t[i])
    
for i in range(0,lengh):
    temp_g=gra_acce_way1(arr_h[i-1],arr_h[i],arr_t[i-1],arr_t[i])
    print ("第",i-1,"和第",i,"组算的g值为：",temp_g)
    g_sum+=temp_g
print ("平均值：",g_sum/lengh)
def linearequ(arr_y,arr_t):
    aver_y=reduce(lambda x,y:x+y,arr_y) 
    aver_t=reduce(lambda x,y:x+y,arr_t)
    num=0.0000
    deno=0.0000
    for i in range(0,lengh):
        num+=(arr_y[i]-aver_y)*(arr_t[i]-aver_t)
        deno+=(arr_t[i]-aver_t)*(arr_t[i]-aver_t)
    b=num/deno
    a=aver_y-b*aver_t
    return a,b
    
print (linearequ(arr_y,arr_t))
print ('\n')
print (arr_t)