# Kingdom Edit
A save file editor for Kingdom New Crowns: Call of Olympus.  

### Usage
```
python kedit.py action save_file island

action
- take_over    destroy all non trigger portals, move to trigger portal with archer, worker, and idol
- destroy      destroy all portals
- exterminate  kill all greed
- pimp         upgrade land's castle to max

save_file
path to save a file in json format

island
which island to affect (number)
```

## How To

### Take over an island
1. Must visit that island to populate that island data in the save file  
2. Decompress the save file into json  
	`generate_json.bat save.json`  
3. Execute kedit with the take_over action
	`python kedit.py take_over save.json 2`  
4. Run the game, you should spawn at the "trigger portal" along with an archer, a worker, the idol, and some coins
5. The archer should kill the portal in one shot as the hp has been lowered
6. Once the portal is gone, pay for the monument
7. Wait for worker to build it
7. Grab the idol and move it over to the monument

### Get an island unlockable upgrade


