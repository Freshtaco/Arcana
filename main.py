#!/usr/bin/python3

import random
from sys import exit as exit
import subprocess


class Main:

	def __init__(self):

		self.player = 0
		self.map = 0
		self.tile = (0,0)
		self.tile_loot = ""
		self.npc_loot = []
		self.game_choice = ""
		self.equip_types = {}
		self.fight_roster = []
		self.fight_roster_enemies = []
		self.fight_introtext = "\nA fight starts between you and "
		self.fight_choice = ""
		self.fight_choice_group = ""
		self.fight_opponent = ""

		self.map_min = [0,0]
		self.map_max = [19,4]

		self.menu_text = ("\nWelcome to Arcana!\n"
						"What would you like to do?\n\n"
						"\n1. New Game\n2. Load Game (not implemented)\n"
						"\n0. Exit\n"
						"\n\n>: ")
		self.menu_choice = "0"
		self.menu()

	def menu(self):
		
		while True:
			self.menu_choice = input(self.menu_text)

			if self.menu_choice == "1":
				self.newgame()
				self.gameloop()
			elif self.menu_choice == "2":
				self.loadgame()
				self.gameloop()
			elif self.menu_choice == "0":
				exit("Exiting Arcana...")
				
	def newgame(self):
		self.player = Player(input("Please enter your character's name:\n>: "))
		print("Welcome,", self.player.name, "\nYour adventure begins now ...\n")
		self.map = Map((0,0))
		print("You awake to a bright light\nshining on your eyes..")
		print("As you get up from the ground and\ndust yourself off you see the sun")
		print("rising through the trees.")
		print("\ntype 'help' to show available commands.")

	def loadgame(self):
		None

	def playerdeath(self):
		print("you died!")

	def durabilitymanager(self, item):
		if random.randint(0, 100) >= item.durability:
			item.durability_real -= 1
			for equip in self.equip_types.values():
				if equip.durability_real == 0:
					print("Your", equip.name, "broke!")
					equip = Item.Empty()


	def fight(self):

		def hitcheck(accuracy):
			if random.randint(0, 100) < accuracy:
				return True
			else:
				return False

		if self.fight_roster:
			for npc in self.fight_roster:
				self.fight_introtext += npc.name
			print(self.fight_introtext)
			self.fight_roster_enemies = self.fight_roster.copy()
			self.fight_roster += [self.player]
			# sort fighters by speed
			self.fight_roster.sort(key=lambda roster: roster.speed, reverse=True)
			
			while True:
				for enemy in self.fight_roster_enemies:
					if enemy.hitpoints > 0:
						break
				else:
					print("\nThe fight was won!")
					print("You gained experience!") # implement exp
					return 0

				for fighter in self.fight_roster:
					if fighter.hitpoints > 0:
						print("\n"+fighter.name+"'s turn!")

						if fighter.type == "player":

							while True:
								self.fight_choice = input(">:").lower()
								self.fight_choice = self.fight_choice.split(" ")
								if self.fight_choice[0] == "help":
									print("attack, spells, stats, run")

								elif self.fight_choice[0] == "stats":
									self.choiceStats()

								elif self.fight_choice[0] in ["attack", "spells", "run"]:
									break
								else:
									print("unknown command", self.fight_choice[0])
									print("use 'help' to see available commands")
									continue
							
							if self.fight_choice[0] == "attack":
								if len(self.fight_roster_enemies) != 1:
									while True:
										print("Who do you want to attack?\n")
										for enemy in self.fight_roster_enemies:
											print(self.fight_roster_enemies.index(enemy)+1, enemy.name)
										self.fight_choice_group = input("\n>: ")
										if self.fight_choice_group == "stats":
											for enemy in self.fight_roster_enemies:
												self.inspectprint(enemy, brief=True)
										else:
											try:
												self.fight_opponent = self.fight_roster_enemies[int(self.fight_choice_group)-1]
												print("you attack and deal", fighter.getAttack(), "damage")
												self.fight_opponent.hitpoints -= fighter.getAttack()
												self.durabilitymanager(self.fighter.weapon)
												print("{}({}) has {} HP left".format(self.fight_opponent, self.fight_choice_group, self.fight_opponent.hitpoints))
												break
											except:
												print("invalid option '{}'".format(self.fight_choice_group))

								elif hitcheck(fighter.accuracy):
									print("You attack and deal", fighter.getAttack(), "damage")
									self.fight_roster_enemies[0].hitpoints -= fighter.getAttack()
									print(self.fight_roster_enemies[0].name, "has", self.fight_roster_enemies[0].hitpoints, "HP left")
									self.durabilitymanager(fighter.weapon)
								else:
									print("You attacked but missed your target.")

						else:
							if hitcheck(fighter.accuracy):
								if fighter.strength >= self.player.getArmor():
									print(fighter.name, "hit you for", fighter.strength, "damage.")
									if fighter.strength >= self.player.hitpoints:
										return 1 # playerdeath
									else:
										self.player.hitpoints -= (fighter.strength - int(round(self.player.getArmor()/2)))
										print("You have", self.player.hitpoints, "HP left.")
								else:
									print(fighter.name, "hit you but your armor saved you")
									self.durabilitymanager()
							else:
								print(fighter.name, "missed the attack on you.")
					
					elif fighter.hitpoints <= 0:
						if fighter.type == "player":
							return 1 # playerdeath
						else:
							self.fight_roster.pop(self.fight_roster.index(fighter))

	def inspectprint(self, item, brief=False):
		if item.type == "weapon":
			print("Name: {}\nType: {}\nAttack: {}\nDurability: {}/{}\nWeight: {}\n{}".format(item.name, item.type.capitalize(), item.attack, item.durability_real, item.durability, item.weight, item.description))
			return 1
		elif item.type == "potion":
			print("")
			return 1
		elif item.type == "npc":
			if brief:
				print("Name: ", item.name)
				print("HP:", item.hitpoints)
				print("Attack:", item.strength, "\n")
			else:
				print(item.description)
				return 1
		elif item.type in ["head", "pants", "chest"]:
			print("Name: {}\nArmor Rating: {}\nWeight: {}\nDurability: {}/{}\n{}".format(item.name, item.armor, item.weight, item.durability_real, item.durability, item.description))
			return 1
		elif item.type == "empty":
			print("Nothing")
			return 1
		else:
			return 0

	def gameloop(self):

		self.equip_types = {
			"head": self.player.head,
			"chest": self.player.chest,
			"pants": self.player.pants,
			"weapon": self.player.weapon
		}

		while True:
			
			if self.map.tile != self.tile:
				self.map.__init__(self.tile)

				self.fight_roster = []
				for npc in self.map.current.npc_list:
					if (npc.alignment == -1) and (npc.hitpoints != 0):
						self.fight_roster += [npc]

				if self.fight_roster:
					self.map.current.introtext_hostile()
					if self.fight() != 0:
						self.playerdeath()
				else:
					self.map.current.introtext()

			self.game_choice = input("\n>:")
			self.game_choice = self.game_choice.split(" ")
			
			if self.game_choice[0] == "help":
				print(", ".join(self.map.current.commands))
			
			elif self.game_choice[0] in ["0", "exit"]:
				break
			
			elif self.game_choice[0] in self.map.current.commands:
				
				if self.game_choice[0] == "look":
					self.choiceLook()

				if self.game_choice[0] == "move":
					self.choiceMove()
				
				elif self.game_choice[0] == "bag":
					self.choiceBag()

				elif self.game_choice[0] == "loot":
					self.choiceLoot()

				elif self.game_choice[0] == "throw":
					self.choiceThrow()

				elif self.game_choice[0] == "inspect":
					self.choiceInspect()

				elif self.game_choice[0] == "equip":
					self.choiceEquip()

				elif self.game_choice[0] == "stats":
					self.choiceStats()

			else:
				print("unknown command", self.game_choice[0])

	def choiceLook(self):
		try:
			self.map.current.look(self.game_choice[1])
		except IndexError:
			print("'look' requires an additional argument (north/east/south/west)")

	def choiceMove(self):

		try:
			# cast to list to change values
			self.tile = list(self.tile)

			# (0/0) = (vertical/horizontal) - 0/0 at bottom left
			if self.game_choice[1] == "north":
				self.tile[0] += 1
				if (self.tile[0] > self.map_max[0]) or (self.tile[0] < self.map_min[0]):
					self.tile[0] -= 1
					self.map.current.oob("north")
			elif self.game_choice[1] == "east":
				self.tile[1] += 1
				if (self.tile[1] > self.map_max[1]) or (self.tile[1] < self.map_min[1]):
					self.tile[1] -= 1
					self.map.current.oob("east")
			elif self.game_choice[1] == "south":
				self.tile[0] -= 1
				if (self.tile[0] > self.map_max[0]) or (self.tile[0] < self.map_min[0]):
					self.tile[0] += 1
					self.map.current.oob("south")
			elif self.game_choice[1] == "west":
				self.tile[1] -= 1
				if (self.tile[1] > self.map_max[1]) or (self.tile[1] < self.map_min[1]):
					self.tile[1] += 1
					self.map.current.oob("west")
		
		except IndexError:
			print("'move' requires an additional argument (north/east/south/west)")
		
		finally:
			# always cast back to tuple
			self.tile = tuple(self.tile)

	def choiceBag(self):
		print("Bag contents:")
		for item in self.player.bag:
			print("- ", item.name)

	def choiceLoot(self):

		try:
			if self.map.current.npc_list:
				for npc in self.map.current.npc_list:
					if " ".join(self.game_choice[1:]) == npc.name:
						print("you loot", npc.name, "and find:")
						if npc.bag:

							self.npc_loot = npc.bag.copy()
							for item in self.npc_loot:

								print(item.name,"\n",item.description,"\n")
								if input("Do you want to loot {} ?\n>:".format(item.name)).lower() in "yes":
									for player_item in self.player.bag:
										if player_item.name == "Empty":
											self.player.bag[self.player.bag.index(player_item)] = item
											npc.bag.pop(npc.bag.index(item))
											print("You looted", item.name, "!")
											break
									else:
										print("your bag is full!")
										print("use 'throw' to throw away things from your bag")
										break
							#npc.bag = self.npc_loot
							self.npc_loot = []

						else:
							print("nothing to loot from", npc.name)

				# !! implement map.current.items

			if self.game_choice[1] == "tile":
				if not self.map.current.tile_searched:
					if self.map.current.items:
						for player_item in self.player.bag:
							if player_item.name == "Empty":
								self.tile_loot = random.choice(self.map.current.items)
								self.player.bag[self.player.bag.index(player_item)] = self.tile_loot
								print("you found {}".format(self.tile_loot.name))
								self.map.current.items.pop(self.map.current.items.index(self.tile_loot))
								self.map.current.tile_searched = True
								break
						else:
							print("your bag is full!")
							print("use 'throw' to throw away things from your bag")
					else:
						self.map.current.tile_searched = True
						print("you scoured everything in the area")
						print("but came out empty-handed...")
				else:
					print("You already searched this tile")
			
			if (" ".join(self.game_choice[1:]) not in [npc.name for npc in self.map.current.npc_list]) and (self.game_choice[1] != "tile"):
				print("no lootable object called", self.game_choice[1])

		except IndexError as e:
			#print(e.message)
			print("'loot' requires an additional argument:")
			print("E.g.: loot (thing to loot or pick up)")

	def choiceThrow(self):
		try:
			for item in self.player.bag:
				if " ".join(self.game_choice[1:]) == item.name.lower():
					if item.name != "Empty":
						self.map.current.items.append(item)
						print("you threw away", item.name)
						self.player.bag[self.player.bag.index(item)] = Item.Empty()
						break
			else:
				print("item '{}' not found in your bag".format(" ".join(self.game_choice[1:])))
		except IndexError:
			print("'throw' requires an additional argument:")
			print("check your bag for things to throw away")

	def choiceInspect(self):
		try:
			self.game_choice[1]
			for item in self.player.bag:
				if " ".join(self.game_choice[1:]) == item.name.lower():
					if self.inspectprint(item):
						break
			else:
				for item in self.map.current.items:
					if " ".join(self.game_choice[1:]) == item.name.lower():
						print("you pick up the", item.name, "from the ground\n")
						if self.inspectprint(item):
							print("\nuse 'loot' to put the item in your bag")
							break
				else:
					for npc in self.map.current.npc_list:
						if " ".join(self.game_choice[1:]) == npc.name.lower():
							if self.inspectprint(npc):
								break
					else:
						print("cannot inspect", " ".join(self.game_choice[1:]))
						print("no such item on tile")

		except IndexError:
			print("'inspect' requires and additional argument")

	def choiceEquip(self):
		try:
			for item in self.player.bag:
				if " ".join(self.game_choice[1:]).lower() == item.name.lower():

					try:
						if self.equip_types[item.type].type != "empty":
							for player_item in self.player.bag:
								if player_item.type == "empty":
									self.player.bag[self.player.bag.index(player_item)] = self.equip_types[item.type]
									if item.type == "head":
										self.player.head = item
									elif item.type == "chest":
										self.player.chest = item
									elif item.type == "pants":
										self.player.pants = item
									elif item.type == "weapon":
										self.player.weapon = item
									print(player_item.name, "equipped successfully")
									self.player.bag[self.player.bag.index(item)] = Item.Empty()
									break
							else:
								print("no room in bag for equipment change!")
								print("use 'throw' to throw away items.")

						else:
							if item.type == "head":
								self.player.head = item
							elif item.type == "chest":
								self.player.chest = item
							elif item.type == "pants":
								self.player.pants = item
							elif item.type == "weapon":
								self.player.weapon = item
							self.player.bag[self.player.bag.index(item)] = Item.Empty()
							print(item.name, "equipped successfully")

					except KeyError:
						print(item.name, "cannot be equipped")

		except IndexError:
			print("'equip' requires an additional argument.")
			print("check your 'bag' for equippable gear and weapons!")

	def choiceStats(self):
		print("Name: {}\nLevel: {}\nHP: {}\nMP: {}\nStrength: {}\nAccuracy: {}".format(self.player.name, self.player.level, self.player.hitpoints, self.player.manapoints, self.player.strength, self.player.accuracy))
		print("\nHead Armor:")
		self.inspectprint(self.player.head)
		print("\nChest Armor:")
		self.inspectprint(self.player.chest)
		print("\nLeg Armor:")
		self.inspectprint(self.player.pants)
		print("\nWeapon:")
		self.inspectprint(self.player.weapon)

