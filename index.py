class Category:
	def __init__(self, name:str):
		self.name = name
		self.ledger = []

	def deposit(self, amount:float, description:str="") -> None:
		self.ledger.append({"amount":amount, "description":description})

	def withdraw(self, amount:float, description:str="") -> bool:
		has_balance = self.check_funds(amount)

		if(not has_balance):
			return False

		self.ledger.append({"amount":-amount, "description":description})
		return True

	def get_balance(self)-> float:
		balance = 0
		for i in self.ledger:
			balance += i["amount"]
		return balance

	def transfer(self, amount:float, category) -> bool:
		has_balance = self.check_funds(amount)

		if(not has_balance):
			return False

		self.withdraw(amount, f'Transfer to {category.name}')
		category.deposit(amount, f'Transfer from {self.name}')

	def check_funds(self, amount:float) -> bool:
		balance = self.get_balance()
		if(balance < amount):
			return False
		return True

	def __repr__(self) -> str:
		lines = []
		title_spaces_to_fill = (30 - len(self.name))//2
		lines.append(("*" * title_spaces_to_fill) + self.name + ("*" * title_spaces_to_fill))
		
		for i in self.ledger:
			spaces_to_fill = 30 - len(str(i["amount"]))
			description_shorter_version = i["description"][:spaces_to_fill-1]
			lines.append(description_shorter_version.ljust(spaces_to_fill) + str(i["amount"]))

		lines.append("Total: {:.2f}".format(self.get_balance()))
		
		str_representations = '\n'.join(lines)
		return str_representations

def create_spend_chart(categories):
	spent_amounts = []
	for category in categories:
		spent = 0
		for item in category.ledger:
			if item["amount"] < 0:
				spent += abs(item["amount"])
		spent_amounts.append(round(spent, 2))

	total = round(sum(spent_amounts), 2)
	spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

	header = "Percentage spent by category\n"

	chart = ""
	for value in reversed(range(0, 101, 10)):
		chart += str(value).rjust(3) + '|'
		for percent in spent_percentage:
			if percent >= value:
				chart += " o "
			else:
				chart += "   "
		chart += " \n"

	footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
	names = list(map(lambda category: category.name, categories))
	max_length = max(map(lambda name: len(name), names))
	names = list(map(lambda name: name.ljust(max_length), names))
	for x in zip(*names):
		footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

	return (header + chart + footer).rstrip("\n")


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)
print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))
