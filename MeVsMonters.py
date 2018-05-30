import sys
import os
import random
import pickle
import math
import platform

weapons = {
    "Great Sword": 40,
    "Axe": 45
}

system = platform.system()

class Player:
    def __init__(self, name):
        self.name = name
        self.maxHealth = 100
        self.health = self.maxHealth
        self.base_attack = 15
        self.level = 1
        self.experience = 0
        self.xpToUp = 1
        self.gold = 0
        self.pots = 1
        self.weapons = ["Rusty Sword"]
        self.currentWeapon = "Rusty Sword"

    @property
    def attack(self):
        attack = self.base_attack
        if self.currentWeapon == "Rusty Sword":
            attack += 5
        if self.currentWeapon == "Great Sword":
            attack += 15
        if self.currentWeapon == "Axe":
            attack += 20
        return attack

class Gobelin:
    def __init__(self, name):
        self.name = name
        self.maxHealth = 50
        self.health = self.maxHealth
        self.attack = 5
        self.goldGain = 10
GobelinIG = Gobelin("Gobelin")

class Troll:
    def __init__(self, name):
        self.name = name
        self.maxHealth = 100
        self.health = self.maxHealth
        self.attack = 4
        self.goldGain = 15
TrollIG = Troll("Troll")

class Orc:
    def __init__(self, name):
        self.name = name
        self.maxHealth = 70
        self.health = self.maxHealth
        self.attack = 7
        self.goldGain = 20    
OrcIG = Orc("Orc")

def main():
    clearConsole()
    print "Welcome to my game!\n"
    print "1.) Start"    
    print "2.) Load"    
    print "3.) Exit"    
    option = raw_input('-> ')
    if option == "1":
        initGame()
    elif option == "2":
        if os.path.exists("savefile") ==  True:
            clearConsole()
            with open("savefile", 'rb') as f:
                global PlayerIG
                PlayerIG = pickle.load(f)
            print "Loaded Save State..."
            option = raw_input(' ')
            start()
        else:
            print "You have no save for this game."
            option = raw_input(' ')
            main()
    elif option == "3":
        sys.exit()
    else:
        main()

def initGame():
    clearConsole()
    print "Hello, what is your name?"
    option = raw_input('-> ')
    global PlayerIG
    PlayerIG = Player(option)
    start()

def start():
    clearConsole()
    print "Name: %s" % PlayerIG.name
    print "Health: %i/%i" % (PlayerIG.health, PlayerIG.maxHealth)
    print "Level: %i (%i/%i)" % (PlayerIG.level, PlayerIG.experience, PlayerIG.xpToUp)
    print "Attack: %i" % PlayerIG.attack
    print "Current weapon: %s" % PlayerIG.currentWeapon
    print "Gold: %i" % PlayerIG.gold
    print "Potions: %i" % PlayerIG.pots
    print "1.) Fight"
    print "2.) Store"
    print "3.) Save"
    print "4.) Inventory"
    print "5.) Exit"
    option = raw_input('-> ')
    if option == '1':
        preFight()
    elif option == '2':
        store()
    elif option == '3':
        clearConsole()
        with open('savefile', 'wb') as f:
            pickle.dump(PlayerIG, f)
            print '\nGame has been saved!\n'
        option = raw_input(' ')
        start()
    elif option == '4':
        inventory()
    elif option == '5':
        sys.exit()
    else:
        start()

def inventory():
    clearConsole()
    print "What do you want to do?"
    print "1.) Equip weapon"
    print "b.) Go back"
    option = raw_input('-> ')
    if option ==  '1':
        equip()
    elif option == 'b':
        start()
    else:
        inventory()

def equip():
    clearConsole()
    print "What do you want to equip?"
    for weapon in PlayerIG.weapons:
        print weapon
    print "b to go back"
    option = raw_input('-> ')
    if option == PlayerIG.currentWeapon:
        print "You already have this weapon equipped"
        option = raw_input(' ')
        equip()
    elif option == 'b':
        inventory()
    elif option in PlayerIG.weapons:
        PlayerIG.currentWeapon = option
        print "You have equiped %s" % option
        option = raw_input(' ')
        equip()
    else:
        print "You don't have %s in your inventory" % option

def preFight():
    global enemy
    enemyNum = random.randint(1, 3)
    if enemyNum == 1:
        enemy = GobelinIG
    elif enemyNum == 2:
        enemy = TrollIG
    else:
        enemy = OrcIG
    fight()

