import Dice
import sys, csv, json, random


def printHelp():
    print("- Valid commands are:")
    print("- mitem [Letter of Magic Item Table] | Chooses a random magic item from given table")
    print("- scroll [level] | Chooses a random spell of the given level")
    print("- money [party tier] | Gives a random amount of money fit to the party tier. Valid parameters are {t1, t2, t3, t4}. Consult the DMG to see which tier is best used")
    print("- booty [gem/art] [value in gp] | Chooses a random gem or art item of given value")



def Money(tier):
    pRoll = Dice.D(100)
    if tier != "t1" and tier != "t2" and tier !="t3" and tier != "t4":
        return "Tier not recognised! Please try again."
    elif tier == "t1":
        if 1 <= pRoll <= 30:
            return str(Dice.D(6,5))+"CP"
        elif 31 <= pRoll <= 60:
            return str(Dice.D(6,4))+"SP"
        elif 61 <= pRoll <= 70:
            return str(Dice.D(6,3))*10+"SP"
        elif 71 <= pRoll <= 95:
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
                #else:
                   # print("Valid values are:")
                   # print("gem [10, 50, 100, 500, 1000, 5000]")
                   # print("art [25, 250, 750, 2500, 7500")

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
    elif command[0] == "help":
        printHelp()
    else:
        print("Unknown command or incorrect usage. Pleas type help for more info")
