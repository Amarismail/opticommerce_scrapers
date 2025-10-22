a_list = [1,2,3,4]
for ind, value in enumerate(a_list):
    print(value)
    print(a_list)
    if value == 2:
        a_list.append(5)
    print(a_list)