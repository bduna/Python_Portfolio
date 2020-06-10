class Singleton:

	singleton = None

	def __new__(cls, *args, **kwargs):
		if cls.singleton is None:
			cls.singleton = super().__new__(cls, *args, **kwargs)
			return cls.singleton
		else:
			raise Exception(f'Only one instance of class {cls.__name__} can be created.')


# creates singleton
singleton = Singleton()
print(type(singleton))

# raises exception
singleton_two = Singleton()







