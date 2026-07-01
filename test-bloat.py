from app.GameDefinitions.Loadouts import LoadoutRegistry

oath_torva_rancour = LoadoutRegistry.get("OathTorvaRancour")
from app.GameDefinitions.Loadouts import LoadoutRegistry

oath_torva_salve = LoadoutRegistry.get("OathTorvaSalve")
from app.GameDefinitions.Monsters.Bloat import Bloat
from app.GameDefinitions.Monsters.Sotetseg import Sotetseg
from app.Player import Player
from app.GameDefinitions.Weapons.Bgs import Bgs
from app.GameDefinitions.Weapons.CrystalHalberd import CrystalHalberd
from app.GameDefinitions.Weapons.DragonClaws import DragonClaws
from app.GameDefinitions.Weapons.Fists import Fists
from app.GameDefinitions.Weapons.NoxHally import NoxHally
from app.GameDefinitions.Weapons.Scythe import Scythe

number_of_tests = 10000
number_of_players = 3


print(f"Sample Size: {number_of_tests}")
print(f"Scale: {number_of_players}")


scythe = Scythe()
nox = NoxHally()
fists = Fists()
bgs = Bgs()
dragon_claws = DragonClaws()
chally = CrystalHalberd()



player = oath_torva_salve
bloat = Bloat(number_of_players)

player.equip_weapon(nox)



tests = [
    {
        "Bgs": 0,
        "Chally": 2,
        "Nox": 7,
        "Claws": 1
    },
    {
        "Bgs": 0,
        "Chally": 2,
        "Nox": 8,
        "Claws": 1
    },
    {
        "Bgs": 0,
        "Chally": 2,
        "Nox": 9,
        "Claws": 1
    },
    {
        "Bgs": 0,
        "Chally": 2,
        "Nox": 10,
        "Claws": 1
    },
    {
        "Bgs": 0,
        "Chally": 2,
        "Nox": 11,
        "Claws": 1
    },
    {
        "Bgs": 1,
        "Chally": 2,
        "Nox": 9,
        "Claws": 1
    },
    {
        "Bgs": 1,
        "Chally": 2,
        "Nox": 10,
        "Claws": 1
    },
        {
        "Bgs": 1,
        "Chally": 2,
        "Nox": 11,
        "Claws": 1
    },
    ]


for test in tests:
    bgs_swings = test["Bgs"]
    chally_swings = test["Chally"]
    claws_swings = test["Claws"]
    nox_swings = test["Nox"]

    resultdata = []
    health_result_data = []



    print("---------------------------------------")
    print(f"BGS:\t {bgs_swings}")
    print(f"Chally:\t {chally_swings}")
    print(f"Claw:\t {claws_swings}")
    print(f"Nox:\t {nox_swings}")

    for i in range(0,number_of_tests):
        bloat = Bloat(number_of_players)

        player.equip_weapon(bgs)
        for i in range(0, number_of_players * bgs_swings):
            hit = player.do_attack(bloat, special_attack=True)
            bloat.reduce_hp(hit)
            player.current_special_attack = 100



        player.equip_weapon(chally)
        for i in range(0, number_of_players * chally_swings):
            hit = player.do_attack(bloat, special_attack=True)
            bloat.reduce_hp(hit)
            player.current_special_attack = 100


        player.equip_weapon(nox)
        for i in range(0, number_of_players * nox_swings):
            hit = player.do_attack(bloat)
            bloat.reduce_hp(hit)


        player.equip_weapon(dragon_claws)
        for i in range(0, number_of_players * claws_swings):
            hit = player.do_attack(bloat, special_attack=True)
            bloat.reduce_hp(hit)
            player.current_special_attack = 100

        if(bloat.is_dead()):
            resultdata.append(1)
        else:
            resultdata.append(0)
            health_result_data.append(bloat.current_hp)


    sum = 0
    alive_sum = 0
    dead_sum = 0
    for result in resultdata:
        sum += result

        if result == 1: alive_sum += 1
        if result == 0: dead_sum += 1

    healthsum = 0
    for result in health_result_data:
        healthsum+= result

    chance = sum/len(resultdata)
    avg_alive_health = healthsum/len(health_result_data)
    print(f"Chance to 2 down bloat: {round(round(chance,4)*100,2)}% {alive_sum} kills, {dead_sum} wipes")
    print(f"When Bloat survived, on average he had {round(avg_alive_health)} health")
    print()













# player_salve = Player(stats=input_stats, weapon=scythe, wearing_salve=True)
# print(f"Player attack roll (w/ salve): {player_salve.calc_att_roll()}")
