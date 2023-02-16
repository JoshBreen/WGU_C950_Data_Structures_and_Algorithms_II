# Josh Breen Student ID: 
# Big-O Notation: N^4

import csv
import sys


# Sets up the Hash Table
# Big-O Notation = O(n)
class HashTable:
    # Creates initial table with 40 empty buckets to be filled with packages
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def search(self, key):  # Searches hashtable for package
        bucket = (hash(key) % 100) - 1
        bl = self.table[bucket]
        for kv in bl:
            if kv[0] == key:
                return kv[1]
        return None

    def insert(self, key, item):  # inserts into hashtable
        bucket = (hash(key) % 100) - 1
        bl = self.table[bucket]
        for kv in bl:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bl.append(key_value)
        return True

    def remove(self, key):  # removes package from hashtable
        bucket = (hash(key) % 100) - 1
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


# Setting up the Package class
# Big-O Notation = O(1)
class Package:
    def __init__(self, ID, address, city, state, zip, deliveryDeadline, mass, specialNotes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.mass = mass
        self.specialNotes = specialNotes
        self.status = status
        self.time_delivered = ""
        self.delivered = False

    def __str__(self):  # overwite
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip, self.deliveryDeadline, self.mass, self.specialNotes, self.status)


hub = '4001 South 700 East'     # Sets hub as the main hub address


# Setting up the Truck class
# Big-O Notation = O(1)
class Truck:
    def __init__(self):
        self.storageLimit = 16
        self.milesTraveled = 0
        self.speed = 18
        self.storage = {}
        self.tripNumber = 0
        self.currentLocation = hub
        self.load1 = []
        self.load2 = []


# Big-O Notation = O(n)
master_package_list = HashTable()
with open('WGUPS Package File.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pID = int(row["Package ID"])
        pAddress = str(row["Address"])
        pCity = str(row["City"])
        pState = str(row["State"])
        pZip = str(row["Zip"])
        pDeadline = str(row["Delivery Deadline"])
        pMass = int(row["Mass KILO"])
        pNotes = str(row["Special Notes"])
        pStatus = "At Hub"

        p = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pMass, pNotes, pStatus)

        master_package_list.insert(pID, p)


# Populates the address list table as a dictionary so we can find distances
# Big-O Notation = O(n)
address_list = {}
with open('WGUPS Distance Table.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        address_list[row['Location']] = {'Western Governors University 4001 South 700 East, Salt Lake City, UT 84107': row['Western Governors University 4001 South 700 East, Salt Lake City, UT 84107'],
                                           'International Peace Gardens 1060 Dalton Ave S': row['International Peace Gardens 1060 Dalton Ave S'],
                                           'Sugar House Park 1330 2100 S': row['Sugar House Park 1330 2100 S'],
                                           'Taylorsville-Bennion Heritage City Gov Off 1488 4800 S': row['Taylorsville-Bennion Heritage City Gov Off 1488 4800 S'],
                                           'Salt Lake City Division of Health Services 177 W Price Ave': row['Salt Lake City Division of Health Services 177 W Price Ave'],
                                           'South Salt Lake Public Works 195 W Oakland Ave': row['South Salt Lake Public Works 195 W Oakland Ave'],
                                           'Salt Lake City Streets and Sanitation 2010 W 500 S': row['Salt Lake City Streets and Sanitation 2010 W 500 S'],
                                           'Deker Lake 2300 Parkway Blvd': row['Deker Lake 2300 Parkway Blvd'],
                                           'Salt Lake City Ottinger Hall 233 Canyon Rd': row['Salt Lake City Ottinger Hall 233 Canyon Rd'],
                                           'Columbus Library 2530 S 500 E': row['Columbus Library 2530 S 500 E'],
                                           'Taylorsville City Hall 2600 Taylorsville Blvd': row['Taylorsville City Hall 2600 Taylorsville Blvd'],
                                           'South Salt Lake Police 2835 Main St': row['South Salt Lake Police 2835 Main St'],
                                           'Council Hall 300 State St': row['Council Hall 300 State St'],
                                           'Redwood Park 3060 Lester St': row['Redwood Park 3060 Lester St'],
                                           'Salt Lake County Mental Health 3148 S 1100 W': row['Salt Lake County Mental Health 3148 S 1100 W'],
                                           'Salt Lake County/United Police Dept 3365 S 900 W': row['Salt Lake County/United Police Dept 3365 S 900 W'],
                                           'West Valley Prosecutor 3575 W Valley Central Station bus Loop': row['West Valley Prosecutor 3575 W Valley Central Station bus Loop'],
                                           'Housing Auth. of Salt Lake County 3595 Main St': row['Housing Auth. of Salt Lake County 3595 Main St'],
                                           'Utah DMV Administrative Office 380 W 2880 S': row['Utah DMV Administrative Office 380 W 2880 S'],
                                           'Third District Juvenile Court 410 S State St': row['Third District Juvenile Court 410 S State St'],
                                           'Cottonwood Regional Softball Complex 4300 S 1300 E': row['Cottonwood Regional Softball Complex 4300 S 1300 E'],
                                           'Holiday City Office 4580 S 2300 E': row['Holiday City Office 4580 S 2300 E'],
                                           'Murray City Museum 5025 State St': row['Murray City Museum 5025 State St'],
                                           'Valley Regional Softball Complex 5100 South 2700 West': row['Valley Regional Softball Complex 5100 South 2700 West'],
                                           'City Center of Rock Springs 5383 South 900 East #104': row['City Center of Rock Springs 5383 South 900 East #104'],
                                           'Rice Terrace Pavilion Park 600 E 900 South': row['Rice Terrace Pavilion Park 600 E 900 South'],
                                           'Wheeler Historic Farm 6351 South 900 East': row['Wheeler Historic Farm 6351 South 900 East']
                                           }


