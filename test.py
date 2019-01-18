
import math

# x=4
# y=6
# a = "jack"
# b = "ffff"
# # print(x+y)
# # print("hi {0} and {1}".format(a, x))
# # print("hi %s and %s" %(a, x))


# xyz = [[4,5,6], "bb", "cc", "dd", "xxx", "yyy"]
# # print(len(xyz))
# new_list = xyz[2:]
# # print(new_list, xyz)
# print(type(xyz[0][1]))
# print(xyz[0])
# ff = [xyz[0][1], xyz[3]]
# print(ff)
# print(  sum(xyz[0])   )

# print(np.sqrt(5))

lis = ["a","b","a","e","e","a"]

num = 0

for i, jack in enumerate(lis):

	# print(i)

	if jack=="a":
		num = num+   1
		# print(num)

print("there were {} occurences of 'a'".format(num))


def adder(x,y):
	# print(x)
	# print(y)
	# return x+y
	return "bla %s, %s" %(x,y)

xx = adder(3,4)
print(xx)



