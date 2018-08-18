class UserData():
	def __init__(self):
		self._recipe_id = None
		self._recipe_step = None
		self._scraping_result = {}

	def isset(self):
		return self._recipe_id != None

	@property
	def recipe_id(self):
		return self._recipe_id

	@recipe_id.setter
	def recipe_id(self, value):
		# validation
		if not value.isdigit(): return

		self._recipe_id = value
		# クローリング
		# self._scraping_result[""] = "hogehoge"
		self._recipe_step = 0

	@property
	def recipe_step(self):
		return self._recipe_step
	

	def next_step(self):
		if self._recipe_step != None:
			self._recipe_step = self._recipe_step + 1

userdata = UserData()