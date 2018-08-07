import pandas as pd
import numpy as np
import re
from user_matrix_generation import X_user

data_comment_raw = pd.read_excel("评论表.xlsx")
data_comment_raw = data_comment_raw[['id', '评论用户id', '帖子网址']]
data_comment_raw = data_comment_raw.values
data_user_raw = pd.read_excel("用户data.xlsx")
data_user_raw_user_id = data_user_raw[['评论用户id']].drop_duplicates()
data_user_raw_user_id = data_user_raw_user_id.values


row_data_comment_raw = data_comment_raw.shape[0]
column_data_comment_raw = data_comment_raw.shape[1]

## 定义 Y，前半部分打乱顺序， 输出结果是0， 后半部分是推荐的数据

Y = np.zeros((data_comment_raw.shape[0], 1))
Y_modified = data_comment_raw

amount_of_random = int(data_comment_raw.shape[0] / 2)
amount_of_sequential = int(data_comment_raw.shape[0] - data_comment_raw.shape[0] / 2)
permutation = np.random.permutation(amount_of_random).reshape((amount_of_random, 1))

Y[0:amount_of_random] = 0
Y[amount_of_random + 1: data_comment_raw.shape[0]] = 1


###调整用户矩阵以及景点矩阵的顺序
# 去掉评论中的其他元素

def remain_number(line):
    rule = re.compile(u'[^\u0030-\u0039]')
    line = rule.sub('', line)
    return line

#从评论表链接中倒出评论ID，
for i in range(0, row_data_comment_raw):
    string = data_comment_raw[i, 2]
    string = remain_number(string)
    data_comment_raw[i, 2] = string

true_list = np.arange(amount_of_sequential, row_data_comment_raw, 1).reshape((amount_of_sequential, 1))
order_num = np.vstack((permutation, true_list))##前半段打乱后额顺序

##data_comment_new 是根据 Y 的新order
user_ID = np.zeros((row_data_comment_raw, 1))

for i in range(0, row_data_comment_raw):
    number = order_num[i, 0]
    user_ID[i, 0] = data_comment_raw[number, 1]##打乱后的用户顺序


true_row_user_ID_test = np.zeros((user_ID.shape[0], 1))
for j in range (0, row_data_comment_raw):
 a= user_ID[j, 0] in data_user_raw_user_id
 true_row_user_ID_test[j,0]  = a


true_row_user_ID = np.zeros((1, 2))
for j in range (0, row_data_comment_raw):
  a = user_ID[j, 0]
  index = np.argwhere(data_user_raw_user_id == a)
  true_row_user_ID = np.vstack((true_row_user_ID, index))
true_row_user_ID = np.delete(true_row_user_ID, 0, axis=0)

##制造评论表中用户的特征矩阵
character_of_the_user_in_comment = np.zeros((1, X_user.shape[1]))
for i in range (0, row_data_comment_raw):
    user_character_vector = X_user[int(true_row_user_ID[i, 0]), :]
    character_of_the_user_in_comment = np.vstack((character_of_the_user_in_comment, user_character_vector))
character_of_the_user_in_comment = np.delete(character_of_the_user_in_comment, 0, axis=0)
###character_of_the_user_in_comment 是评论表里面user的特征矩阵是一个输入端