class NPC:

	def __init__(self, hitpoints, manapoints, strength, speed, level, accuracy, name, items, alignment, description):
		self.type = "npc"
		self.hitpoints = hitpoints
		self.manapoints = manapoints

		self.bag = []
		self.bag.extend(items)

		self.strength = strength
		if self.bag:
			for item in self.bag:
				if item.type == "weapon":
					self.strength += item.attack
					break
		
		self.speed = speed
		self.level = level
		self.accuracy = accuracy
		self.name = name
		
		# -1 = Evil
		# 0 = Neutral
		# 1 = Good
		self.alignment = alignment
		self.description = description

class Item:

	# this is only a constructor
	# items are specified in the map tiles (Map-subclasses)

	class Weapon:

		def __init__(self, name, attack, durability, weight, description):

			self.type = "weapon"
			self.name = name
			self.attack = attack
			self.durability = durability
			self.durability_real = durability
			self.weight = weight
			self.description = description

		def use(self):
			self.durability_real -= 1

	class Potion:

		def __init__(self, name, pot_type, potency, weight, description):

			self.type = "potion"
			self.name = name
			self.type = pot_type
			self.potency = potency
			self.weight = weight
			self.description = description

	class Armor:

		def __init__(self, armor_type, name, armor, weight, durability, description):

			# equippable types:
			# head, chest pants, weapon

			self.type = armor_type
			self.name = name
			self.armor = armor
			self.weight = weight
			self.durability = durability
			self.durability_real = durability
			self.description = description

	class Empty:

		def __init__(self):

			self.type = "empty"
			self.name = "Empty"
			self.attack = 0
			self.armor = 0

