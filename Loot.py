import Dice, Prob
import sys, csv, json, random, string, os


def printHelp():
    print("Valid commands are:")
    print("- mitem [Letter of Magic Item Table] | Chooses a random magic item from given table")
    print("- scroll [level] | Chooses a random spell of the given level")
    print("- money [party tier] | Gives a random amount of money fit to the party tier. Valid parameters are {t1, t2, t3, t4}. Consult the DMG to see which tier is best used")
    print("- booty [gem/art] [value in gp] | Chooses a random gem or art item of given value")
    print("- prob [ac] [bonus] [a/d/n] | probability to hit ac with bonus and adv/disadv/normal throw")


def money(tier):
    pRoll = Dice.D(100)
    if tier not in ["t1", "t2", "t3", "t4"]:
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
        if 1 <= pRoll <= 20:
            return f"{Dice.D(6, 4)*100}SP + {Dice.D(6)*100}GP"
        elif 21 <= pRoll <= 35:
            return f"{Dice.D(6)*100}EP + {Dice.D(6)*100}GP"
        elif 36 <= pRoll <= 75:
            return f"{Dice.D(6, 2)*100}GP + {Dice.D(6)*10}PP"
        else:
            return f"{Dice.D(6, 2)*100}GP + {Dice.D(6, 2)*10}PP"
    elif tier == "t4":
        if 1 <= pRoll <= 15:
            return f"{Dice.D(6, 2) * 1000}EP + {Dice.D(6, 8) * 100}GP"
        elif 16 <= pRoll <= 55:
            return f"{Dice.D(6) * 1000}GP + {Dice.D(6) * 100}PP"
        else:
            return f"{Dice.D(6) * 1000}GP + {Dice.D(6, 2) * 100}PP"

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
    if tier not in ["t1", "t2", "t3", "t4"]:
        print("Invalid tier!")
        return
    if tier == "t1":
        print(f"{Dice.D(6, 6)*100}CP + {Dice.D(6, 3)*100}SP + {Dice.D(6, 2)*10}GP")
        hoard_table("h1")


def hoard_table(table):
    if table not in ["h1", "h2", "h3", "h4"]:
        print("Invalid hoard table!")
        return
    with open("Tables/"+table+".csv") as tf:
        reader = csv.reader(tf)
        pRoll = Dice.D(100)
        for row in reader:
            if int(row[0]) <= pRoll <= int(row[1]):
                if len(row) < 3:
                    print("No items for you. Better luck next time!")
                    return
                elif len(row) >= 5:
                    if "d" in row[2]:
                        rd = row[2].split("d")
                        for _ in range(Dice.D(int(rd[1]), int(rd[0]))):
                            booty(row[4], row[3])
                    else:
                        for _ in range(int(row[2])):
                            booty(row[4], row[3])
                if len(row) == 7:
                    if "d" in row[5]:
                        rd = row[5].split("d")
                        for _ in range(Dice.D(int(rd[1]), int(rd[0]))):
                            magicItem(row[6])
                    else:
                        for _ in range(int(row[5])):
                            magicItem(row[6])



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
    try:
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
        elif command[0] == "prob" and len(command) == 4:
            Prob.hitChance(int(command[1]), int(command[2]), command[3])
        elif command[0] == "clear":
            os.system("cls" if os.name == "nt" else "clear")
        elif command[0] == "hoard" and len(command) == 2:
            hoard(command[1])
        else:
            print("Unknown command or incorrect usage. Pleas type help for more info")
    except Exception:
        print("Something went wrong! Very, very wrong!")