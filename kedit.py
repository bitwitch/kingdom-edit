import argparse
import copy
import json
import sys
import uuid

archer_template = { "name": "Archer P1 [B]", "parentObject": { "linkedObjectID": "" }, "hierarchyPath": "Level/GameLayer/", "prefabPath": "Prefabs/Characters/Archer", "uniqueID": "Archer P1 [B]--6969", "mode": 0, "createOrder": 12345, "linkOrder": 0, "decayHint": 0, "decayResistanceDays": 2, "decayedVersionPrefabPath": "Prefabs/Characters/Peasant", "netID": 1666, "crpcType": 1, "localPosition": { "x": 120.98619079589844, "y": 0.8799997568130493, "z": 0.7556657791137695 }, "localScale": { "x": -1.0, "y": 1.0, "z": 1.0 }, "componentData2": [ { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":0,\"gems\":0,\"usesCurrencySystem\":true,\"currency\":{\"Coins\":1,\"Gems\":0,\"Crown\":0,\"Skulls\":0,\"Shades\":0,\"Merchandise\":0}}" }, { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" }, { "name": "Archer", "type": "ArcherData", "data": "{\"tower\":{\"linkedObjectID\":\"\"},\"knight\":{\"linkedObjectID\":\"\"},\"guardSide\":1,\"guardDepth\":0,\"desiredAttackMode\":0,\"despawnOnLoad\":false}" }, { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":0,\"invulnerable\":false}" }, { "name": "GenderAnimatorSelector", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":false}" }, { "name": "Petrifiable", "type": "PetrifiableSaveData", "data": "{\"RemainingHP\":0,\"IsPetrified\":false,\"RemainingDuration\":-106.38296508789063}" }, { "name": "Embarkee", "type": "EmbarkeeSaveData", "data": "{\"IsEmbarked\":false,\"SlotId\":-1,\"Embarkable\":{\"linkedObjectID\":\"\"}}" } ] }

worker_template = { "name": "Worker P1 [A]", "parentObject": { "linkedObjectID": "" }, "hierarchyPath": "Level/GameLayer/", "prefabPath": "Prefabs/Characters/Worker", "uniqueID": "Worker P1 [A]--6969", "mode": 0, "createOrder": 22222, "linkOrder": 0, "decayHint": 4, "decayResistanceDays": 1, "decayedVersionPrefabPath": "Prefabs/Characters/Peasant", "netID": 1098, "crpcType": 1, "localPosition": { "x": 127.18162536621094, "y": 0.875, "z": 0.5052622556686401 }, "localScale": { "x": -1.0, "y": 1.0, "z": 1.0 }, "componentData2": [ { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":0,\"gems\":0,\"usesCurrencySystem\":true,\"currency\":{\"Coins\":1,\"Gems\":0,\"Crown\":0,\"Skulls\":0,\"Shades\":0,\"Merchandise\":0}}" }, { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" }, { "name": "Worker", "type": "WorkerData", "data": "{\"despawnOnLoad\":false}" }, { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":0,\"invulnerable\":false}" }, { "name": "GenderAnimatorSelector", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":false}" }, { "name": "Petrifiable", "type": "PetrifiableSaveData", "data": "{\"RemainingHP\":0,\"IsPetrified\":false,\"RemainingDuration\":-106.38296508789063}" }, { "name": "Embarkee", "type": "EmbarkeeSaveData", "data": "{\"IsEmbarked\":false,\"SlotId\":-1,\"Embarkable\":{\"linkedObjectID\":\"\"}}" } ] }

pikeman_template = { "name": "Pikeman P1 [8]", "parentObject": { "linkedObjectID": "" }, "hierarchyPath": "Level/GameLayer/", "prefabPath": "Prefabs/Characters/Pikeman", "uniqueID": "Pikeman P1 [8]--59924", "mode": 0, "createOrder": 20668, "linkOrder": 0, "decayHint": 32, "decayResistanceDays": 2, "decayedVersionPrefabPath": "Prefabs/Characters/Peasant", "netID": 1101, "crpcType": 1, "localPosition": { "x": -7.411938667297363, "y": 0.8804292678833008, "z": 0.9069020748138428 }, "localScale": { "x": -1.0, "y": 1.0, "z": 1.0 }, "componentData2": [ { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":0,\"gems\":0,\"usesCurrencySystem\":true,\"currency\":{\"Coins\":3,\"Gems\":0,\"Crown\":0,\"Skulls\":0,\"Shades\":0,\"Merchandise\":0}}" }, { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" }, { "name": "Pikeman", "type": "PikemanData", "data": "{\"fishingSide\":-1,\"assignedSide\":-1,\"assignedWall\":{\"linkedObjectID\":\"\"},\"assignedReadiness\":0,\"remainingPikeUses\":30,\"summonedToBoat\":false}" }, { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":1,\"invulnerable\":false}" }, { "name": "GenderAnimatorSelector", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":true}" }, { "name": "Petrifiable", "type": "PetrifiableSaveData", "data": "{\"RemainingHP\":0,\"IsPetrified\":false,\"RemainingDuration\":-26.941898345947267}" }, { "name": "Embarkee", "type": "EmbarkeeSaveData", "data": "{\"IsEmbarked\":false,\"SlotId\":-1,\"Embarkable\":{\"linkedObjectID\":\"\"}}" } ] }

enemy_kinds = [ "GreedArcher", "GreedKnight", "CrownStealer", "Troll", "Squid", "Boss" ]

max_castle_level = 6
max_wall_level = 4

_next_net_id = 3000
def next_net_id():
    global _next_net_id
    prev = _next_net_id
    _next_net_id += 1
    return prev

_create_order = 30000
def next_create_order():
    global _create_order 
    prev = _create_order
    _create_order += 1
    return prev

def make_archer(name, x=0):
    archer = copy.deepcopy(archer_template)
    archer["name"] = name
    archer["uniqueID"] = str(uuid.uuid1())
    archer["localPosition"]["x"] = x
    archer["netID"] = next_net_id()
    archer["createOrder"] = next_create_order()
    return archer

def make_worker(name, x=0):
    worker = copy.deepcopy(worker_template)
    worker["name"] = name
    worker["uniqueID"] = str(uuid.uuid1())
    worker["localPosition"]["x"] = x
    worker["netID"] = next_net_id()
    worker["createOrder"] = next_create_order()
    return worker

def make_pikeman(name, x=0):
    pikeman = copy.deepcopy(pikeman_template)
    pikeman["name"] = name
    pikeman["uniqueID"] = str(uuid.uuid1())
    pikeman["localPosition"]["x"] = x
    pikeman["netID"] = next_net_id()
    pikeman["createOrder"] = next_create_order()
    return pikeman

def init_shop(shop_kind, objects):
    identifier = None
    if shop_kind == "bow":
        identifier = "ShopBow"
    elif shop_kind == "hammer":
        identifier = "ShopHammer"
    elif shop_kind == "scythe":
        identifier = "ShopScythe"
    else:
        assert 0, f"init_shop: unknown shop_kind: {shop_kind}"

    shop = obj_by_name_contains(objects, f"{identifier} Placeholder")
    if shop != None:
        net_id = next_net_id()
        shop["name"] = f"{identifier}_greece(Clone)"
        shop["uniqueID"] = str(uuid.uuid1())
        shop["prefabPath"] = f"Prefabs/Buildings and Interactive/greece/{identifier}_greece"
        shop["netID"] = net_id
        # shop["crpcType"] = 2
        # shop["componentData2"] = [ { "name": "PayableShop", "type": "PayableShopData", "data": "{\"items\":[]}" }, { "name": "WorkableBuilding", "type": "WorkableBuildingData", "data": "{\"currentBuildPoints\":0.0,\"usesConstructionBuildingComponent\":true}" }, { "name": "CRPCStamp", "type": "CRPCSaveData", "data": f'{{"NetID":{net_id},"SemiStatic":true}}' }, { "name": "ConstructionBuildingComponent", "type": "ConstructionBuildingComponentSaveData", "data": "{\"CurrentBuildPoints\":4.0}" }, { "name": "PersistentRouter", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":false}" } ]

        print(f"initializing {shop_kind} shop")
    else:
        print(f"no placeholder {shop_kind} shop found")


def upgrade_castle(obj, level):
    global max_castle_level
    level = min(level, max_castle_level)
    obj["name"] = f"Castle{level}_greece(Clone)"
    obj["uniqueID"] = str(uuid.uuid1())
    obj["prefabPath"] = f"Prefabs/Buildings and Interactive/greece/Castle{level}_greece"
    if not obj_has_component(obj, "Castle"):
        obj["componentData2"].append({"name":"Castle","type":"CastleData","data":"{}"})
    if not obj_has_component(obj, "GhostHintTrigger"):
        obj["componentData2"].append({"name":"GhostHintTrigger","type":"GhostHintTriggerData","data":"{\"IsGhostHintEnabled\":true,\"hintDataPath\":\"UpgradeTheCastle1\"}"})

def upgrade_walls(objects, level):
    global max_wall_level
    level = min(level, max_wall_level)
    for obj in objects:
        if "Wall0" in obj["name"]:
            obj["name"] = f"Wall{level}_greece(Clone)"
            obj["uniqueID"] = str(uuid.uuid1())
            obj["prefabPath"] = f"Prefabs/Buildings and Interactive/greece/Wall{level}_greece"
            obj["decayedVersionPrefabPath"] = f"Prefabs/Buildings and Interactive/greece/Wall{level} Wreck_greece"
            # make two workers to build each wall
            for i in range(2):
                worker = make_worker("pimp my walls worker", x=obj["localPosition"]["x"])
                objects.append(worker)

def mark_trees(objects):
    for obj in objects:
        if obj_has_component(obj, "WorkableTree"):
            mark_tree(obj)

def player_set_formation_active(obj, val):
    for comp in obj["componentData2"]:
        if comp["name"] == "Player":
            data = json.loads(comp["data"])
            data["isFormationActive"] = val
            comp["data"] = json.dumps(data)

def obj_set_crpc_stamp_net_id(obj, val):
    for comp in obj["componentData2"]:
        if comp["name"] == "CRPCStamp":
            data = json.loads(comp["data"])
            data["NetID"] = val
            comp["data"] = json.dumps(data)

def obj_set_hp(obj, val):
    for comp in obj["componentData2"]:
        if comp["name"] == "Damageable":
            data = json.loads(comp["data"])
            data["hitPoints"] = val
            comp["data"] = json.dumps(data)

def obj_set_coins(obj, val):
    for comp in obj["componentData2"]:
        if comp["name"] == "Wallet":
            data = json.loads(comp["data"])
            data["usesCurrencySystem"] = True
            data["currency"]["Coins"] = val
            comp["data"] = json.dumps(data)

def mark_tree(obj):
    for comp in obj["componentData2"]:
        if comp["name"] == "WorkableTree":
            data = json.loads(comp["data"])
            data["marked"] = True
            comp["data"] = json.dumps(data)

def obj_has_component(obj, comp_name):
    for comp in obj["componentData2"]:
        if comp["name"] == comp_name:
            return True
    return False

def find_all_with_component(objects, comp_name):
    results = []
    for obj in objects:
        if obj_has_component(obj, comp_name):
            results.append(obj)
    return results

def obj_by_name(objects, name):
    for obj in objects:
        if obj["name"] == name:
            return obj
    return None

def obj_by_name_contains(objects, substr):
    for obj in objects:
        if substr in obj["name"]:
            return obj
    return None

def parse_json_file(filepath):
    with open(filepath, "r") as f:
        doc = json.load(f)
    return doc

# for use in python interpreter for easily playing around
def get_island_data(filepath, island):
    doc = parse_json_file(filepath)
    campaign_index = 0
    return doc["campaigns"][campaign_index]["_islands"][island]


def print_objs_between(objects, a, b):
    ignore = ["Grass", "Tree", "Shrub", "Snow", "Cloud", "Moss", "OracleHintText"]
    for obj in objects:
        x = obj["localPosition"]["x"] 
        if x >= a and x <= b:
            skip = False
            for s in ignore:
                if s in obj["name"]:
                    skip = True
            if not skip:
                print(f'{obj["name"]} at x={x}')



# remove all non trigger portals, move to trigger portal with archer, worker, and idol
def action_take_over(doc, island):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    portal_x = 0
    new_objects = []

    for obj in objects:
        if obj_has_component(obj, "Portal"):
            if obj_has_component(obj, "QuestTransitionTrigger"):
                obj_set_hp(obj, 1)
                portal_x = obj["localPosition"]["x"]
                new_objects.append(obj)
        else:
            new_objects.append(obj)

    print(f"After taking over there are {len(new_objects)} objects")

    campaign["currentReign"]["landData"][island]["portals"] = 1

    # set player position and activate formation
    target_x = portal_x - 3 if portal_x > 0 else portal_x + 3
    player1 = obj_by_name(objects, "Player 1")
    player1["localPosition"]["x"] = target_x
    player_set_formation_active(player1, True)
    obj_set_coins(player1, 69)

    # set squad position to portal position
    idol = obj_by_name_contains(objects, "Idol")
    if idol:
        idol["localPosition"]["x"] = portal_x
    else:
        print(f"warning: no idol found on island {island}")

    archer = make_archer("Steve", x=target_x)
    new_objects.append(archer)
    worker = make_worker("Joey", x=target_x)
    new_objects.append(worker)

    land["objects"] = new_objects
    
    outfile = f"takeover_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")


# destroy all portals
def action_destroy(doc, island):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    new_objects = [obj for obj in objects if not obj_has_component(obj, "Portal")]

    campaign["currentReign"]["landData"][island]["portals"] = 0
    land["objects"] = new_objects

    print(f"After destroying there are {len(new_objects)} objects")
    
    outfile = f"destroy_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")


# kill all enemies
def action_exterminate(doc, island):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    new_objects = []

    for obj in objects:
        keep = True
        for kind in enemy_kinds:
            if obj_has_component(obj, kind):
                keep = False
                break
        if keep:
            new_objects.append(obj)

    land["objects"] = new_objects

    print(f"After extermination there are {len(new_objects)} objects")
    
    outfile = f"exterminate_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")


