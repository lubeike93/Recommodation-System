import numpy as np
import pandas as pd
from numpy import array
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import jieba
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
import re


#### read exel sheet
data_post_details_raw = pd.read_excel("帖子详情表.xlsx")
data_post_details_raw = data_post_details_raw.drop_duplicates(['帖子网址'])

data_post_details_raw = data_post_details_raw[['作者id', '观看数', '回复数', '点赞数', '收藏数', '标签1', '标签2',
                                               '标签3', '标签4', '标签5', '标签6', '帖子标题']]

#####提取
row_number_data_post = data_post_details_raw.shape[0]
column_number_data_post = data_post_details_raw.shape[1]
data_post_details_raw = pd.DataFrame(data_post_details_raw).fillna(method="ffill")
data_post_details_raw = data_post_details_raw.values  ###convert the values into num array

def remove_punctuation(line):
    rule = re.compile(u'[^\u4E00-\u9FA5]')
    line = rule.sub('',line)
    return line

for i in range (0, row_number_data_post):
    for j in range (5, 11):
     string = data_post_details_raw[i,j]
     string = remove_punctuation(string)
     data_post_details_raw[i,j] = string


data_post_details_raw = pd.DataFrame(data_post_details_raw).fillna(method="ffill")
data_post_details_raw = data_post_details_raw.values  ###convert the values into num array



X_post = np.zeros((row_number_data_post, 5))
X_post[:, 0:5] = data_post_details_raw[:, 0:5]

X_post = preprocessing.normalize(X_post)


print(np.shape(X_post))


for j in range(6, column_number_data_post-1):
    data_post = data_post_details_raw[:, j]
    values_post = array(data_post)
    # integer encode
    label_encoder = LabelEncoder()
    label_encoder = label_encoder
    integer_encoded = label_encoder.fit_transform(values_post)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    X_post = np.hstack((X_post, onehot_encoded))
print(X_post)



###提取并且处理评论中的文字并转换成向量
X_post_data_comment = data_post_details_raw[:, 11]

seg_list = jieba.cut_for_search(X_post_data_comment[0])
X_post_final = " ".join(seg_list)

for k in range(1, row_number_data_post):
 seg_list = jieba.cut_for_search(X_post_data_comment[k])
 a = " ".join(seg_list)
 X_post_final = np.hstack((X_post_final, a))


# integer encode the documents
vocab_size = 100
X_post_comment = [one_hot(d, vocab_size) for d in X_post_final]

# pad documents to a max length of 50 words
max_length = 50
X_post_data_comment_in_array = pad_sequences(X_post_comment, maxlen=max_length, padding='post')
print((X_post_data_comment_in_array))