# Searches for the distance from the current address to the next
# Big-O Notation = O(N^4)
def distance_between(currentLoc, nextLoc):
    for k1, v1 in address_list.items():
        if currentLoc in k1:          # takes the partial address and searches it for the full key
            for k2, v2 in v1.items():      # takes the values of all the distances from that location
                if nextLoc in k2:    # searches for the next location from the current address
                    if(not v2):                    # checks to make sure it has a value, if not it reverses the address order to get the value
                        for k3, v3 in address_list.items():   # if the first search didn't return a result it reverses the addresses
                            if nextLoc in k3:
                                for k4, v4 in v3.items():
                                    if currentLoc in k4:
                                        dist2 = float(v4)       # returns the distance from the second search
                                        return(dist2)
                    else:     # if it finds a number it returns the number
                        dist = float(v2)
                        return(dist)


# Creating the trucks
Truck1 = Truck()
Truck1.load1 = [15, 16, 34, 14, 19, 20, 21, 4, 40, 7, 29, 2, 33, 1, 13, 39]
Truck1.load2 = [31, 32, 6, 12, 9, 23, 11]
Truck2 = Truck()
Truck2.load1 = [3, 8, 30, 5, 37, 38, 10, 27, 35, 36, 17, 18]
Truck2.load2 = [25, 26, 22, 24, 28]


# converts time into minutes
def calculate_minutes(hr, min):
    y = hr * 60
    w = y + min
    return w


# Delivers the packages
# Big-O Notation = O(N^2)
def deliver_packages(truck, hour, mins):
    deliver_hour = 8
    deliver_minutes = 0

    for x in range(2):
        if truck.currentLocation == hub:
            if truck.tripNumber == 0:     # Loads the truck with the first load of packages
                for r in truck.load1:
                    truck.storage[r] = master_package_list.search(r)    # Puts the packages in the truck
                    truck.storage[r].status = 'en route'       # Updates the package status to en route

            else:
                for q in truck.load2:     # Loads the trucks with the second load of packages
                    truck.storage[q] = master_package_list.search(q)      # Puts the packages in the truck
                    if truck.storage[q] == master_package_list.search(9):
                        truck.storage[q].address = '410 S State St'
                        truck.storage[q].zip = '84111'

                    truck.storage[q].status = 'en route'    # Updates the package status to en route

            for z in truck.storage:
                if truck.currentLocation == truck.storage[z].address:    # Checks to see if there are multiple packages to be delivered to the same address
                    truck.storage[z].time_delivered = '{}:{:02d}'.format(deliver_hour, deliver_minutes)    # Updates packaged time delivered
                    truck.storage[z].status = 'Delivered at {}:{:02d}'.format(deliver_hour, deliver_minutes)    # Updates status of package and time delivered
                    truck.storage[z].delivered = True      # Marks packaged as delivered which is used in min_distance to avoid checking delivered packages

                else:
                    d = min_distance(truck)
                    if d == {}:            # Checks to make sure there is a package
                        break              # If no more packages we are done with this part
                    else:
                        distance_traveled = distance_between(truck.currentLocation, d.address)   # Runs distanceBetween to figure out how far to next address
                        minutes = round((distance_traveled / truck.speed) * 60)   # determine time taken to travel to next location
                        deliver_minutes += minutes                                # increase minutes
                        if deliver_minutes >= 60:       # Checks to see if we are over 60 minutes, if so it converts 60 to 1 hour
                            deliver_minutes %= 60       # Takes what remains after taking out the 60
                            deliver_hour += 1           # Adds an hour to the time

                        current_time_min = calculate_minutes(deliver_hour, deliver_minutes)
                        compared_time_min = calculate_minutes(hour, mins)
                        if current_time_min < compared_time_min:
                            truck.milesTraveled += distance_traveled    # Increases the mileage on the truck
                            truck.currentLocation = d.address           # Updates the trucks location to the now current address
                            truck.storage[d.ID].time_delivered = '{}:{:02d}'.format(deliver_hour, deliver_minutes)   # Updates packaged time delivered
                            truck.storage[d.ID].status = 'Delivered at {}:{:02d}'.format(deliver_hour, deliver_minutes)   # Updates status of package and time delivered
                            truck.storage[d.ID].delivered = True    # Marks packaged as delivered which is used in min_distance to avoid checking delivered packages
                        else:
                            break

