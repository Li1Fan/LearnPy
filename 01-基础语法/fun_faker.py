from faker import Faker

fake = Faker()
print(fake.name(), fake.email(), fake.country(), fake.profile())
#
# # import pywhatkit
# # pywhatkit.text_to_handwriting('''Learning Python from the basics is extremely important. Before starting to learn python,understanding a base language like c is a must and some of the oops concepts.Python program has many modulesand packages, which helps with efficient programming.
# # Understanding these modules and 1proper usage of many syntax and libraries is recommended.
# # In this article, a few modules and packages are used in the program. 
# # Python includes tons of libraries and some of them are quiet intresting''')
#
# import matplotlib.pyplot as plt
# Partition = 'Holidays', 'Eating_Out', 'Shopping', 'Groceries'
# sizes = [250, 100, 300, 200]
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=Partition, autopct='%1.1f%%', shadow=False, startangle=90)
# ax1.axis('equal')
# plt.show()
#
# import pyautogui
# num=int(input("Enter a value to divide 100"))
# if num == 0:
#     pyautogui.alert(" Alert!!! 100 cannot be divided by 0")
# else:
#     print(f'The value is {100/num}')

# import pyttsx3
# engine = pyttsx3.init()
# engine.say("厉害了呀")
# engine.runAndWait()