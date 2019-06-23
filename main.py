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
		self.game_choice = ""

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

	def gameloop(self):


		def inspectprint(item):
			if item.type == "weapon":
				print("Name: {}\nType: {}\nAttack: {}\nDurability: {}/{}\nWeight: {}\n{}".format(item.name, item.type.capitalize(), item.attack, item.durability_real, item.durability, item.weight, item.description))
				return 1
			elif item.type == "potion":
				print("")
				return 1
			elif item.type == "npc":
				print(item.description)
				return 1
			elif item.type in ["head", "pants", "chest"]:
				print("Name: {}\nArmor Rating: {}\nWeight: {}\n{}".format(item.name, item.armor, item.weight, item.description))
				return 1
			elif item.type == "empty":
				print("Nothing")
				return 1
			else:
				return 0

		while True:
			
			if self.map.tile != self.tile:
				self.map.__init__(self.tile)
				self.map.current.introtext()

			self.equip_types = {
				"head": self.player.head,
				"chest": self.player.chest,
				"pants": self.player.pants,
				"weapon": self.player.weapon
			}

			self.game_choice = input("\n>:")
			self.game_choice = self.game_choice.split(" ")
			
			if self.game_choice[0] == "help":
				print(self.map.current.commands)
			
			elif self.game_choice[0] in ["0", "exit"]:
				break
			
			elif self.game_choice[0] in self.map.current.commands:
				
				if self.game_choice[0] == "look":
					try:
						self.map.current.look(self.game_choice[1])
					except IndexError:
						print("'look' requires an additional argument (north/east/south/west)")

				if self.game_choice[0] == "move":
					try:
						# cast to list to change values
						self.tile = list(self.tile)

						# (0/0) = (vertical/horizontal) - 0/0 at bottom left
						if self.game_choice[1] == "north":
							self.tile[0] += 1
						elif self.game_choice[1] == "east":
							self.tile[1] += 1
						elif self.game_choice[1] == "south":
							self.tile[0] -= 1
						elif self.game_choice[1] == "west":
							self.tile[1] -= 1
					
					except IndexError:
						print("'move' requires an additional argument (north/east/south/west)")
					
					finally:
						# always cast back to tuple
						self.tile = tuple(self.tile)
				
				elif self.game_choice[0] == "bag":
					print("Bag contents:")
					for item in self.player.bag:
						print("- ", item.name)

				elif self.game_choice[0] == "loot":

					try:
						if self.map.current.npc_list:
							for npc in self.map.current.npc_list:
								if " ".join(self.game_choice[1:]) == npc.name:
									print("you loot", npc.name, "and find:")
									if npc.bag:
										for item in npc.bag:
											
											try: # try except to check for single or multi items
											
												print(item.name)
												if input("Do you want to loot {} ?\n>:".format(item.name)).lower() in "yes":
													for player_item in self.player.bag:
														if player_item.name == "Empty":
															self.player.bag[self.player.bag.index(player_item)] = item
															npc.bag.pop(npc.bag.index(item))
															break
													else:
														print("your bag is full!")
														print("use 'throw' to throw away things from your bag")
											
											except AttributeError:

												for loot_obj in item:
													if input("Do you want to loot {} ?\n>:".format(loot_obj.name)).lower() in "yes":
														for player_item in self.player.bag:
															if player_item.name == "Empty":
																self.player.bag[self.player.bag.index(player_item)] = item
																npc.bag.pop(npc.bag.index(loot_obj))
																break
														else:
															print("your bag is full!")
															print("use 'throw' to throw away things from your bag")
									else:
										print("nothing to loot from", npc.name)

						if self.game_choice[1] == "tile":
							if not self.map.current.tile_searched:
								if self.map.current.items:
									for player_item in self.player.bag:
										if player_item.name == "Empty":
											self.tile_loot = random.choice(self.map.current.items)
											self.player.bag[self.player.bag.index(player_item)] = self.tile_loot
											print("you found {}".format(self.tile_loot.name))
											self.map.current.items.pop(self.player.bag.index(self.tile_loot))
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
						
						if (self.game_choice[1] not in [npc.name for npc in self.map.current.npc_list]) and (self.game_choice[1] != "tile"):
							print("no lootable object called", self.game_choice[1])

					except IndexError:
						print("'loot' requires an additional argument:")
						print("E.g.: loot (thing to loot or pick up)")

				elif self.game_choice[0] == "throw":
					try:
						for item in self.player.bag:
							if " ".join(self.game_choice[1:]) == item.name.lower():
								if item.name != "Empty":
									self.map.current.items.append(item)
									self.player.bag[self.player.bag.index(item)] = Item.Empty()
									break
						else:
							print("item '{}' not found in your bag".format(" ".join(self.game_choice[1:])))
					except IndexError:
						print("'throw' requires an additional argument:")
						print("check your bag for things to throw away")

				elif self.game_choice[0] == "inspect":
					try:
						for item in self.player.bag:
							if " ".join(self.game_choice[1:]) == item.name.lower():
								if inspectprint(item):
									break
						else:
							for item in self.map.current.items:
								if " ".join(self.game_choice[1:]) == item.name.lower():
									print("you pick up the", item.name, "from the ground\n")
									if inspectprint(item):
										print("\nuse 'loot' to put the item in your bag")
										break
							else:
								for npc in self.map.current.npc_list:
									if " ".join(self.game_choice[1:]) == npc.name.lower():
										if inspectprint(npc):
											break
								else:
									print("cannot inspect", " ".join(self.game_choice[1:]))
									print("no such item on tile")

					except IndexError:
						print("'inspect' requires and additional argument")

				elif self.game_choice[0] == "equip":

					try:
						for item in self.player.bag:
							if " ".join(self.game_choice[1:]).lower() == item.name.lower():

								try:
									if self.equip_types[item.type].type != "empty":
										for player_item in self.player.bag:
											if player_item.type == "empty":
												self.player.bag[self.player.bag.index(player_item)] = self.equip_types[item.type]
												if player_item.type == "head":
													self.player.head = player_item
												elif player_item.type == "chest":
													self.player.chest = player_item
												elif player_item.type == "pants":
													self.player.pants = player_item
												elif player_item.type == "weapon":
													self.player.weapon = player_item
												print(player_item.name, "equipped successfully")
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

				elif self.game_choice[0] == "stats":
					print("Name: {}\nLevel: {}\nHP: {}\nMP: {}\nStrength: {}".format(self.player.name, self.player.level, self.player.hitpoints, self.player.manapoints, self.player.strength))
					print("\nHead Armor:")
					inspectprint(self.player.head)
					print("\nChest Armor:")
					inspectprint(self.player.chest)
					print("\nLeg Armor:")
					inspectprint(self.player.pants)
					print("\nWeapon:")
					inspectprint(self.player.weapon)

			else:
				print("unknown command", self.game_choice[0])



