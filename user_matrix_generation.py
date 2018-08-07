import numpy as np
import pandas as pd
from numpy import array
import xlsxwriter
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.datasets import load_iris
from sklearn import preprocessing


#### read exel sheet
data_user_raw = pd.read_excel("用户data.xlsx")
data_user_raw = data_user_raw.drop_duplicates(['评论用户id'])
data_user_raw = data_user_raw[['性别','年', '月', '日','旅行偏好1', '旅行偏好2', '旅行偏好3', '旅行偏好4',
                               '旅行偏好5','去过的城市1','去过的城市2','去过的城市3','去过的城市4','去过的城市5',
                               '去过的城市6','去过的城市7','去过的城市8','去过的城市9','去过的城市10']]


data_user_raw = data_user_raw.values
####填补却少的数据 先用上一个的数据去填补
data_user_raw = pd.DataFrame(data_user_raw).fillna(method="ffill")
data_user_raw = data_user_raw.values


#####提取
row_number_user = data_user_raw.shape[0]
column_number_user = data_user_raw.shape[1]

X_user = np.zeros((data_user_raw.shape[0], 5))

# 生日转化成神经网络的入， 可是一半都是无效生日
X_user[:, 2] = data_user_raw[:, 1]##年
X_user[:, 3] = data_user_raw[:, 2]##月
X_user[:, 4] = data_user_raw[:, 3]##日

X_user = preprocessing.normalize(X_user)


#讲性别转化成数字

for i in range(0, row_number_user):

 if data_user_raw[i, 0] == '女':
      block = np.array([1,0])
 elif data_user_raw[i,0] == '男':
      block = np.array([0,1])
 else:
      block = np.array([0,0])

 X_user[i, 0:2] = block


"将汉字转化为向量"
print(np.shape(X_user))
for j in range(7, column_number_user):
    data = data_user_raw[:, j]
    values = array(data)
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    X_user = np.hstack((X_user, onehot_encoded))
print(np.shape(X_user))