class Map:

	def __init__(self, tile):
		self.tile = tile
		self.index = {
			(0,0) : self.Map00,
			(0,1) : self.Map01,
			(0,2) : self.Map02,
			(1,0) : self.Map10
		}
		self.current = self.index[self.tile]

	class Map00:

		commands = ["look", "move", "bag", "loot", "throw", "inspect","equip", "stats", "exit"]
		dagger = Item.Weapon("Goblin Dagger", 5, 15, 1, "A dagger made from a tiger's tooth.\nThe hilt is wrapped in leather.")
		goblin = NPC(0, 0, 0, 0, 2, 3,"goblin", [dagger], -1, "A dead goblin.\nHe's completely fried.")
		helmet = Item.Armor("head", "Frying Pan", 2, 1, 15, "It's a frying pan and a helmet!\nHow convenient.")
		npc_list = [goblin]
		items = [helmet]
		tile_searched = False
			

		@staticmethod
		def introtext():
			print("You are standing in the middle of the forest.")
			print("Here is where you woke up.")

		@staticmethod
		def look(direction):
			if direction == "north":
				print("As you peek through the tree trunks you")
				print("glimpse a vast empty land ahead of you")
				print("and a mountain far off in the distance.")
			elif direction == "east":
				print("Looking east, thanks to the sun rising,")
				print("you can make out a small little hut a couple")
				print("hundred meters ahead.")
			elif direction == "south":
				print("You smell something. Death?")
				print("As you gaze around your eyes fall on")
				print("the carcass of a goblin right behind a bush.")
				print("You always thought goblins were green,")
				print("but black as charcoal, its body looks like")
				print("it was struck by Zeus himself.")
				print("It's dead for a couple days already.")
			elif direction == "west":
				print("A big blueish metal structure is hiding between")
				print("the trees. Inspecting it closer you see that it")
				print("gives off a quiet humming sound.")
				print("something tells you that you shouldn't mess with it...")
			else:
				print("!! Invalid direction")

		@staticmethod
		def oob(direction):
			if direction == "south":
				print("You move through a couple dense bushes only to")
				print("find that a big blue shimmering cloth is hanging")
				print("right in the air. It gives off a silent hum.")
				print("Following it with your eyes you cannot see")
				print("something that looks like an end.")
				print("As you reach out to it a butterfly lands")
				print("on your index finger and then continues towards")
				print("the cloth. On impact the butterfly goes up in flames.")
			elif direction == "west":
				print("As you move westwards you approach a")
				print("big blue metal structure. The hum it")
				print("gives off slightly shakes the earth around you.")
				print("From each side of the structure hang blue")
				print("shimmering cloths. They float magically in the air.")
				print("looking around you cannot see how long they are.")
				print("But they stretch very far into the woods.")

			print("Since there is no way around the cloth,")
			print("you decide not to continue this way.")

	class Map01:
		commands = ["look", "move", "bag", "loot", "throw", "inspect", "equip", "stats", "exit"]
		#robe = Item.Armor("chest", "White Robe", 5, 1, 15, "A white robe.\nnot too white though.")
		#sword = Item.Weapon("Butterknife", 7, 20, 0.25, "A butterknife, handy.")
		#pants = Item.Armor("pants", "Kilt", 2, 0.75, 15,"A Kilt?\nHow did this get here?")
		#treasure_chest = NPC(10, 0, 0, 1, "treasure chest", [robe, sword, pants], 0, "a small treasure chest")
		items = []
		npc_list = []
		tile_searched = False

		@staticmethod
		def introtext():
			print("You are standing in the forest.")
			print("The sun is shining through the trees")
			print("to create patterns on the ground.")
			print("A light breeze rustles thorugh the leaves.")

		@staticmethod
		def look(direction):
			if direction == "north":
				print("You look out through the tree line")
				print("to catch a glimpse of the plains ahead.")
				print("It seems calm.")
			elif direction == "east":
				print("Peeking through the woods you can see a small hut.")
				print("Why would someone build a house here?")
				print("It seems to be made out of wood and looks relatively")
				print("You wonder who would live so deep in the forest.")
			elif direction == "south":
				print("You see a big blue cloth dancing in the air behind")
				print("some trees. Upon closer inspection you see three dead")
				print("goblins on the other side of the cloth.")
				print("They look like they burned to death.")
			elif direction == "west":
				print("Due to a change in elevation you can now look")
				print("down on the place where you woke up. You see a slight")
				print("blue shimmer flashing from the treetops.")
				print("It goes all the way through the woods.")
			else:
				print("!! Invalid direction")

		@staticmethod
		def oob(direction):
			print("You move toward the cloth and smell death.")
			print("Suddenly you stop, an intense heat is shooting")
			print("through your body. You step back, the pain alleviates.")
			print("Since there is no way around the cloth,")
			print("you decide not to continue this way.")

	class Map02:
		
		commands = ["look", "move", "bag", "loot", "throw", "inspect", "equip", "stats", "exit"]
		slingshot = Item.Weapon("Crude Slingshot", 2, 10, 1, "A crude slingshot made by a goblin.")
		goblin = NPC(10, 2, 2, 2, 2, 50, "goblin", [slingshot], -1, "A lone goblin.\nThey are usually in packs,\nthe others must have died.")
		#hut = NPC()
		items = []
		npc_list = [goblin]
		tile_searched = False

		@staticmethod
		def introtext_hostile():
			print("As you move toward the hut a stone flies")
			print("by your face. Looking for the source you find")
			print("a goblin with a slingshot hiding in the hut.")

		@staticmethod
		def introtext():
			print("You are at a hut in the woods.")

	class Map10:
		commands = ["look", "move", "bag", "loot", "throw", "inspect", "equip", "stats" "exit"]
		npc_list = []
		items = []
		tile_searched = False

class Player:

	def __init__(self, name):

		self.type = "player"
		self.hitpoints = 10
		self.manapoints = 0
		self.level = 1
		self.strength = 5
		self.accuracy = 65
		self.speed = 3
		self.name = name

		self.tile = [0,0]
		self.bag = [Item.Empty()]*6

		self.head = Item.Empty()
		self.chest = Item.Armor("chest","Tattered Shirt", 1, 0.5, 10, "A dirty old shirt.\nBetter than nothing?")
		self.pants = Item.Armor("pants", "Old Pants", 1, 0.5, 10, "Old pants made from linen.\nThey're dirty.")
		self.weapon = Item.Weapon("Broken Twig", 1, 1, 0.5, "A small twig you found on the floor")
		#self.weapon = Item.Empty()

		self.spells = []

	def getAttack(self):
		return self.strength + self.weapon.attack

	def getArmor(self):
		return self.head.armor + self.chest.armor + self.pants.armor


if __name__ == "__main__":
	main = Main()