# Return to Hub
        distancetohub = distance_between(truck.currentLocation, hub)      # Figures out how far to get back to the hub
        minutes = round((distancetohub / truck.speed) * 60)  # determine time taken to travel to next location
        deliver_minutes += minutes  # increase minutes
        if deliver_minutes >= 60:  # Checks to see if we are over 60 minutes, if so it converts 60 to 1 hour
            deliver_minutes %= 60  # Takes what remains after taking out the 60
            deliver_hour += 1  # Adds an hour to the time
        truck.milesTraveled += distancetohub               # Updates the trucks mileage once back at the hub
        truck.currentLocation = hub                        # Updates the trucks current location to be at the hub
        truck.tripNumber += 1                              # Updates the trucks trip number so it knows when to pick up load 2 or it is done


# Used to determine which package would be the next closest to deliver
# Big-O Notation = O(N^2)
def min_distance(truck):
    d = {}
    min_dis = 100
    for a in truck.storage:
        if not truck.storage[a].delivered:  # confirm that the package had not already been delivered
            min_dis = distance_between(truck.currentLocation, truck.storage[a].address)  # sets the minimum distance
            d = truck.storage[a]
        for y in truck.storage:
            if not truck.storage[y].delivered:    # confirms that the compared packages have not already been delivered
                compare = distance_between(truck.currentLocation, truck.storage[y].address)   # sets the second distance to compare
                if min_dis > compare:
                    min_dis = compare          # if the compare distance is smaller sets it as the new min_dis
                    d = truck.storage[y]       # saves the package info if it is the shortest distance
        return d


# Command Line Console
# Big-O Notation = O(1)
print('Select from the following options:')
print('1 = Look Up Package by ID')
print('2 = Print All Packages')
print('3 = Enter Time to Check Status')
print('4 = Exit')

# Big-O Notation = O(1)
while True:
    try:
        inp = int(input('Please type selection:'))
    except ValueError:
        print('Input must be a number')
        continue

    if inp == 1:
        id_lookup = int(input("Insert Package Number: "))
        deliver_packages(Truck1, 88, 88)         # Input hour and minute outside time to avoid it causing problems
        deliver_packages(Truck2, 88, 88)
        if (id_lookup > 0) & (id_lookup < 41):
            print('ID, Address, City, State, Zip, Delivery Deadline, Weight, Special Instructions, Status')
            print(master_package_list.search(id_lookup))
        else:
            print('Package not found.')

    if inp == 2:
        deliver_packages(Truck1, 88, 88)   # Input hour and minute outside time to avoid it causing problems
        deliver_packages(Truck2, 88, 88)

        for x in range (1, 41):
            print(master_package_list.search(x))
        print("Total Truck Mileage: {:.2f}".format(Truck1.milesTraveled + Truck2.milesTraveled))

    if inp == 3:
        time_search = input('Type time as 00:00 (24 Hour Time):  ')
        input_hr, input_mins = time_search.split(':')
        user_hr = int(input_hr)                           # parse hour into int
        user_mins = int(input_mins)                       # parse minutes into int
        deliver_packages(Truck1, user_hr, user_mins)      # Runs deliver packages with user input time as cut off
        deliver_packages(Truck2, user_hr, user_mins)
        for x in range (1, 41):
            print(master_package_list.search(x))          # Prints list after it's been run to the cut off

    if inp == 4:
        sys.exit('Thank you')
