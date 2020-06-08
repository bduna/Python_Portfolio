# Author: Barrett Duna

from testfixtures import ShouldRaise


def validate_input(*type_args, kw_type_dict=None):
	"""
	Decorator to validate the input to a function.
	"""
	def inner(func):
		def wrapper(*args, **kwargs):

			# ensure both functions have same number of positional arguments
			if len(type_args) != len(args):
				raise Exception('Differing number of positional arguments.')

			# handle positional arguments
			for type_arg, arg in zip(type_args, args):
				if type_arg is not type(arg):
					raise Exception('Invalid type supplied in positional argument.')

			# handle keyword arguments
			if kw_type_dict is not None:
				for arg_name, arg_type in kw_type_dict.items():
					if (arg_name in kwargs) and (arg_type is not type(kwargs[arg_name])):
						raise Exception('Keyword {} has invalid type.'.format(arg_name))

			# execute decorated function
			return func(*args, **kwargs)
		return wrapper
	return inner


@validate_input(int)
def f_one(n):
	return n

@validate_input(str)
def f_two(s):
	return s

@validate_input(kw_type_dict={"kw_one": int, "kw_two": str})
def f_three(kw_one=0, kw_two=""):
	return str(kw_one) + kw_two

@validate_input(int, float, kw_type_dict={"kw_one": int, "kw_two": float})
def f_four(n, x, kw_one=0, kw_two=3.14159):
	return n + x + kw_one + kw_two


# f_one(n) tests
assert f_one(1) == 1
with ShouldRaise():
	f_one(3.14159)
with ShouldRaise():
	f_one("3.14159")

# f_two(s) tests
assert f_two("3.14159") == "3.14159"
with ShouldRaise():
	f_two(1)

# f_three(kw_one=0, kw_two="")
assert f_three() == "0"
with ShouldRaise():
	f_three(kw_one="abc", kw_two="")
with ShouldRaise():
	f_three(kw_one=0, kw_two=0)

# f_four(n, x, kw_one=0, kw_two=3.14159) tests
assert f_four(0, 0.0, kw_one=0, kw_two=0.0) == 0
assert f_four(0, 0.0) == 3.14159
with ShouldRaise():
	f_four("abc", 0.0, kw_one=0)
with ShouldRaise():
	f_four(0, 1, kw_one=0, kw_two=0.0)
with ShouldRaise():
	f_four(0, 0.0, kw_one=0, kw_two="abc")



