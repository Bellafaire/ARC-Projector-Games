#!/usr/bin/ python3

#Imports
import argparse, random, time
import numpy as np

#Walking person class
class WalkingPerson: 
    """Object designed to imitate the motion of a person in the playing area of the projector game. 
    """
    def __init__(self, field_resolution, field_size): 
        """Creation of the WalkingPerson Object

        Args:
            field_resolution (Tuple Int): Resolution of the playing area, this is the resolution of the game itself
            field_size (Tuple Float): Size of the real-world play area in meters, this is the size of the projection on the floor. 
        """
        self.field_resolution = field_resolution
        self.field_size = field_size
        self.position = [random.random() * field_size[0], random.random() * field_size[1]]
        self.direction = 0
        self.velocity = 1

    def get_position(self): 
        """Gets the position of the walking person 

        Returns:
            Tuple Float: Position of the walking person in meters in format (x,y)
        """
        return (self.position[0], self.position[1])

    def move(self): 
        """Moves the object by a small amount, this function should be called repeatedly. There is a small chance that for 
            any given movement the person will change directions and velocity, otherwise it smoothly moves in its last decided direction
        """
        if(random.random() < 0.025): 
            self.direction = random.uniform(-np.pi, np.pi)

            #calculate the direction to the center of the field 
            diff = (self.position[0] - self.field_size[0]/2, self.position[1] - self.field_size[1]/2)  
            direction_to_center = np.arctan2(diff[1], diff[0])

            if(random.random() < 0.9): 
                self.direction = direction_to_center

            self.velocity = np.random.normal() * 0.025

            print("Object updated to direction %0.2f, with velocity %0.2f" % (self.direction, self.velocity))

        self.position[0] += self.velocity * np.cos(self.direction)
        self.position[1] += self.velocity * np.sin(self.direction)
        self.velocity *= 0.99

        if(self.position[0] > self.field_size[0]): 
            self.position[0] = self.field_size[0]
            self.velocity *= -1
        elif (self.position[0] < 0): 
            self.position[0] = 0
            self.velocity *= -1
        
        if(self.position[1] > self.field_size[1]): 
            self.position[1] = self.field_size[1]
            self.velocity *= -1
        elif (self.position[1] < 0): 
            self.position[1] = 0
            self.velocity *= -1
        

class LocationGenerator: 
    """LocationGenerator handles the generation of locations of objects and writing those objects to a file that can act as simulation of the lidar output
    """
    def __init__(self, field_resolution, field_size, num_people):
        """Constructor of LocationGenerator

        Args:
            field_resolution (Tuple (int)): Resolution in pixels of the python game (width,height). 
            field_size (Tuple (Float)): Size of the real-world projector field in meters in format (width, height)
            num_people (int): number of people to simulate
        """
        self.field_resolution = field_resolution
        self.field_size = field_size
        self.num_people = num_people
        print("Creating LocationGenerator with field resolution of (%d, %d) and field size of (%0.2fm, %0.2fm) with %d people in the playing field" % (self.field_resolution[0], self.field_resolution[1], self.field_size[0], self.field_size[1], self.num_people))

        self.people = []
        for a in range(0, num_people): 
            self.people.append(WalkingPerson(field_resolution, field_size))
        
    def move(self): 
        """Moves all WalkingPerson objects that available in the LocationGenerator
        """
        for a in self.people: 
            a.move()

    def write_to_file(self):
        """Writes the position of each tracked object in a text file that mirrors the output of the lidar tracker""" 

        output_string = ""
        for a in self.people: 
            output_string += "%0.6f,%0.6f\n" % (a.get_position()[1], a.get_position()[0])

        f = open("lidar_output.txt", "w")
        f.write(output_string)
        f.close()


def main(): 
    """Main function, entry point for the program. 
    uses the argparse library to better parse commandline arguments and allow for easier running of the program. 
    This allows us to automatically parse the arguments given by command line and also automatically generate the '-h' help string. 
    """

    #create parser and add arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--field_resolution", "-r", help="Resolution of the playing field in pixels given in format 'width:height'")
    arg_parser.add_argument("--field_size", "-s", help="Real-world size of the projected field in meters given in format 'width:height'")
    arg_parser.add_argument("--num_people", "-n", help="Number of people to simulate interacting with the game.")
    
    #parse arguments
    args = arg_parser.parse_args()

    #defaults
    field_resolution, field_size, num_people = (1920,1080), (3,2), 2

    #go through each argument, if the argument is None than it's not provided and we use the defaults. Otherwise take its value
    # and override the defaults
    #field resolution
    if(args.field_resolution is not None): 
        res = args.field_resolution.split(":")
        field_resolution = (int(res[0]), int(res[1]))

    #field size
    if(args.field_size is not None): 
        res = args.field_size.split(":")
        field_size = (float(res[0]), float(res[1]))

    #Num People
    if(args.num_people is not None): 
        num_people = int(args.num_people)

    #Create the location generator object 
    gen = LocationGenerator(field_resolution, field_size, num_people)

    #infinite loop (unless someone does ctrl + c)
    try: 
        while(True): 
            #move the objects
            gen.move()

            #write the objects to a file
            gen.write_to_file()

            #sleep for 25ms so we're not running at a million miles an hour. 
            time.sleep(0.025)
    except KeyboardInterrupt: 
        print("Exiting...")

if __name__ == "__main__": 
    main()

