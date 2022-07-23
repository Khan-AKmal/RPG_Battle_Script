from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random 


#Create Black Magic
fire  = Spell("Fire", 25, 600, "black")
thunder  = Spell("Thunder", 25, 600, "black")
blizzard  = Spell("Blizzard", 25, 600, "black")
meteor  = Spell("Meteor", 40, 1200, "black")
quake  = Spell("Quake", 14, 140, "black")

#Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


#Creating Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully resotres party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

#Instantiate People
player1 = Person("Valos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Clare", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("John ", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp  ", 1250, 30, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 18200, 221, 525, 25, enemy_spells, [])
enemy3 = Person("Imp  ", 1250, 30, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "\nYOU HAVE BEEN AMBUSHED!" + bcolors.ENDC)

while running:
    print("============================")
    
    print("")
    print(bcolors.OKYELLOW + "NAME                 HP                                    MP" + bcolors.ENDC)
    for player in players: #Printing stats of all players
        player.get_stats()
        
    print(bcolors.BOLD + bcolors.OKYELLOW + "\n\nEnemies:" + bcolors.ENDC)
    
    for enemy in enemies:
        enemy.get_enemy_stats()
    
    for player in players:
        
        #Check if player wins
        starting_enemies = 3 
        defeated_enemies = 0
        
        for enemy in enemies:
            defeated_enemies += 1

        if starting_enemies - defeated_enemies == 3:
            print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
            running = False
            break


        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1
        
        if index == 0: #Attack action
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)                
            
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage")
            
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
            
        elif index == 1: #Magic action
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1
            
            if magic_choice == -1: #if entered value is 0
                continue
            
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            
            current_mp = player.get_mp()
            
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            
            player.reduce_mp(spell.cost)
            
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
            
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                
        elif index == 2: #Item action
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1 
            
            if item_choice == -1: #if entered value is 0
                continue
            
            item = player.items[item_choice]["item"]
            
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
                continue
            
            player.items[item_choice]["quantity"] -= 1
            
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                
                if item.name == "Mega Elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
            
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
            

    print("\n")
    #Enemy attack phase
    for enemy in enemies:
        if enemy.get_hp() == 0:
            continue
        
        #Check if enemies win
        starting_players = 3
        defeated_players = 0
        
        for player in players:
            defeated_players += 1
            
        if starting_players - defeated_players == 3:
            print(bcolors.FAIL + "The Enemies have defeated you!" + bcolors.ENDC) 
            running = False 
            break
                     
                      
        if defeated_players == 3:
            highRange = 3 # 3 players left
        elif defeated_players == 2:
            highRange = 2 # 2 players left
        elif defeated_players == 1:
            highRange = 1 # 1 player left
    
        enemy_choice = random.randrange(0, 2)
      
        if enemy_choice == 0: #Attack Action
            target = random.randrange(0,highRange)
            enemy_dmg = enemy.generate_damage()
            
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacked " + players[target].name.replace(" ", "") + " for", enemy_dmg, "points of damage.")

        elif enemy_choice == 1: #Magic Action
            spell, magic_dmg = enemy.choose_enemy_spell()
           
            if magic_dmg == 0:
                target = random.randrange(0,highRange)
                enemy_dmg = enemy.generate_damage()
            
                players[target].take_damage(enemy_dmg)
                print(enemy.name.replace(" ", "") + " attacked " + players[target].name.replace(" ", "") + " for", enemy_dmg, "points of damage.")
                
            elif spell.type == "white":
                enemy.reduce_mp(spell.cost)
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP" + bcolors.ENDC)
            
            elif spell.type == "black":
                enemy.reduce_mp(spell.cost)
                target = random.randrange(0,highRange)
            
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

        if players[target].get_hp() == 0:
            print(players[target].name.replace(" ", "") + " has died.")
            del players[target]
                    
