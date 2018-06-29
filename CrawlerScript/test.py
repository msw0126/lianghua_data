# -*- coding:utf-8 -*-

lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
b = [lst[i:i+4] for i in range(0, len(lst), 4)]
print(b)
for i in range(0, len(lst), 4):
    print(i)