# Author Barrett Duna


def counter_decorator(counter_var_name, increment=True):
	"""
	counter_decorator is a class method decorator for class functions
	that need to increment or decrement an integer variable such
	as a counter each time the class method is run. Takes in a
	class attribute integer variable name (string) and increments (by default)
	or decrements the class integer variable every time the function is
	called.
	"""
	def inner(func):
		def wrapper(self, *args, **kwargs):
			rv = func(self, *args, **kwargs)
			if increment:
				self.__dict__[counter_var_name] += 1
			else:
				self.__dict__[counter_var_name] -= 1
			return rv
		return wrapper
	return inner


class Counter:
	"""
	Demo class using counter_decorator.
	"""
	def __init__(self):
		self.counter_one = 0
		self.counter_two = 0

	# function_one will increment self.counter_one
	# each time it is run
	@counter_decorator("counter_one")
	def function_one(self):
		pass

	# function_two will decrement self.counter_two
	# each time it is run
	@counter_decorator("counter_two", False)
	def function_two(self):
		pass


# create counter object
c = Counter()

# run and increment counter_one multiple
# times and print results
print("function_one and counter_one...")
print(c.counter_one)
c.function_one()
print(c.counter_one)
c.function_one()
print(c.counter_one)

# run and decrement counter_two multiple
# times and print results
print("function_two and counter_two...")
print(c.counter_two)
c.function_two()
print(c.counter_two)
c.function_two()
print(c.counter_two)
