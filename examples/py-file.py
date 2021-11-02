import random # import random library

# main function
def main(random_int):
	# create variable a
	a="Hello, i'm human #{}".format(random_int)
	# and return it
	return a

if __name__ == "__main__":
	# call main function
	print (main(random.randint(1,1000000)))
