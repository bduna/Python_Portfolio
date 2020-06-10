# Author: Barrett

import numpy as np


class Poly:

	"""
	Poly is a class representing polynomials. It allows various operations
	to be performed on the polynomial objects such as addition, subtraction,
	polynomial products, scalar multiplication, differentiation and
	integration. It also includes root finding, local minimum and
	local maximum numeric methods.

	Each polynomial is callable and when called calculates the polynomial's
	function value at the supplied x. There is a string representation
	supplied which is flexible in the format the polynomial is printed.
	"""

	def __init__(self, *args):
		self.coefs = list(args)

	def __call__(self, x):
		"""
		Polu polynomial class objects are callable and when
		called calculate the polynomial function value at the specified
		x value.
		"""
		rv = 0
		for i in range(len(self.coefs)):
			rv += self.coefs[i] * (x ** i)
		return rv

	def __repr__(self):
		"""
		Method that returns the command necessary to recreate
		the exact polynomial object.
		"""
		str_coefs = [str(c) for c in self.coefs]
		return '{self.__class__.__name__}('.format(self=self) \
		       + ', '.join(str_coefs) + ')'

	def __str__(self,):
		"""
		Method that produces a readable text representation of
		this polynomial object as a string.
		"""

		# print format options
		plus = ' + '
		minus = ' - '
		x_power_str = '^'
		x_str = 'x'

		rstr = ''
		for i in range(len(self.coefs)):

			# get coefficient and create coefficient string
			c = self.coefs[i]
			if abs(c) == 1:
				coef_str = ''
			else:
				coef_str = str(abs(c))

			# concatenate each polynomial term to rstr
			if i == 0:
				rstr += str(self.coefs[i])
			elif i == 1:
				if c == 0:
					pass
				elif c < 0:
					rstr += minus + coef_str + x_str
				else:
					rstr += plus + coef_str + x_str
			else:
				if c == 0:
					pass
				elif c < 0:
					rstr += minus + coef_str + x_str + x_power_str + str(i)
				else:
					rstr += plus + coef_str + x_str + x_power_str + str(i)

		return rstr

	def derivative(self):
		"""
		Returns a polynomial object instance which is the
		derivative of the polynomial object.
		"""
		rv_coefs = self.coefs.copy()
		for i in range(len(rv_coefs)):
			rv_coefs[i] *= i
		return Poly(*rv_coefs[1:])

	def differentiate(self):
		"""
		Differentiates the polynomial object and reassigns
		the value of the polynomial to the derivative.
		"""
		self.coefs = self.derivative().coefs

	def integral(self, c=0):
		"""
		Calculates the integral of the polynomial object and
		returns it as a polynomial object. c is the constant of
		integration and is set to 0 by default.
		"""
		rv_coefs = self.coefs.copy()
		rv_coefs.insert(0, c)
		for i in range(1, len(rv_coefs)):
			rv_coefs[i] /= i
		return Poly(*rv_coefs)

	def integrate(self, c=0):
		"""
		Alters the object by transforming it into it's integral
		with integration constant c supplied in th e function.
		"""
		self.coefs = self.integral(c).coefs

	def degree(self):
		"""
		Returns the degree of the polynomial.
		"""
		return len(self.coefs) - 1

	def __add__(self, other):
		"""
		Defines addition (p + q) of polynomial p and polynomial q.
		Returns a polynomial object that is the sum of the two
		polynomials.
		"""
		num_self = len(self.coefs)
		num_other = len(other.coefs)
		if num_self > num_other:
			other_coefs = other.coefs + [0]*(num_self-num_other)
			return Poly(*[x+y for x, y in zip(self.coefs, other_coefs)])
		else:
			self_coefs = self.coefs + [0]*(num_other-num_self)
			return Poly(*[x+y for x, y in zip(self_coefs, other.coefs)])

	def __sub__(self, other):
		"""
		Defines subtraction (p - q) of polynomial p and polynomial q.
		Returns a polynomial object that is the difference of the two
		polynomials.
		"""
		num_self = len(self.coefs)
		num_other = len(other.coefs)
		if num_self > num_other:
			other_coefs = other.coefs + [0] * (num_self - num_other)
			return Poly(*[x - y for x, y in zip(self.coefs, other_coefs)])
		else:
			self_coefs = self.coefs + [0] * (num_other - num_self)
			return Poly(*[x - y for x, y in zip(self_coefs, other.coefs)])

	def __mul__(self, other):
		"""
		Defines multiplication (p*q) of polynomial p and polynomial q.
		Returns a polynomial object that is the product of the two
		polynomials.

		Uses matrix multiplication to implement the algorithm for speed
		and simplicity of implementation.
		"""
		num_self = len(self.coefs)
		num_other = len(other.coefs)
		num_rows = num_self + num_other - 1
		m = np.zeros((num_rows, num_self))
		for col in range(num_self):
			for i in range(num_other):
				m[col+i, col] = other.coefs[i]
		return Poly(*list(np.dot(m, np.array(self.coefs))))

	def scalar_multiply(self, s):
		"""
		Allows multiplication of a polynomial p by a scalar s
		returning a polynomial object representing s*p.
		"""
		if s == 0:
			self.coefs = [0]
		else:
			self.coefs = [s*c for c in self.coefs]

	def local_minimum(self, start_x, lr=0.01, num_iters=2500):
		"""
		Finds a local or global minimum if one exists using 1d
		gradient descent.
		"""
		derivative = self.derivative()
		lm_x = start_x
		for _ in range(num_iters):
			lm_x = lm_x - lr*derivative(lm_x)
		return lm_x, self(lm_x)

	def local_maximum(self, start_x, lr=0.01, num_iters=2500):
		"""
		Finds a local or global maximum if one exists using 1d
		gradient ascent.
		"""
		derivative = self.derivative()
		lm_x = start_x
		for _ in range(num_iters):
			lm_x = lm_x + lr*derivative(lm_x)
		return lm_x, self(lm_x)

	def definite_integral(self, x1, x2):
		"""
		Calculates the definite integral of the polynomial between x1 and
		x2.
		"""
		integral = self.integral()
		return integral(x2) - integral(x1)

	def find_root(self, start_x, num_iters=2500):
		"""
		Implements Newton's method to find a root of the polynomial.
		start_x is the intitial guess of the root and the algorithm
		iterates from there using Newton's method num_iters number
		of times.
		"""
		root_x = start_x
		derivative = self.derivative()
		for _ in range(num_iters):
			if derivative(root_x) == 0:
				raise ZeroDivisionError('Derivative of polynomial evaluated '
				                        'to zero at current iteration '
				                        'producing division by zero in '
				                        'Newton\'s method.')
			root_x = root_x - self(root_x)/derivative(root_x)
		return root_x, self(root_x)


if __name__ == '__main__':

	p = Poly(1, 2, -5)
	q = Poly(2, -2, 10, -1)
	print("Polynomial P:", p)
	print("Polynomial Q:", q)
	print("Degree of P:", p.degree())
	print("Degree of Q:", q.degree())
	print("P+Q:", p+q)
	print("P-Q:", p-q)
	print("P*Q:", p*q)
	print("Derivative of P: ", p.derivative())
	print("Derivative of Q:", q.derivative())
	print("Integral of P:", p.integral())
	print("Integral of Q:", q.integral())
	print("Root of P: {}".format(*p.find_root(start_x=1)))
	print("Root of P: {}".format(*p.find_root(start_x=-1)))
	print("Root of Q: {}".format(*q.find_root(start_x=1)))
	print("Maximum of P at x={} with maximum value {}".format(
		*p.local_maximum(start_x=1)))

