import Dice
import sys, csv, json, random, string


def printHelp():
    print("Valid commands are:")
    print("- mitem [Letter of Magic Item Table] | Chooses a random magic item from given table")
    print("- scroll [level] | Chooses a random spell of the given level")
    print("- money [party tier] | Gives a random amount of money fit to the party tier. Valid parameters are {t1, t2, t3, t4}. Consult the DMG to see which tier is best used")
    print("- booty [gem/art] [value in gp] | Chooses a random gem or art item of given value")


def money(tier):
    pRoll = Dice.D(100)
    if tier != "t1" and tier != "t2" and tier != "t3" and tier != "t4":
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
        if 1 <= pRoll <= 30:
            return str(Dice.D(6,7))+"GP"
        elif 31 <= pRoll <= 60:
            return str(Dice.D(6,6)+Dice.D(6,2)*10)+"GP"
        elif 61 <= pRoll <= 70:
            return str(Dice.D(6, 3) + Dice.D(6, 2) * 10) + "GP"
        elif 71 <= pRoll <= 95:
            return str(Dice.D(6,4)*10)+"GP"
        else:
            return str(Dice.D(6,5))+"GP"
    elif tier == "t3":
        return tier+" not yet implemented"
    elif tier == "t4":
        return tier+" not yet implemented"


def magicItem(table):
    if table not in list(string.ascii_uppercase)[:8]:
        print("Invalid Table!")
        return
    table = "Tables/"+table+".csv"
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
                spellScroll(scroll)
            break
        else:
            previous = int(key)


def spellScroll(level):
    with open("Tables/"+level+".json") as spellFile:
        spells = json.load(spellFile)
        print(random.choice(spells))


def hoard(tier):
    return


def booty(type, value):
    with open("Tables/Booty.json") as bfile:
        bty = json.load(bfile)
        if type in bty and value in bty[type]:
            print(str(value)+"G|"+random.choice(bty[type][value]))
        else:
            print("Valid values are:")
            print("gem [10, 50, 100, 500, 1000, 5000]")
            print("art [25, 250, 750, 2500, 7500")


while True:
    print("LootConsole > ", end="")
    inputs = input()
    command = inputs.split()
    command = [x.lower() for x in command]
    if command[0] == "exit":
        sys.exit()
    elif command[0] == "money" and len(command) == 2:
        print(money(command[1]))
    elif command[0] == "mitem" and len(command) == 2:
        magicItem(command[1].upper())
    elif command[0] == "scroll" and len(command) == 2:
        spellScroll(command[1])
    elif command[0] == "booty" and len(command) == 3:
        booty(command[1], command[2])
    elif command[0] == "help":
        printHelp()
    else:
        print("Unknown command or incorrect usage. Pleas type help for more info")