def fight():
    clearConsole()
    print "%s     vs     %s" % (PlayerIG.name, enemy.name)
    print "%s's Health: %i/%i     %s's Health: %i/%i" % (PlayerIG.name, PlayerIG.health, PlayerIG.maxHealth, enemy.name, enemy.health, enemy.maxHealth)
    print "Potions: %i" % PlayerIG.pots
    print "1.) Attack"    
    print "2.) Drink Potion"
    print "3.) Run"
    option = raw_input('-> ')
    if option == '1':
        attack()
    elif option == '2':
        drinkPot()
    elif option == '3':
        run()
    else:
        fight()

def attack():
    clearConsole()
    PlayerAttackAction()
    clearConsole()
    EnemyAttackAction()

def PlayerAttackAction():
    PAttack = getRandomAttack(PlayerIG)
    if PAttack == PlayerIG.attack / 2:
        print "You missed!"
    else:
        enemy.health -= PAttack
        print "You deal %i damage!" % PAttack
    option = raw_input(' ')
    if enemy.health <= 0:
        win()

def EnemyAttackAction():
    EAttack = getRandomAttack(enemy)
    if EAttack == enemy.attack / 2:
        print "The enemy missed!"
    else:
        PlayerIG.health -= EAttack
        print "The enemy deals %i damage!" % EAttack
    option = raw_input(' ')
    if PlayerIG.health <= 0:
        die()
    else:
        fight()

def drinkPot():
    clearConsole()
    if PlayerIG.pots == 0:
        print "You don't have any potions!"
    else:
        PlayerIG.health += 30
        PlayerIG.pots -= 1
        if PlayerIG.health > PlayerIG.maxHealth:
            PlayerIG.health = PlayerIG.maxHealth 
        print "You drank a potion!"
    option = raw_input(' ')
    fight()

def run():
    clearConsole()
    runNum = random.randint(1, 3)
    if runNum == 3:
        print "You have successfully ran away!"
        option = raw_input(' ')
        start()
    else:
        print "You failed to get away"
        option = raw_input(' ')
        clearConsole()
        EnemyAttackAction()
        option = raw_input(' ')

def win():
    clearConsole()
    PlayerIG.gold += enemy.goldGain
    experience = math.fabs(enemy.attack/3)
    PlayerIG.experience += experience
    enemy.health = enemy.maxHealth
    print "You have defeated the %s!" % enemy.name
    print "You found %i golds!" % enemy.goldGain
    print "You earned %i XP" % experience
    if PlayerIG.experience >= PlayerIG.xpToUp:
        PlayerIG.level += 1
        PlayerIG.experience = PlayerIG.experience - PlayerIG.xpToUp
        PlayerIG.xpToUp = math.fabs(math.pow(PlayerIG.level, 3/2))
        print "You up to level %i" % PlayerIG.level
    option = raw_input(' ')
    start()

def die():
    clearConsole()
    print "You have died"
    option = raw_input(' ')
    main()

def store():
    clearConsole()
    print "Welcome to the shop!"
    print "\nWhat whould you like to buy?\n"
    print "1.) Great Sword"
    print "2.) Potion"
    print "b to go back"
    print " "
    option = raw_input('Type the name of the weapon (or "back") -> ')

    if option in weapons:
        if PlayerIG.gold >= weapons[option]:
            clearConsole()
            PlayerIG.gold -= weapons[option]
            PlayerIG.weapons.append(option)
            print "You have bought %s" % option
        else:
            clearConsole()
            print "You don't have enough gold"
        option = raw_input(' ')
        store()
    elif option == 'potion':
        if PlayerIG.gold >= 15:
            clearConsole()
            PlayerIG.pots += 1
            print "You have bought %s" % option
        else:
            clearConsole()
            print "You don't have enough gold"
        option = raw_input(' ')
        store()
    elif option == 'b':
        start()
    else:
        clearConsole()
        print "That item does not exist"
        option = raw_input(' ')
        store()


# Util methods
def getRandomAttack(entity):
    return random.randint(entity.attack / 2, entity.attack)

def clearConsole():
    if (system == 'Linux' or system == 'Darwin'):
        os.system('clear')
    elif system == 'Windows':
        os.system('cls')

main()
