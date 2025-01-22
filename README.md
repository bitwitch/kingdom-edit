# Kingdom Edit
A save file editor for Kingdom New Crowns: Call of Olympus.   

**Why?**  
As of December 2024, the game has some issues on Nintendo Switch and can corrupt your save file causing the game to be unplayable. My partner and I love this game and played it for many many hours, so when it broke I had to find a way to fix it so we could keep playing. I discovered that the save file format is just a json file that has been gzipped, so I hacked away at it to get us back to where we were when the game broke.  

**Warning: This is quick and dirty code that I wrote to solve my problem. I don't have time nor energy to make it a nice polished thing that is easy to use, but I am still releasing it just in case it can help someone anyway.**  

### Usage
`$ python kedit.py save_file -i island_number action `  

```
save_file
path to save a file in json format

-i, --island        
which island to affect (number)


actions:
goto                   go to island -i, with money and crew

take_over              destroy all non trigger portals, move to trigger portal with archer, worker, and idol

destroy                destroy all portals

exterminate            kill all enemies

pimp                   upgrade land's castle to 1 less than max (you can then manually upgrade it once more
                       to max, this is to avoid an error in castle placement when upgraded to max)

trees                  mark all trees for removal

formation              teleport to a position with a squad for battle
    -x, --position           x position to teleport to

spawn                  spawn characters like archers or workers
    -a, --archers            how many archers to spawn
    -w, --workers            how many archers to spawn
    -p, --pikemen            how many archers to spawn
      

```

## How To

### Take over an island
This action is meant for the first four small islands that have an idol and monument.  
1. Must visit that island at least once to populate the island data in the save file, assume for this example we are choosing island 1
2. Navigate to the directory where the game save file is located (e.g. C:\Users\shmow\AppData\LocalLow\noio\KingdomTwoCrowns\Release)
3. Decompress the save file into json
	`generate_json.bat save.json`
4. Execute kedit with the take_over action 
	`python kedit.py save.json -i 1 take_over`  
5. Gzip the newly generated save file
	`generate_save.bat take_over_1.json`
6. Run the game, you should spawn at the "trigger portal" along with an archer, a worker, the idol, and some coins
7. The archer should kill the portal in one shot as the hp has been lowered
8. Once the portal is gone, pay for the monument
9. Wait for worker to build it
10. Grab the idol and move it over to the monument


