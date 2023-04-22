n = eval(input())  # 获取用户输入
f = open("三国演义.txt", "r", encoding="utf-8")  # 打开文件
file_content = f.read()
f.close()

dict_str = {}
for i in file_content.strip().replace('\n', ''):
    if i in dict_str:
        dict_str[i] += 1
    else:
        dict_str[i] = 1

list_keys = list(dict_str.keys())
list_value = list(dict_str.values())
list_value.sort(reverse=True)
for i in range(n):
    value = list_value[i]
    key = list_keys[list(dict_str.values()).index(value)]
    print("{}:{}".format(key, value))
