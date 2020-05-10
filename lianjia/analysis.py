import re
import pandas as pd
import numpy as np
import pymongo

#引入数据库
client = pymongo.MongoClient('localhost', 27017)
database = client['链家']
collection = database['北京二手房']
data = pd.DataFrame(list(collection.find()))
danjia = data[['单价']]
mianjia = data[['面积']]
#mianji = re.findall(r"\d+\.?\d*", mianjia)
#print(mianji)
#zongjia =





data = data[['标题','总价','小区','区','商圈','挂牌时间','户型','面积','梯户比例','楼层','用途','关注人数','朝向','供暖方式','电梯','单价','介绍','ID']]

#print(type(danjia))

#print(data)

'''
目标： 最值 （总价、单价、面积、户型、关注人数）
价格分布区间 面积分布 小区数量最多
面积和关注的散点图
'''



#单价大于18万的
print(data[data['单价']>18][['总价','关注人数','单价','ID']])

#按总价排序
print( data.sort_values(by='总价', ascending=False)[0:10][['总价','单价','ID']])

#按单价排序
print( data.sort_values(by='单价', ascending=False)[0:10][['单价','总价','ID']])

#供暖方式分布
print( data.loc[:,'供暖方式'].value_counts()[0:2])

#数量最多的10个小区
print( data.loc[:,'小区'].value_counts()[0:10])

#数量最多的价格
print( data.loc[:,'总价'].value_counts()[0:10])

#数量最多的区
print( data.loc[:,'区'].value_counts()[0:3])

#数量最多的商圈
print( data.loc[:,'商圈'].value_counts()[0:10])