# teleport to a position with a squad for battle
def action_formation(doc, island, x):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    player1 = obj_by_name(objects, "Player 1")
    player1["localPosition"]["x"] = x
    player_set_formation_active(player1, True)

    for i in range(5):
        objects.append(make_archer(f"Formation Archer {i}", x))
        objects.append(make_pikeman(f"Formation Pikeman {i}", x))

    print(f"After formation mode there are {len(objects)} objects")
    
    outfile = f"formation_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")


# upgrade land's castle to max
def action_pimp(doc, island):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    player1 = obj_by_name(objects, "Player 1");
    player1["localPosition"]["x"] = 0
    obj_set_coins(player1, 69)

    castle = obj_by_name_contains(objects, "Castle")

    if "Castle0" in castle["name"]:
        init_shop("bow", objects)
        init_shop("hammer", objects);
        init_shop("scythe", objects);

    # upgrade castle
    global max_castle_level
    upgrade_castle(castle, max_castle_level)
    print(f"castle upgraded to level {max_castle_level}")

    # upgrade walls
    global max_wall_level
    upgrade_walls(objects, max_wall_level)

    # mark all trees for removal
    mark_trees(objects)

    # spawn some bros
    spawn_count = 10
    for i in range(spawn_count):
        archer = make_archer(f"Shooty Boy {i}")
        objects.append(archer)
        worker = make_worker(f"Good Ole Boy {i}")
        objects.append(worker)
        pikeman = make_pikeman(f"Pokey Boy {i}")
        objects.append(pikeman)

    print(f"pimped out island {island}")
    outfile = f"pimp_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")



