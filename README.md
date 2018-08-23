根据用户喜好的推荐系统

User_matrix_generation

	•	依据用户的exel 表格将使用的数据转化成数据矩阵。
	•	将数据矩阵的元素one hot 转码
	•	输出的X_user 是转码后的用户矩阵

Sight_matrix_generation

	•	依据用户的exel 表格将使用的数据转化成数据矩阵。
	•	将数据矩阵的元素one hot 转码
	•	输出的X_post是转码后的帖子矩阵


User_character_generation

	•	神经网路输出Y 为0或者1。0是不推荐， 1 是推荐。因为在评论表中帖子跟用户是一一对应，所以这种情况输出神经网络所有输出为1。因此打乱评论  表中一半的用户列表， 输出端一半为0， 一半为1。 
	
	•	打乱一半的用户后，对应用户景点特征向量对应的进行了调整

Sight_character_generation

	•	同样根据新的输出端Y,调整景点的特征向量

biuld_tensor

	•	搭建神经网络
	
      运行此程序即可， 此程序中的函数从调用
