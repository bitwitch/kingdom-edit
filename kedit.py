import argparse
import copy
import json
import sys

archer_template = { "name": "Archer P1 [B]", "parentObject": { "linkedObjectID": "" }, "hierarchyPath": "Level/GameLayer/", "prefabPath": "Prefabs/Characters/Archer", "uniqueID": "Archer P1 [B]--6969", "mode": 0, "createOrder": 12345, "linkOrder": 0, "decayHint": 0, "decayResistanceDays": 2, "decayedVersionPrefabPath": "Prefabs/Characters/Peasant", "netID": 1666, "crpcType": 1, "localPosition": { "x": 120.98619079589844, "y": 0.8799997568130493, "z": 0.7556657791137695 }, "localScale": { "x": -1.0, "y": 1.0, "z": 1.0 }, "componentData2": [ { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":0,\"gems\":0,\"usesCurrencySystem\":true,\"currency\":{\"Coins\":1,\"Gems\":0,\"Crown\":0,\"Skulls\":0,\"Shades\":0,\"Merchandise\":0}}" }, { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" }, { "name": "Archer", "type": "ArcherData", "data": "{\"tower\":{\"linkedObjectID\":\"\"},\"knight\":{\"linkedObjectID\":\"\"},\"guardSide\":1,\"guardDepth\":0,\"desiredAttackMode\":0,\"despawnOnLoad\":false}" }, { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":0,\"invulnerable\":false}" }, { "name": "GenderAnimatorSelector", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":false}" }, { "name": "Petrifiable", "type": "PetrifiableSaveData", "data": "{\"RemainingHP\":0,\"IsPetrified\":false,\"RemainingDuration\":-106.38296508789063}" }, { "name": "Embarkee", "type": "EmbarkeeSaveData", "data": "{\"IsEmbarked\":false,\"SlotId\":-1,\"Embarkable\":{\"linkedObjectID\":\"\"}}" } ] }

worker_template = { "name": "Worker P1 [A]", "parentObject": { "linkedObjectID": "" }, "hierarchyPath": "Level/GameLayer/", "prefabPath": "Prefabs/Characters/Worker", "uniqueID": "Worker P1 [A]--6969", "mode": 0, "createOrder": 22222, "linkOrder": 0, "decayHint": 4, "decayResistanceDays": 1, "decayedVersionPrefabPath": "Prefabs/Characters/Peasant", "netID": 1098, "crpcType": 1, "localPosition": { "x": 127.18162536621094, "y": 0.875, "z": 0.5052622556686401 }, "localScale": { "x": -1.0, "y": 1.0, "z": 1.0 }, "componentData2": [ { "name": "Wallet", "type": "WalletData", "data": "{\"coins\":0,\"gems\":0,\"usesCurrencySystem\":true,\"currency\":{\"Coins\":1,\"Gems\":0,\"Crown\":0,\"Skulls\":0,\"Shades\":0,\"Merchandise\":0}}" }, { "name": "Character", "type": "CharacterData", "data": "{\"isGrabbed\":false,\"inert\":false}" }, { "name": "Worker", "type": "WorkerData", "data": "{\"despawnOnLoad\":false}" }, { "name": "Damageable", "type": "DamageableData", "data": "{\"hitPoints\":0,\"invulnerable\":false}" }, { "name": "GenderAnimatorSelector", "type": "GenderSelectorSaveData", "data": "{\"IsFemale\":false}" }, { "name": "Petrifiable", "type": "PetrifiableSaveData", "data": "{\"RemainingHP\":0,\"IsPetrified\":false,\"RemainingDuration\":-106.38296508789063}" }, { "name": "Embarkee", "type": "EmbarkeeSaveData", "data": "{\"IsEmbarked\":false,\"SlotId\":-1,\"Embarkable\":{\"linkedObjectID\":\"\"}}" } ] }


def player_set_formation_active(obj, val):
    for comp in obj["componentData2"]:
        if comp["name"] == "Player":
            data = json.loads(comp["data"])
            data["isFormationActive"] = val
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

# destroy all non trigger portals, move to trigger portal with archer, worker, and idol
def action_take_over(doc, island):
    campaign_index = 0
    campaign = doc["campaigns"][campaign_index]
    land = campaign["_islands"][island]
    objects = land["objects"]

    print(f"Land {island} has {len(objects)} objects")

    portal_x = 0
    new_objects = []

    for i, obj in enumerate(objects):
        if obj_has_component(obj, "Portal"):
            if obj_has_component(obj, "QuestTransitionTrigger"):
                obj_set_hp(obj, 1)
                portal_x = obj["localPosition"]["x"]
                new_objects.append(obj)
        else:
            new_objects.append(obj)

    print(f"After there are {len(new_objects)} objects")

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

    archer = copy.deepcopy(archer_template)
    archer["name"] += " - steve"
    archer["uniqueID"] += "69"
    archer["localPosition"]["x"] = target_x
    new_objects.append(archer)

    worker = copy.deepcopy(worker_template)
    worker["name"] += " - joey"
    worker["uniqueID"] += "00"
    worker["localPosition"]["x"] = target_x
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

    new_objects = []

    for i, obj in enumerate(objects):
        if not obj_has_component(obj, "Portal"):
            new_objects.append(obj)

    campaign["currentReign"]["landData"][island]["portals"] = 0
    land["objects"] = new_objects

    print(f"After there are {len(new_objects)} objects")
    
    outfile = f"destroy_{island}.json"
    with open(outfile, "w") as f:
        json.dump(doc, f)
    print(f"save file written to {outfile}")


# upgrade land's castle to max
def action_pimp(doc, island):
    assert 0, "Not Implemented"

if __name__ == "__main__":
    action_list = {
        "take_over": "destroy all non trigger portals, move to trigger portal with archer, worker, and idol",
        "destroy":   "destroy all portals",
        "pimp":      "upgrade land's castle to max" }
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("action", choices=action_list, help="\n".join([f"{action:10} - {help_msg}" for action, help_msg in action_list.items()]))
    parser.add_argument("save_file", help="path to a save file in json format")
    parser.add_argument("island", help="which island to affect (number)", type=int)
    args = parser.parse_args()

    with open(args.save_file, "r") as f:
        doc = json.load(f)

    if args.action == "take_over":
        action_take_over(doc, args.island)
    elif args.action == "destroy":
        action_destroy(doc, args.island)
    elif args.action == "pimp":
        action_pimp(doc, args.island)
    