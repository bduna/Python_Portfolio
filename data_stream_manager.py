# Author: Barrett Duna

from abc import ABC, abstractmethod


class DataStreamManager:
	"""
	Manages the communication and processing of a data stream to
	multiple components of an application. The DataStreamManager
	implements a subscription model where objects of classes derived
	from the abstract base class DataStreamUser can subscribe and
	unsubscribe from the data stream.

	Each class derived from DataStreamUser must implement the process
	method which is the method that let's the derived object receive and
	make use of the data.

	This code architecture can be used in applications that
	have many different components needing access to the same
	data stream.
	"""
	def __init__(self):
		self.subscribers = []

	def subscribe(self, subscriber):
		if subscriber in self.subscribers:
			raise ValueError("Multiple subscriptions not allowed.")
		if not issubclass(type(subscriber), DataStreamUser):
			raise ValueError("Input is not a valid type of subscriber.")
		self.subscribers.append(subscriber)

	def unsubscribe(self, subscriber):
		if subscriber not in self.subscribers:
			raise ValueError("Can only unsubscribe subscribers.")
		self.subscribers.remove(subscriber)

	def process(self, data):
		for subscriber in self.subscribers:
			subscriber.process(data)


class DataStreamUser(ABC):
	"""
	DataStreamUser is an abstract base class that simply
	enforcers that any derived "data stream user" class
	implements the process method. It also provides
	the functionality to subscribe and unsubscribe to
	the data stream.
	"""
	def __init__(self, dsm):
		self.dsm = dsm

	def subscribe(self):
		self.dsm.subscribe(self)

	def unsubscribe(self):
		self.dsm.unsubscribe(self)

	@abstractmethod
	def process(self, data):
		pass


if __name__ == '__main__':

	class DataStreamUserUpper(DataStreamUser):
		"""
		DataStreamUserUpper class is derived from the abstract
		base class DataStreamUser. This requires it at least
		implements the process method. In this class' case,
		it simply prints the string data in all upper-case
		letters.
		"""
		def process(self, data):
			print(data.upper())


	class DataStreamUserLower(DataStreamUser):
		"""
		DataStreamUserLower class is derived from the abstract
		base class DataStreamUser. This requires it at least
		implements the process method. In this class' case,
		it simply prints the string data in all lower-case
		letters.
		"""
		def process(self, data):
			print(data.lower())


	# create DataStreamManager object
	dsm = DataStreamManager()

	# create data stream user number
	# one and subscribe the user to the data
	dsu_one = DataStreamUserUpper(dsm)
	dsu_one.subscribe()

	# simulate data using input and trigger
	# data stream user to process new data
	input_one = input("Input: ")
	dsm.process(input_one)

	# create and subscribe data stream user
	# number two
	dsu_two = DataStreamUserLower(dsm)
	dsu_two.subscribe()

	# get new simulated data
	input_two = input("Input: ")
	dsm.process(input_two)

	# unsubscribe data stream user one
	dsu_one.unsubscribe()

	# get new simulated data
	input_three = input("Input: ")
	dsm.process(input_three)
