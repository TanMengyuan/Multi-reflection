# Multi-reflection

此项目准备实现可见光通信中房间内多次反射的冲击响应计算
config.json文件说明：  
"TIME_ARRAY_LENGTH": 时间序列的长度，以20ns的时间为例，长度为200时每一段的时间dt为0.1ns  
"MAXIMUM_TIME": 冲击响应需要计算的最长时间，冲击响应如果超过该时间则不会统计  
"REFLECT_TIMES": 反射次数