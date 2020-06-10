# Author: Barrett Duna

from abc import ABC, abstractmethod


class DataStreamManager:
	"""
	Manages the communication of a data stream to data stream
	users. It subscribes an object whose class inherits from
	the abstract base class DataStreamUser to the data stream
	and then calls the object's process method on the incoming
	data. Additionally, if the object no longer needs access
	to the data stream, the DataStreamManager can unsubscribe
	a data stream user object.

	This code architecture can be used in applications that
	have many different components needing access to the same
	data stream.
	"""
	def __init__(self):
		self.subscribers = []

	def subscribe(self, subscriber):
		self.subscribers.append(subscriber)

	def unsubscribe(self, subscriber):
		self.subscribers.remove(subscriber)

	def process(self, data):
		for subscriber in self.subscribers:
			subscriber.process(data)


class DataStreamUser(ABC):
	"""
	DataStreamUser is an abstract base class that simply
	enforcers that any derived "data stream user" class
	implements the process method.
	"""
	@abstractmethod
	def process(self, data):
		pass


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


if __name__ == '__main__':

	# create DataStreamManager object
	dsm = DataStreamManager()

	# create data stream user number
	# one and subscribe the user to the data
	dsu_one = DataStreamUserUpper()
	dsm.subscribe(dsu_one)

	# simulate data using input and trigger
	# data stream user to process new data
	input_one = input("Input: ")
	dsm.process(input_one)

	# create and subscribe data stream user
	# number two
	dsu_two = DataStreamUserLower()
	dsm.subscribe(dsu_two)

	# get new simulated data
	input_two = input("Input: ")
	dsm.process(input_two)

	# unsubscribe data stream user one
	dsm.unsubscribe(dsu_one)

	# get new simulated data
	input_three = input("Input: ")
	dsm.process(input_three)