def action_spawn(doc, island, num_archers, num_workers, num_pikemen):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    player1 = obj_by_name(objects, "Player 1")
    player_x = player1["localPosition"]["x"]

    if num_archers > 0 or num_pikemen > 0:
        player_set_formation_active(player1, True)

    for i in range(num_archers):
        archer = make_archer(f"Shooty Boy {i}", x=player_x)
        objects.append(archer)

    for i in range(num_workers):
        worker = make_worker(f"Good Ole Boy {i}", x=player_x)
        objects.append(worker)

    for i in range(num_pikemen):
        pikeman = make_pikeman(f"Pokey Boy {i}", x=player_x)
        objects.append(pikeman)


    print(f"After spawn there are {len(objects)} objects")

    outfile = f"spawn_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")



def probe():
    land = get_island_data("save_34.json", 8)
    print_objs_between(land["objects"], -5, 5)

if __name__ == "__main__":
    # probe()
    # sys.exit(0)

    action_list = {
        "take_over":   "destroy all non trigger portals, move to trigger portal with archer, worker, and idol",
        "destroy":     "destroy all portals",
        "exterminate": "kill all enemies",
        "formation":   "teleport to a position with a squad for battle",
        "spawn":       "spawn characters like archers or workers",
        "pimp":        "upgrade land's castle to max" }
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("action", choices=action_list, help="\n".join([f"{action:12} {help_msg}" for action, help_msg in action_list.items()]))
    parser.add_argument("save_file", help="path to a save file in json format")
    parser.add_argument("island", help="which island to affect (number)", type=int)

    parser.add_argument("-a", "--archers", type=int, default=0, help="how many archers to spawn")
    parser.add_argument("-w", "--workers", type=int, default=0, help="how many workers to spawn")
    parser.add_argument("-p", "--pikemen", type=int, default=0, help="how many pikemen to spawn")
    # parser.add_argument("-k", "--knights", type=int, default=0, help="how many knights to spawn")
    parser.add_argument("-x", "--position", type=int, help="x position")

    args = parser.parse_args()

    doc = parse_json_file(args.save_file)

    if args.action == "take_over":
        action_take_over(doc, args.island)
    elif args.action == "destroy":
        action_destroy(doc, args.island)
    elif args.action == "exterminate":
        action_exterminate(doc, args.island)
    elif args.action == "formation":
        if args.position != None:
            action_formation(doc, args.island, args.position)
        else:
            print("you must specify an x position with the formation action (-x, --position-x)")
            sys.exit(1)
    elif args.action == "spawn":
        action_spawn(doc, args.island, args.archers, args.workers, args.pikemen)
    elif args.action == "pimp":
        action_pimp(doc, args.island)
    
