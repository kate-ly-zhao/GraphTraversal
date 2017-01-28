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

    # for testing
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

    ##########################
    # Construct the graph
    ##########################
    siteGraph = getGraph(siteConfig)    
    print(siteGraph)

   
    ##########################
    # Run the test
    ##########################
    runTest(siteConfig, siteGraph)



def runTest(siteConfig, siteGraph):
    "This function is designed to run the bandwidth loading tests"
    "Tests are 'hard' coded in place"

    #############################
    # Get all the loading senarios for Site to Prime test
   
    # First list a list of unique 'Site' numbers that are avaliable in the network
    uniqueSite = []
    for key in siteConfig:
        uniqueSite.append(siteConfig[key]["Site"])
        pass
    uniqueSite = list(set(uniqueSite))

    # for each site number, find all the Prime and GeoPrime sites
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

    # delete any site number that has not Prime or GeoPrime location
    # this is due to fact that 'Dispatch' locations have a site number designation of 0
    keysToDelete = []
    for key in uniquePrimeSite:
        print key, uniquePrimeSite[key], len(uniquePrimeSite[key])
        if(len(uniquePrimeSite[key]) == 0):
            keysToDelete.append(key)
            pass
        pass
    for key in keysToDelete:
        del uniquePrimeSite[key]

    # Debug Output
    print uniquePrimeSite

    # for each Prime/GeoPrime site, find all the loading senarios for SUT to PUT graphs
    # Store this information for later use
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


    ##################################
    # This is PUT to CUT loading senairo
    # Basic idea: create all combinations of Prime/GeoPrime at can be active for all site numbers
    # Similarly, create all combinations of core/DSR that can be active in a given zone
    # then compute the loading for all senarios

    # this is creating the correct input format for itertool to create the 
    # cartesian product of prime/GeoPrime sites
    primeSiteList = []
    for siteNum in uniquePrimeSite:
        primeSiteList.append(uniquePrimeSite[siteNum])
        pass

    # Debug output
    print primeSiteList
    activePrimeSiteCombinations = itertools.product(*primeSiteList)

    # first find the unique zones in the graph
    uniqueZone = []
    for key in siteConfig:
        uniqueZone.append(siteConfig[key]["Zone"])
        pass
    uniqueZone = list(set(uniqueZone))

    # for each zone, find the list of Cores/DSR cores
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

    # debug output
    print uniqueZoneSite

    # For each zone in the graph
    # loop over all Core/DSRCore
    # compute the loading for each Prime/GeoPrime senairo
    PUT_TO_CUT_loading = {}
    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            PUT_TO_CUT_loading[activeCore] = {}
            for currActivePrime in itertools.product(*primeSiteList):
                #print 'Running Loading', activeCore, currActivePrime
                PUT_TO_CUT_loading[activeCore][currActivePrime] = runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph)
                pass
            pass
        pass


    ##################################
    # This is DUT to CUT loading senairo
    # For each core, compute the loading senario for where all dispatch sites talk to an active core/DSR
    DUT_TO_CUT_loading = {}
    
    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            print "Testing active Core",activeCore
            DUT_TO_CUT_loading[activeCore] = runDispatchToCoreTest(activeCore, siteConfig, siteGraph)
            pass
        pass

    ######################################
    # TODO: Compute the GeoPrime -> Prime loading
    # TODO: Compute the DSR -> Core Loading
    # TODO: Sum all possible senarios and find the worst case loading for each node


    ########################################
    # Long term future list
    # GUI? :P


def runDispatchToCoreTest(activeCore, siteConfig, siteGraph):
    "This function computes the loading from all dispatch site in a zone to activeCore location"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

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

    # load the network for all dispatch to active core
    bwLoad = computeLoading(dispatchList, activeCore, bwLoad, 'Dispatch', siteConfig, siteGraph)
    
    return bwLoad


def runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph):
    " This function computes the loading for active prime/geoprime locations to active cores in a zone"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    bwLoad = computeLoading(currActivePrime, activeCore, bwLoad, 'Prime', siteConfig, siteGraph)
    return bwLoad



def runSubSiteToPrimeTest(primeSiteName, siteConfig, siteGraph):
    " This function computes the loading for active subsite locations to active primes in a site"    
    
    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

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

    bwLoad = computeLoading(subsiteList, primeSiteName, bwLoad, 'Subsite', siteConfig, siteGraph)
    return bwLoad


def computeLoading(fromSiteList, toSite, bwLoad, BandwidthOption, siteConfig, siteGraph):
    "This function computes the loading on the network, when all sites in the fromSiteList"
    "communicates to the toSite. The bandwidth for each site is choosen by the BandwidthOption input variable"

    # find the shortest path from each fromSite to toSite
    for fromSite in fromSiteList:
        #print 'Path from', fromSite, toSite
        pathList = siteGraph.find_shortest_path(fromSite, toSite)

        # if there is one path, pick that path, otherwise poll the user to pick one
        if(len(pathList) == 1):
            path = pathList[0]
        else:
            print pathList
            xString = input("Pick your path: ")
            x = int(xString)
            path = pathList[x]
            pass

        # for each edge in the path, load the line with the bandwidth 
        bwSite = siteConfig[fromSite]['Bandwidth'][BandwidthOption]
        for i in range(0, len(path)-1):
            bwLoad[path[i]][path[i+1]] += bwSite
            #print "loading", path[i], path[i+1], bwSite
            pass
        pass

    # print for debugging
    for key in siteConfig:
        for keyprime in siteConfig:
            if(bwLoad[key][keyprime] == 0):
                continue
            print key, keyprime, bwLoad[key][keyprime]
            pass
        pass
    return bwLoad


def getBwMap(siteConfig):
    "define the struture to store graph bandwidth loading"    
    bwLoad = {}
    for key in siteConfig:
        bwLoad[key] = {}
        for keyprime in siteConfig:
            bwLoad[key][keyprime] = 0
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
