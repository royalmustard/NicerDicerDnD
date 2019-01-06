import Dice
import sys, csv, json, random


def Money(tier):
    pRoll = Dice.D(100)
    if tier != "t1" and tier != "t2" and tier !="t3" and tier != "t4":
        return "Tier not recognised! Please try again."
    elif tier == "t1":
        if pRoll >= 1 and pRoll <= 30:
            return str(Dice.D(6,5))+"CP"
        elif pRoll >= 31 and pRoll <= 60:
            return str(Dice.D(6,4))+"SP"
        elif pRoll >= 61 and pRoll <= 70:
            return str(Dice.D(6,3))*10+"SP"
        elif pRoll >= 71 and pRoll <= 95:
            return str(Dice.D(6,3))+"GP"
        else:
            return str(Dice.D(6))+"PP"
    elif tier == "t2":
        return tier+" not yet implemented"
    elif tier == "t3":
        return tier+" not yet implemented"
    elif tier == "t4":
        return tier+" not yet implemented"

def MagicItem(table):
        itemTableFile = open(table, newline="")
        reader = csv.reader(itemTableFile, delimiter=";")
        itemTable = {rows[0]:rows[1] for rows in reader}
        previous = 0
        roll = Dice.D(100)
        for key in itemTable:
            if roll in range(previous, int(key)):
                print(itemTable.get(key))
                if "Spell scroll" in itemTable.get(key):
                    scroll = itemTable.get(key).split(" ")
                    scroll = scroll[2].strip("()")
                    SpellScroll(scroll)
                break
            else:
                previous = int(key)
        itemTableFile.close()

def SpellScroll(level):
    with open("Tables/"+level+".json") as spellFile:
        spells = json.load(spellFile)
        print(random.choice(spells))
    spellFile.close()

def Hoard(tier):
    return

def Booty(type, value):
	with open("Tables/Booty.json") as bfile:
		bty = json.load(bfile)
		if type in bty and value in bty[type]:
			print(str(value)+"G|"+random.choice(bty[type][value]))
        else:
            print("Not found")

while True:
    inputs = input()
    command = inputs.split()
    command = [x.lower() for x in command]
    if command[0] == "exit":
        sys.exit()
    elif command[0] == "money" and len(command) == 2:
        print(Money(command[1]))
    elif command[0] == "mitem" and len(command) == 2:
        MagicItem("Tables/"+command[1].upper()+".csv")
    elif command[0] == "scroll" and len(command) == 2:
        SpellScroll(command[1])
    elif command[0] == "booty" and len(command) == 3:
        Booty(command[1], command[2])
    else:
        print("Sorry, but I can't let you do this, Dave.")
