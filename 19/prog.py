from __future__ import annotations
from typing import List
from helpers import Beacon, Scanner, findComponent
# wtf this task is insane?


# read the input
scanners: List[Scanner] = []
with open("input") as f:
    inp = f.read().split("\n\n")
    for s in range(len(inp)):
        beacons = inp[s].split("\n")[1:]
        scanners.append(Scanner(s, beacons))


# find all the scanners which overlap, storing them in a adjacency list type data structure
overlaps = dict([ (i, {}) for i in range(len(scanners)) ])
for i1 in range(len(scanners)):
    for i2 in range(len(scanners)):
        if i1 == i2: continue

        s1 = scanners[i1]
        s2 = scanners[i2]
        overlap = s1.overlapping(s2)
        if overlap:
            overlaps[s1.id][s2.id] = (overlap[0], overlap[1])


# think of the overlaps as a graph and find the strongly connected components, 
# pick the any scanner in that component, and reduce all other scanners down to it
# then you can use set notation to determine which beacons overlap, and which dont, to get final total count  # for p1
adjDict = dict([ (i, set(overlaps[i].keys())) for i in overlaps ])
components = {}
uniqueComponents = []
for sc in overlaps:
    component = findComponent(sc, adjDict, {}, 0)
    if set(component.keys()) in uniqueComponents:
        continue  # skip this because a component for this scanner has already been found
    components[sc] = component
    uniqueComponents.append(set(component.keys()))

# now descending sort the scanners in each component their distance from the first component
for c in components:
    components[c] = dict(sorted(components[c].items(), key=lambda n: n[1], reverse=True))




# p1
# finally reduce them down
uniqueBeacons = dict([ (i, set(map(lambda b: tuple(b), scanners[i].beacons))) for i in range(len(scanners)) ])
# go through each component  (I dont think there are multiple but just incase)
for c in components:
    scannerDistances = components[c]
    # go through the scanners starting at the furthest away
    for sid in scannerDistances:
        dist = scannerDistances[sid]
        if dist == 0:  # cant reduce this, this is the base of the component
            continue
            
        # find an appropriate closer scanner to reduce it to
        targetSid = None
        for targetSid in adjDict[sid]:
            if scannerDistances[targetSid] < dist:
                # found a valid one
                break

        # reduce sid to overlap sid
        # print(sid, "->", overlapSid, overlaps[overlapSid][sid])
        for coords in uniqueBeacons[sid]:
            rearrCoords = Beacon(coords).remap(overlaps[targetSid][sid][1])  # rearrange the coords to be relative correct
            offset = overlaps[targetSid][sid][0]  # the coordinates of the target Scanner
            remapCoords = ( rearrCoords[0] + offset[0], rearrCoords[1] + offset[1], rearrCoords[2] + offset[2] )
            uniqueBeacons[targetSid].add(remapCoords)  # add the remapped beacon to the unique beacons for the target scanner
        del uniqueBeacons[sid]  # since all beacons have been transfered, delete the old scanners beacons storage

# result, find the size of each component (even though there is only one in input)
total = 0
for c in components:
    total += len(uniqueBeacons[c])
print(total)




# p2  i think this assumes there is only one component, so ima do the same
# reduce all the scanners coordinates down to all be relative to a single scanner
relativeLocations = overlaps
scannerDistances = components[0]
# go through each scanner
for sid in scannerDistances:
    dist = scannerDistances[sid]
    if dist == 0:  # cant reduce this, this is the base of the component
        continue
        
    # find an appropriate scanner to recalculate its location relative to
    targetSid = None
    for targetSid in adjDict[sid]:
        if scannerDistances[targetSid] < dist:
            # found a valid one
            break

    # go through each of the local scanners which are currently known relative to sid, 
    # and make them relative to targetSid instead
    for localSid in relativeLocations[sid]:
        if scannerDistances[localSid] <= dist:
            continue  # since we dont want to reduce stuff that is closer to the final target
        
        coords = relativeLocations[sid][localSid][0]  # the local scanners coords
        sidCoords = relativeLocations[targetSid][sid][0]  # the coords of the sid
        orientation = relativeLocations[targetSid][sid][1]  # the sids orientation relative to targetSid
        rearrCoords = Beacon(coords).remap(orientation)  # reoriented the coords
        localCoordsRelativeToTarget = ( rearrCoords[0] + sidCoords[0], rearrCoords[1] + sidCoords[1], rearrCoords[2] + sidCoords[2] )
        relativeLocations[targetSid][localSid] = (localCoordsRelativeToTarget, orientation)  # transfer the localsid to targetsid
    
    del relativeLocations[sid]  # delete the scanners storage, since all relative scanners have been transfered to a target

# now all locations should be relative to one location
locations = [(0, 0, 0)]
locations.extend(list(map(lambda c: c[0], relativeLocations[0].values())))
largest = 0
for l1 in locations:
    for l2 in locations:
        dx = abs(l1[0] - l2[0])
        dy = abs(l1[1] - l2[1])
        dz = abs(l1[2] - l2[2])
        mdist = dx + dy + dz
        largest = max(largest, mdist)

print(largest)