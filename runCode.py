import os
import argparse
import time
import datetime
import re
from collections import OrderedDict
from Graph import Graph
import itertools



def main():
    siteConfig = OrderedDict() 
    ######################################
    # define the site configuration
    ######################################
    option = OrderedDict()
    name = "HRPS"
    option["Name"]      = name
    option["Link"]      = ["Bronte", "WhiteOaks"]
    option["Type"]      = ["Dispatch", "Prime", "Core"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Prime": 1008, "Dispatch": 1640 + 1304, "DSRCore": 5200, "GeoPrime": 10000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Bronte"
    option["Name"]      = name
    option["Link"]      = ["Lakeshore", "HRPS"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()    
    name = "WhiteOaks"
    option["Name"]      = name
    option["Link"]      = ["HRPS", "MiltonWT"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Lakeshore"
    option["Name"]      = name
    option["Link"]      = ["Waterdown", "Bronte"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Waterdown"
    option["Name"]      = name
    option["Link"]      = ["BurlingtonFire", "Rattlesnake" , "Lakeshore"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "BurlingtonFire"
    option["Name"]      = name
    option["Link"]      = ["Waterdown"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Rattlesnake"
    option["Name"]      = name
    option["Link"]      = ["MiltonFire", "Brookville" , "Waterdown", "MiltonWT"]
    #option["Link"]      = ["MiltonFire", "Brookville" , "Waterdown", "Ghost"]
    option["Type"]      = ["Subsite", "GeoPrime"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000, "Prime": 1008 , "GeoPrime": 10000}
    siteConfig[name] = option

    #option = OrderedDict()
    #name = "Ghost"
    #option["Name"]      = name
    #option["Link"]      = ["MiltonWT", "Rattlesnake"]
    #option["Type"]      = ["Subsite"]
    #option["Zone"]      = 1
    #option["Site"]      = 1
    #option["Bandwidth"] = {"Subsite": 0}
    #siteConfig[name] = option

    option = OrderedDict()
    name = "MiltonWT"
    option["Name"]      = name
    option["Link"]      = ["WhiteOaks", "Rattlesnake" , "Speyside"]
    #option["Link"]      = ["WhiteOaks", "Ghost", "Speyside"]
    option["Type"]      = ["Subsite", "Prime"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {'Subsite': 352, "Prime": 2000}
    siteConfig[name] = option


    option = OrderedDict()
    name = "MiltonFire"
    option["Name"]      = name
    option["Link"]      = ["Rattlesnake"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Brookville"
    option["Name"]      = name
    option["Link"]      = ["Acton", "Rattlesnake"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Acton"
    option["Name"]      = name
    option["Link"]      = ["Georgetown", "Brookville"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Georgetown"
    option["Name"]      = name
    option["Link"]      = ["HHFire", "Speyside" , "Acton"]
    option["Type"]      = ["Subsite", "DSRCore"]
    option["Bandwidth"] = {'Subsite': 688, "DSRCore": 5200}
    option["Zone"]      = 1
    option["Site"]      = 2
    siteConfig[name] = option

    option = OrderedDict()
    name = "HHFire"
    option["Name"]      = name
    option["Link"]      = ["Georgetown"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Speyside"
    option["Name"]      = name
    option["Link"]      = ["MiltonWT", "Georgetown"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option


    siteGraph = getGraph(siteConfig)
    
    print(siteGraph)

    #print(siteGraph.find_shortest_path("Bronte", "HRPS"))
    #print(siteGraph.find_shortest_path("HRPS", "Georgetown"))
    #print(siteGraph.find_shortest_path("HRPS", "Rattlesnake"))

    runTest("HRPS", "HRPS", siteConfig, siteGraph)



def runTest(primeSiteName, coreSiteName, siteConfig, siteGraph):
    
    uniqueSite = []
    for key in siteConfig:
        uniqueSite.append(siteConfig[key]["Site"])

        pass

    uniqueSite = list(set(uniqueSite))
    uniquePrimeSite = {}
    for siteNum in uniqueSite:
        uniquePrimeSite[siteNum] = []
        for key in siteConfig:
            if('Prime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                uniquePrimeSite[siteNum].append(key)
                pass
            if('GeoPrime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                uniquePrimeSite[siteNum].append(key)
                pass

            pass
        pass

    
    keysToDelete = []
    for key in uniquePrimeSite:
        print key, uniquePrimeSite[key], len(uniquePrimeSite[key])
        if(len(uniquePrimeSite[key]) == 0):
            keysToDelete.append(key)
            pass
        pass
    print keysToDelete
    for key in keysToDelete:
        del uniquePrimeSite[key]

    print uniquePrimeSite

    SUT_to_PUT_loading = {}
    for siteNum in uniquePrimeSite:
        if(len(uniquePrimeSite[siteNum]) == 0):
            continue
        SUT_to_PUT_loading[siteNum] = {}

        for site in uniquePrimeSite[siteNum]:
            print "Testing SUT to PUT loading", siteNum, site
            SUT_to_PUT_loading[siteNum][site] = runSubSiteToPrimeTest(site, siteConfig, siteGraph)
            pass
        pass


    primeSiteList = []
    for siteNum in uniquePrimeSite:
        primeSiteList.append(uniquePrimeSite[siteNum])
        pass
    print primeSiteList

    activePrimeSiteCombinations = itertools.product(*primeSiteList)

    # list of active core + DSR core in a given zone
    uniqueZone = []
    for key in siteConfig:
        uniqueZone.append(siteConfig[key]["Zone"])
        pass

    uniqueZone = list(set(uniqueZone))
    uniqueZoneSite = {}
    for zoneNum in uniqueZone:
        uniqueZoneSite[zoneNum] = []
        for key in siteConfig:
            if('Core' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                uniqueZoneSite[zoneNum].append(key)
                pass
            if('DSRCore' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                uniqueZoneSite[zoneNum].append(key)
                pass

            pass
        pass

    print uniqueZoneSite

    
    PUT_TO_CUT_loading = {}

    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            PUT_TO_CUT_loading[activeCore] = {}
            for currActivePrime in itertools.product(*primeSiteList):
                print 'Running Loading', activeCore, currActivePrime
                PUT_TO_CUT_loading[activeCore][currActivePrime] = runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph)
                pass
            pass
        pass


    # DUT to CUT loading
    DUT_TO_CUT_loading = {}
    print "DUT to CUT loading"
    
    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            print "Testing active Core",activeCore
            DUT_TO_CUT_loading[activeCore] = runDispatchToCoreTest(activeCore, siteConfig, siteGraph)
            pass
        pass


def runDispatchToCoreTest(activeCore, siteConfig, siteGraph):
    # define the struture to store graph bandwidth loading
    bwLoad = {}
    for key in siteConfig:
        bwLoad[key] = {}
        for keyprime in siteConfig:
            bwLoad[key][keyprime] = 0
            pass
        pass

    # get the dispatch sites in the same zone
    dispatchList = []
    for key in siteConfig:
        # skip any location that is not a dispatch
        if("Dispatch" not in siteConfig[key]['Type']):
            continue

        # skip any location that is not in the same zone 
        if(siteConfig[key]['Zone'] != siteConfig[activeCore]['Zone']):
            continue

        dispatchList.append(key)
        pass

    # find the shortest path from each dispatch to the core
    for dispatch in dispatchList:
        print 'Path from', dispatch, activeCore
        pathList = siteGraph.find_shortest_path(dispatch, activeCore)
        #print pathList
        if(len(pathList) == 1):
            path = pathList[0]
        else:
            print pathList
            xString = input("Pick your path: ")
            x = int(xString)
            path = pathList[x]
            pass

        bwSite = siteConfig[dispatch]['Bandwidth']['Dispatch']
        
        for i in range(0, len(path)-1):
            bwLoad[path[i]][path[i+1]] += bwSite
            #print "loading", path[i], path[i+1], bwSite
            pass
        pass

    for key in siteConfig:
        for keyprime in siteConfig:
            if(bwLoad[key][keyprime] == 0):
                continue
            print key, keyprime, bwLoad[key][keyprime]
            pass
        pass

    return bwLoad

     

def runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph):
    # define the struture to store graph bandwidth loading
    bwLoad = {}
    for key in siteConfig:
        bwLoad[key] = {}
        for keyprime in siteConfig:
            bwLoad[key][keyprime] = 0
            pass
        pass

    # find the shortest path from each subsite to the prime
    for prime in currActivePrime:
        print 'Path from', prime, activeCore
        pathList = siteGraph.find_shortest_path(prime, activeCore)
        #print pathList
        if(len(pathList) == 1):
            path = pathList[0]
        else:
            print pathList
            xString = input("Pick your path: ")
            x = int(xString)
            path = pathList[x]
            pass

        bwSite = siteConfig[prime]['Bandwidth']['Prime']
        
        for i in range(0, len(path)-1):
            bwLoad[path[i]][path[i+1]] += bwSite
            #print "loading", path[i], path[i+1], bwSite
            pass
        pass

    for key in siteConfig:
        for keyprime in siteConfig:
            if(bwLoad[key][keyprime] == 0):
                continue
            print key, keyprime, bwLoad[key][keyprime]
            pass
        pass

    return bwLoad



def runSubSiteToPrimeTest(primeSiteName, siteConfig, siteGraph):
    # define the struture to store graph bandwidth loading
    bwLoad = {}
    for key in siteConfig:
        bwLoad[key] = {}
        for keyprime in siteConfig:
            bwLoad[key][keyprime] = 0
            pass
        pass


    # subsite -> prime test
    # first get the list of all subsites
    subsiteList = []
    for key in siteConfig:
        # skip any location that is not a subsite
        if("Subsite" not in siteConfig[key]['Type']):
            continue

        # skip any location that is not in the same site 
        if(siteConfig[key]['Site'] != siteConfig[primeSiteName]['Site']):
            continue

        subsiteList.append(key)
        pass


    # find the shortest path from each subsite to the prime
    for subsite in subsiteList:
        #print subsite, primeSiteName
        #print(siteGraph.find_shortest_path(subsite, primeSiteName))
        pathList = siteGraph.find_shortest_path(subsite, primeSiteName)
        if(len(pathList) == 1):
            path = pathList[0]
        else:
            print pathList
            xString = input("Pick your path: ")
            x = int(xString)
            path = pathList[x]
            pass

        bwSite = siteConfig[subsite]['Bandwidth']['Subsite']
        
        for i in range(0, len(path)-1):
            bwLoad[path[i]][path[i+1]] += bwSite
            #print "loading", path[i], path[i+1], bwSite
            pass
        pass

    for key in siteConfig:
        for keyprime in siteConfig:
            if(bwLoad[key][keyprime] == 0):
                continue
            print key, keyprime, bwLoad[key][keyprime]
            pass
        pass

    return bwLoad





def getGraph(siteConfig):
    " This helper function creates the graph network for the site"
    graphDef = {}
    for key in siteConfig:
        graphDef[siteConfig[key]['Name']] = siteConfig[key]['Link']
        pass
    return Graph(graphDef)




if __name__ == "__main__":
    start_time = time.time()
    main()
    ex_time = time.time() - start_time
    print "Execution time ",str(datetime.timedelta(seconds=ex_time))