class NPC:

	def __init__(self, hitpoints, manapoints, level, name, items, alignment, description):
		self.type = "npc"
		self.hitpoints = hitpoints
		self.manapoints = manapoints
		self.level = level
		self.name = name

		self.bag = []
		self.bag.append(items)
		
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

		def __init__(self, armor_type, name, armor, weight, description):

			self.type = armor_type
			self.name = name
			self.armor = armor
			self.weight = weight
			self.description = description

	class Empty:

		def __init__(self):

			self.type = "empty"
			self.name = "Empty"

class Map:

	def __init__(self, tile):
		self.tile = tile
		self.index = {
			(0,0) : self.Map00,
			(0,1) : self.Map01,
			(1,0) : self.Map10
		}
		self.current = self.index[self.tile]

	class Map00:

		commands = ["look", "move", "bag", "loot", "throw", "inspect","equip", "stats", "exit"]
		dagger = Item.Weapon("Goblin Dagger", 5, 15, 1, "A dagger made from a tiger's tooth.\nThe hilt is wrapped in leather.")
		goblin = NPC(0, 0, 2, "goblin", dagger, -1, "A dead goblin.\nHe's completely fried.")
		helmet = Item.Armor("head", "Frying Pan", 2, 1, "It's a frying pan and a helmet!\nHow convenient.")
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

	class Map01:
		commands = ["look", "move", "bag", "loot", "throw", "inspect", "equip", "stats", "exit"]
		robe = Item.Armor("chest", "white robe", 5, 1, "A white robe.\nnot too white though.")
		sword = Item.Weapon("Butterknife", 7, 20, 0.25, "A butterknife, handy.")
		treasure_chest = NPC(10, 0, 1, "treasure chest", [robe, sword], 0, "a small treasure chest")
		items = []
		npc_list = [treasure_chest]
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
				print("You look out though the tree line")
				print("to catch a glimpse of the plains ahead.")
				print("It seems calm.")
			elif direction == "east":
				print("")
				print("")
				print("")
			elif direction == "south":
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
			elif direction == "west":
				print("")
				print("")
				print("")
				print("")
			else:
				print("!! Invalid direction")

	class Map10:
		commands = ["look", "move", "bag", "loot", "throw", "inspect", "equip", "stats" "exit"]
		npc_list = []
		items = []
		tile_searched = False

class Player:

	def __init__(self, name):

		self.hitpoints = 10
		self.manapoints = 0
		self.level = 1
		self.strength = 5
		self.name = name

		self.tile = [0,0]
		self.bag = [Item.Empty()]*6

		self.head = Item.Empty()
		self.chest = Item.Armor("chest","Tattered Shirt", 1, 0.5, "A dirty old shirt.\nBetter than nothing?")
		self.pants = Item.Armor("pants", "Old Pants", 1, 0.5, "Old pants made from linen.\nThey're dirty.")
		self.weapon = Item.Empty()


if __name__ == "__main__":
	main = Main()