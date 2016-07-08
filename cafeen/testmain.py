#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafeen.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

from polls.models import Wares, Waregroups, Events, Waresingroup, Pricesinevent


#testWares = Wares(warename="den bedste øl")
#testWares.save()

#testWares = Wares(warename="den næstbedste øl", inbar=5, instockroom=1000)
#testWares.save()

#testWares = Wares(warename="den tredje-bedste øl", inbar=0)
#testWares.save()

#testWares = Wares(warename="den fjerde-bedste øl")
#testWares.save()

#testWares = Wares(warename="den femte-bedste øl")
#testWares.save()

#testWares = Wares(warename="den sjette-bedste øl")
#testWares.save()

#testWaregroups = Waregroups(wgname="øller")
#testWaregroups.save()

#testWaresingroups = Waresingroup(ware=testWares,waregroup=testWaregroups)
#testWaresingroups.save()

#print(Wares.objects.all())


#print(Wares.objects.all().filter(inbar=5))
#print(Wares.objects.all().exclude(inbar=5))



# Creates a new ware with 0 in stock and bar
def insertware(name):
    ware = Wares(warename=name)
    ware.save()

# Creates a new waregroup
def insertwaregroup(name):
    waregroup = Waregroups(wgname=name)
    waregroup.save()

# Creates a new event
def insertevent(name):
    event = Events(eventname=name)
    event.save()

# Changes the number of wares in the bar
def setwareinbar(wareid, numberofwares):    
    setwareanything("inbar", wareid, numberofwares)

# Changes the number of wares in the bar
def setwareinstockroom(wareid, numberofwares):    
    setwareanything("instockroom", wareid, numberofwares)

# Changes the name of a given ware       
def setwarename(wareid, newname):    
    setwareanything("warename", wareid, newname)

# Made for code reuse / 'superfunction'        
def setwareanything(function, wareid, changedvalue):    
    ourfilter = Wares.objects.all().filter(id=wareid)
    ourware = ourfilter[0] # Since there is only one object in the queryset
    if (function == "warename"): 
        ourware.warename = changedvalue
    elif (function == "instockroom"):
        ourware.instockroom = changedvalue
    elif (function == "inbar"):
        ourware.inbar = changedvalue
    else:
        # Simple raise exception untill we make something better
        print("error in setwareanything function-call")
    ourware.save()
    
    
#setwareinbar(1, 4)
#setwarename(1, "Tuborg super")
    
#print(Wares.objects.all().filter(inbar=5))
#ourware = Wares.objects.all().filter(id=1)
#for objekt in ourware:
    #objekt.inbar = 3
    #objekt.save()
print(Wares.objects.all().filter(inbar=4))
