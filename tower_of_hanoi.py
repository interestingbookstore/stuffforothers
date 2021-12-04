class Stacks:
	def __init__(self, disks):
		self.one = [i + 1 for i in range(disks)]
		self.two = []
		self.three = []

	def check_if_move_is_legal(self, from_stack, to):
		if from_stack == self.one:
			fn = 's1'
		elif from_stack == self.two:
			fn = 's2'
		elif from_stack == self.three:
			fn = 's2'
		else:
			raise TypeError(f"What's a {from_stack}? Please specify self.one, self.two, or self.three")
		if to == self.one:
			tn = 's1'
		elif to == self.two:
			tn = 's2'
		elif to == self.three:
			tn = 's2'
		else:
			raise TypeError(f"What's a {to}? Please specify self.one, self.two, or self.three")

		if not from_stack:
			raise IndexError(f'Tried to move {fn} to {tn}, but {fn} is empty!')
		if to:
			if from_stack[0] > to[0]:
				raise ValueError(f'Tried to move {fn} to {tn}, but {from_stack[0]} > {to[0]}!')

	def stack_one_to_stack_two(self):
		self.check_if_move_is_legal(self.one, self.two)
		self.two.insert(0, self.one.pop(0))

	def stack_one_to_stack_three(self):
		self.check_if_move_is_legal(self.one, self.three)
		self.three.insert(0, self.one.pop(0))

	def stack_two_to_stack_one(self):
		self.check_if_move_is_legal(self.two, self.one)
		self.one.insert(0, self.two.pop(0))

	def stack_two_to_stack_three(self):
		self.check_if_move_is_legal(self.two, self.three)
		self.three.insert(0, self.two.pop(0))

	def stack_three_to_stack_one(self):
		self.check_if_move_is_legal(self.three, self.one)
		self.one.insert(0, self.three.pop(0))

	def stack_three_to_stack_two(self):
		self.check_if_move_is_legal(self.three, self.two)
		self.two.insert(0, self.three.pop(0))

	def move(self, f, t):
		if f == 0:
			fs = self.one
		elif f == 1:
			fs = self.two
		elif f == 2:
			fs = self.three
		else:
			raise TypeError(f"I know of stacks 1, 2, and 3, but what's {f}?")
		if t == 0:
			ts = self.one
		elif t == 1:
			ts = self.two
		elif t == 2:
			ts = self.three
		else:
			raise TypeError(f"I know of stacks 1, 2, and 3, but what's {f}?")
		self.check_if_move_is_legal(fs, ts)
		ts.insert(0, fs.pop(0))

	def __getitem__(self, item):
		if item == 0:
			return self.one
		if item == 1:
			return self.two
		if item == 2:
			return self.three
		raise TypeError(f'{item} was given. Waa?')

	def get_top_disk(self, stack_index):
		if self[stack_index]:
			return self[stack_index][0]
		return None

	def get_bottom_disk(self, stack_index):
		if self[stack_index]:
			return self[stack_index][-1]

	def has_disks(self, stack_index):
		if stack_index == 0:
			if self.one:
				return True
			return False
		if stack_index == 1:
			if self.two:
				return True
			return False
		if stack_index == 2:
			if self.three:
				return True
			return False
		raise TypeError(f"Look, it's like, 1 AM right now. Just specify 0, 1, or 2, okay?")

	def get_disk_above(self, disk_value, stack):
		return self[stack][self[stack].index(disk_value) - 1]

	def get_other_stack(self, stack_1, stack_2):
		return 3 - (stack_1 + stack_2)

	def __str__(self):
		return f's1: {" ".join([str(i) for i in reversed(self.one)])}\ns2: {" ".join([str(i) for i in reversed(self.two)])}\ns3: {" ".join([str(i) for i in reversed(self.three)])}'


stacks = Stacks(4)


# print(stacks)
#
# # stacks.stack_one_to_stack_two()
# stacks.move(0, 2)
#
# print(stacks)

# stacks.show_all_stacks()


# raise Exception

def move_a_disk(disk_value, f, t):
	r = stacks.get_other_stack(f, t)
	# print(f'-----------------------------------------------')
	# print(f'Moving {disk_value} from {f} to {t}')
	# print(f'Before:\n{stacks}')
	# print(f'===============================')

	while True:
		if disk_value > stacks.get_top_disk(f):
			move_a_disk(stacks.get_disk_above(disk_value, f), f, r)
			continue
		if stacks.has_disks(t) and disk_value > stacks.get_top_disk(t):
			move_a_disk(stacks.get_top_disk(t), t, r)
			continue
		break

	print(f'Move {f + 1} to {t + 1}')
	input()
	stacks.move(f, t)


# print(f'--------------------------------')
# print(f'Moving {disk_value} from {f} to {t}')
# print(f'After:\n{stacks}')
# print(f'===================================================')


while stacks.has_disks(0) or stacks.has_disks(1):
	if stacks.has_disks(0):
		move_a_disk(stacks.get_bottom_disk(0), 0, 2)
	elif stacks.has_disks(1):
		move_a_disk(stacks.get_bottom_disk(1), 1, 2)

# print(stacks)
