import pandas as pd
import numpy as np
import re
from sight_matrix_generation import X_post

data_comment_raw = pd.read_excel("评论表.xlsx")
data_comment_raw = data_comment_raw[['id', '评论用户id', '帖子网址']]
data_comment_raw = data_comment_raw.values
data_post = pd.read_excel("帖子详情表.xlsx")
data_post = data_post[['帖子id']].drop_duplicates()
data_post = data_post.values


row_data_comment_raw = data_comment_raw.shape[0]
column_data_comment_raw = data_comment_raw.shape[1]
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

for i in range (0, data_post.shape[0]):
    string_post = data_post[i, 0]
    string_post = remain_number(string_post)
    data_post[i, 0] = string_post

##data_comment_new 是根据 Y 的新 order
post_ID = np.zeros((row_data_comment_raw, 1))
order_num_post = np.arange(0, row_data_comment_raw, 1).reshape(row_data_comment_raw, 1)
post_ID= data_comment_raw[:, 2].reshape(row_data_comment_raw, 1)##帖子顺序

true_row_post_ID_test = np.zeros((post_ID.shape[0], 1))
for j in range (0, row_data_comment_raw):
 a= post_ID[j, 0] in data_post
 true_row_post_ID_test[j,0]  = a


true_row_post_ID = np.zeros((1, 2))
for j in range (0, row_data_comment_raw):
  a = post_ID[j, 0]
  index = np.argwhere(data_post == a)
  true_row_post_ID = np.vstack((true_row_post_ID, index))
true_row_post_ID = np.delete(true_row_post_ID, 0, axis=0)##true_row_user_ID 是

##制造评论表中用户的特征矩阵
character_of_the_post_in_comment = np.zeros((1, X_post.shape[1]))
for i in range (0, row_data_comment_raw):
    user_character_vector = X_post[int(true_row_post_ID[i, 0]), :]
    character_of_the_post_in_comment = np.vstack((character_of_the_post_in_comment, user_character_vector))
character_of_the_post_in_comment = np.delete(character_of_the_post_in_comment, 0, axis=0)

###character_of_the_post_in_comment 是评论表里面帖子的特征矩阵是一个输入端




