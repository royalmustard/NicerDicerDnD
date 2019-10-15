def hitChance(ac, bonus=0, state="n"):
    if state not in ["n", "a", "d"]:
        print("Please enter valid state!")
        return
    pr = (20+bonus-ac)/20
    chance = 0
    if state == "n":
        chance = pr
    elif state == "a":
        chance = 2*pr-pr**2
    else:
        chance = pr**2
    print("Hit chance: "+str(round(chance*100, 1))+"%")
    print("Mu: "+str(10.5+bonus))

