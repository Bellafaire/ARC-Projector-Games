# ARC-Projector-Games

This repo contains the games for the Augmented Reality Center Interactive display project. 
Each game is contained in its own folder inside this repo. 
Current games incldue: 
- random particles 
- distortion grid

All games interact with the [lidar-people-detect](https://github.com/Makers-Oakland-University/lidar-people-detect) ros project through the lidar_output.txt file which will be generated when the ros system is running. 
To deploy these games with the projector, both the game **AND** the ros system must be running at the same time. 
All games in this repo are written in [PyGame](https://www.pygame.org/wiki/GettingStarted), a basic example of a game for the ARC project is provided in this repo under the basic_example folder. 


# movement_simulation.py
The movement_simulation.py file is provided in this repo to aid development of ARC projector games. 
It generates tracked object movements in a way that somewhat mirrors how people may move in playing the games. 
To run this file open the repo location in the terminal and type: 

```./movement_simulation```

The movement_simulation python script has a number of additonal optional parameters to mirror the environment the projector is operating in. 
For help run the script with the ```-h``` flag to get the available parameters: 

```
usage: movement_simulation.py [-h] [--field_resolution FIELD_RESOLUTION]
                              [--field_size FIELD_SIZE]
                              [--num_people NUM_PEOPLE]
optional arguments:
  -h, --help            show this help message and exit
  --field_resolution FIELD_RESOLUTION, -r FIELD_RESOLUTION
                        Resolution of the playing field in pixels given in
                        format 'width:height'
  --field_size FIELD_SIZE, -s FIELD_SIZE
                        Real-world size of the projected field in meters given
                        in format 'width:height'
  --num_people NUM_PEOPLE, -n NUM_PEOPLE
                        Number of people to simulate interacting with the
                        game.
```

as an example to set the field size to 5 meters by 3.5 meters with 6 people on the field we can run the script as: 
```
./movement_simulation -s 5:3.5 -n 6
```

# Contributing 

If you want to contribute a game to the ARC interactive display clone this repo and create a game in its own folder then create a pull request. 