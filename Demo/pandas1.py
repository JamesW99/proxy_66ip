import baostock as bs
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name":['james','peter','ben'],
    'gender':['male','male','femail'],
    'age':['18','80','33']
})

print(type(df))
print(df['age'].max())


titanic = pd.read_csv('/Users/james/Downloads/titanic.csv')
print(titanic.head(10))


dates = pd.date_range('20130101', periods=6)
#print(dates)
#random:生成6*4的矩阵，随机甜数
#index：行名，0开始。现在为日期
#columns：列名
df = pd.DataFrame(np.random.randn(6,4),index=dates, columns=list('ABCD'))
print(df)
print(df.T)#矩阵转制，行列对掉


#axis: 0控制index， 1控制columns
df.sort_index(axis=1, ascending=False)


#以B为准，生序排列整个数组
df.sort_values(by='B')
#B相等看C
df.sort_values(by=['B','C'])



#切片
#显示前三行
df[0:3]
#显示BC
df[['B','C']]


#2,3等仓,多个列
titanic[titanic['Pclass'].isin([2,3])]

#非空数据
titanic[titanic['Age'].notna()]

#输出某范围数据方块 从<9，2>,<24,5>
titanic.iloc[9:24,2:5]




#选择Age大于35的
titanic[titanic['Age']>35]
#选择Age大于35的Name
titanic.loc[titanic['Age']>35],'Name'
#选择Age大于35的Name和Pclass
titanic[titanic['Age']>35][['Pclass','Name']]
