#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cafeen.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Wares, Waregroups, Events, Waresingroup, Pricesinevent, Extrafunctions, Waresnamehistory, Waresstdpricehistory, Waresinbarhistory, Waresinstockhistory, Waresdeletehistory, Wgnamehistory, Wginfohistory, Wgdeletehistory, Eventnamehistory, Eventinfohistory, Eventdeletehistory, WINcreatehistory, WINdeletehistory, PIEcreatehistory, PIEdeletehistory, Openandclose, PIEpricehistory

# Find out why these need to be imported but Noopeningsyet doesn't
from polls.exceptions import Alreadyclosed, Alreadyopen, Alreadymade


class WaresMethodTests(TestCase):
    
    def test_insertware(self):
        #Tests that a ware can be inserted with insert function
        Wares.insert("Carlsberg")
        self.assertEqual(len(Wares.objects.all().filter(warename="Carlsberg")) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(warename="Calrsberg")) == 1, False)
        Wares.insert("Tuborg")
        self.assertEqual(len(Wares.objects.all().filter(warename="Tuborg")) == 1, True)

    def test_setinbar(self): 
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.setwareinbar(1,5)
        Wares.setwareinbar(2,10)
        self.assertEqual(len(Wares.objects.all().filter(inbar=5)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(inbar=10)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(inbar=2)) == 2, False)

    def test_setinstockroom(self): 
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Wares.setwareinstockroom(1,5)
        Wares.setwareinstockroom(2,10)
        Wares.setwareinbar(3,20)
        self.assertEqual(len(Wares.objects.all().filter(instockroom=5)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(instockroom=10)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(instockroom=20)) == 1, False)
        self.assertEqual(len(Wares.objects.all().filter(instockroom=2)) == 2, False)
        
    def test_standardprice(self):
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Wares.setwareinbar(1,5)
        Wares.setwareinstockroom(1,5)
        Wares.setstandardprice(1,500) #Carlsberg er dyrt
        Wares.setstandardprice(2,50)
        Wares.setstandardprice(3,50) 
        self.assertEqual(len(Wares.objects.all().filter(standardprice=500)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(standardprice=50)) == 2, True)
        self.assertEqual(len(Wares.objects.all()) == 3, True)
        
    def test_removeware(self):
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        self.assertEqual(len(Wares.objects.all()) == 3, True)
        Wares.deletethis(1)
        self.assertEqual(len(Wares.objects.all()) == 2, True)
        Wares.insert("Carslberg")
        Wares.deletethis(4) 

    def test_getwaresforopening(self):
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        self.assertEqual(len(Wares.objects.all()) == 3, True)
        self.assertEqual(len(Wares.getopeningwares()) == 0, True)
        Wares.setwareinbar(1,1)
        self.assertEqual(len(Wares.getopeningwares()) == 1, True)
        Wares.setwareinstockroom(1,2)
        self.assertEqual(len(Wares.getopeningwares()) == 1, True)
        Wares.setwareinstockroom(2,2)
        self.assertEqual(len(Wares.getopeningwares()) == 2, True)
        
    def test_getstdprice(self): 
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.setwareinbar(1,5)
        Wares.setwareinbar(2,10)
        self.assertEqual(len(Wares.objects.all().filter(inbar=5)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(inbar=10)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(inbar=2)) == 2, False)
        Wares.setstandardprice(1,10)
        Wares.setstandardprice(2,30)
        self.assertEqual(Wares.getstdprice(1) == 10, True)
        self.assertEqual(Wares.getstdprice(1) == 30, False)
        self.assertEqual(Wares.getstdprice(2) == 30, True)

    def test_name_occupied(self):
        Wares.insert("Carlsberg")
        self.assertEqual(Wares.nameisavailable("Carlsberg"), False)
        self.assertEqual(Wares.nameisavailable("Tuborg"), True)
                
# All wareshis tests collected here
class WaresHistoriesMethodTests(TestCase):
    
    #Checks that only the correct calls increase elements in Waresnamehistory
    def test_Waresnamehistory1(self):
        self.assertEqual(len(Waresnamehistory.objects.all().filter(warename="Carlsberg")) == 0, True)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        self.assertEqual(len(Waresnamehistory.objects.all().filter(warename="Carlsberg")) == 1, True)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 7, True)
        Wares.setwarename(1, "Carlsberg xtreme")
        Wares.setwarename(7, "Tuborg guld")
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.getthis(1)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.getopeningwares()
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.getstdprice(1)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.setwareinbar(1,10)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.setwareinstockroom(2,300)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.setstandardprice(1,1)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresnamehistory.objects.all()) == 9, True)
        
    #Checks that elements are saved in Waresnamehistory in a meaningful way based on name and wareid
    #TODO: check for pubdate?
    def test_Waresnamehistory2(self):
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        self.assertEqual(len(Waresnamehistory.objects.all().filter(warename="Carlsberg")) == 1, True)
        self.assertEqual(len(Waresnamehistory.objects.all().filter(wareid=1)) == 1, True)
        Wares.setwarename(1, "Carlsberg xtreme")
        Wares.setwarename(7, "Tuborg guld")
        self.assertEqual(len(Waresnamehistory.objects.all().filter(wareid=1)) == 2, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresnamehistory.objects.all().filter(wareid=1)) == 2, True)    
        

    def test_Waresinbarhistory(self):
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")        
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.setwarename(1, "Carlsberg xtreme")
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.getthis(1)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.getopeningwares()
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.getstdprice(1)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 0, True)
        Wares.setwareinbar(1,10)
        Wares.setwareinbar(1,20)
        Wares.setwareinbar(2,11)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 3, True)
        Wares.setwareinstockroom(2,300)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 3, True)
        Wares.setstandardprice(1,1)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 3, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresinbarhistory.objects.all()) == 3, True)
        

    def test_Waresinstockhistory(self):
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")        
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.setwarename(1, "Carlsberg xtreme")
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.getthis(1)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.getopeningwares()
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.getstdprice(1)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.setwareinbar(1,10)
        Wares.setwareinbar(1,20)
        Wares.setwareinbar(2,11)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 0, True)
        Wares.setwareinstockroom(2,300)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 1, True)
        Wares.setstandardprice(1,1)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 1, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresinstockhistory.objects.all()) == 1, True)
        

    def test_Waresstdpricehistory(self):
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")        
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.setwarename(1, "Carlsberg xtreme")
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.getthis(1)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.getopeningwares()
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.getstdprice(1)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.setwareinbar(1,10)
        Wares.setwareinbar(1,20)
        Wares.setwareinbar(2,11)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.setwareinstockroom(2,300)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 0, True)
        Wares.setstandardprice(1,1)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 1, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresstdpricehistory.objects.all()) == 1, True)
    
    def test_Waresdeletehistory(self):
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        Wares.deletethis(1)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.setwarename(2, "Carlsberg xtreme")
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.getthis(2)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.getopeningwares()
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.getstdprice(2)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.setwareinbar(2,10)
        Wares.setwareinbar(2,20)
        Wares.setwareinbar(3,11)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.setwareinstockroom(3,300)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.setstandardprice(2,1)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 1, True)
        Wares.deletethis(5)
        self.assertEqual(len(Waresdeletehistory.objects.all()) == 2, True)
        
        

class WaregroupsHistoriesMethodTests(TestCase):
    
    def test_Waregroupsnamehistory(self):
        self.assertEqual(len(Wgnamehistory.objects.all()) == 0, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        Waregroups.insert("slik")
        Waregroups.insert("snack")
        Waregroups.insert("sodavand")
        Waregroups.insert("drikkevand")
        Waregroups.insert("sprut")
        self.assertEqual(len(Wgnamehistory.objects.all()) == 8, True)
        Waregroups.getthis(1)
        self.assertEqual(len(Wgnamehistory.objects.all()) == 8, True)
        Waregroups.setname(1,"kedelige øl")
        self.assertEqual(len(Wgnamehistory.objects.all()) == 9, True)
        Waregroups.setinfo(1,"de er faktisk lidt luksus")
        self.assertEqual(len(Wgnamehistory.objects.all()) == 9, True)
        Waregroups.deletethis(1)
        self.assertEqual(len(Wgnamehistory.objects.all()) == 9, True)
        Waregroups.deletethis(2)
        self.assertEqual(len(Wgnamehistory.objects.all()) == 9, True)
        Waregroups.deletethis(3)
        self.assertEqual(len(Wgnamehistory.objects.all()) == 9, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        self.assertEqual(len(Wgnamehistory.objects.all()) == 12, True)
        Waregroups.deletethis(11)
        self.assertEqual(len(Wgnamehistory.objects.all()) == 12, True)
        
        
    def test_Waregroupsinfohistory(self):
        self.assertEqual(len(Wginfohistory.objects.all()) == 0, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        Waregroups.insert("slik")
        Waregroups.insert("snack")
        Waregroups.insert("sodavand")
        Waregroups.insert("drikkevand")
        Waregroups.insert("sprut")
        self.assertEqual(len(Wginfohistory.objects.all()) == 0, True)
        Waregroups.getthis(1)
        self.assertEqual(len(Wginfohistory.objects.all()) == 0, True)
        Waregroups.setname(1,"kedelige øl")
        self.assertEqual(len(Wginfohistory.objects.all()) == 0, True)
        Waregroups.setinfo(1,"de er faktisk lidt luksus")
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
        Waregroups.deletethis(1)
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
        Waregroups.deletethis(2)
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
        Waregroups.deletethis(3)
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
        Waregroups.deletethis(11)
        self.assertEqual(len(Wginfohistory.objects.all()) == 1, True)
    
    def test_Waregroupsdeletehistory(self):
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 0, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        Waregroups.insert("slik")
        Waregroups.insert("snack")
        Waregroups.insert("sodavand")
        Waregroups.insert("drikkevand")
        Waregroups.insert("sprut")
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 0, True)
        Waregroups.getthis(1)
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 0, True)
        Waregroups.setname(1,"kedelige øl")
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 0, True)
        Waregroups.setinfo(1,"de er faktisk lidt luksus")
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 0, True)
        Waregroups.deletethis(1)
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 1, True)
        Waregroups.deletethis(2)
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 2, True)
        Waregroups.deletethis(3)
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 3, True)
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 3, True)
        Waregroups.deletethis(11)
        self.assertEqual(len(Wgdeletehistory.objects.all()) == 4, True)



class EventssHistoriesMethodTests(TestCase):
    
    def test_Eventsnamehistory(self):
        self.assertEqual(len(Eventnamehistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(Eventnamehistory.objects.all()) == 7, True)
        Events.setname(1,"blobdag")
        self.assertEqual(len(Eventnamehistory.objects.all()) == 8, True)
        Events.setinfo(1, "det er blobdag når man starter en ny uge")
        self.assertEqual(len(Eventnamehistory.objects.all()) == 8, True)
        Events.deletethis(1)
        self.assertEqual(len(Eventnamehistory.objects.all()) == 8, True)
        Events.insert("mandag")
        self.assertEqual(len(Eventnamehistory.objects.all()) == 9, True)

    def test_Eventsinfohistory(self):
        self.assertEqual(len(Eventinfohistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(Eventinfohistory.objects.all()) == 0, True)
        Events.setname(1,"blobdag")
        self.assertEqual(len(Eventinfohistory.objects.all()) == 0, True)
        Events.setinfo(1, "det er blobdag når man starter en ny uge")
        self.assertEqual(len(Eventinfohistory.objects.all()) == 1, True)
        Events.deletethis(1)
        self.assertEqual(len(Eventinfohistory.objects.all()) == 1, True)
        Events.insert("mandag")
        self.assertEqual(len(Eventinfohistory.objects.all()) == 1, True)
    
    def test_Eventsdeletehistory(self):
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 0, True)
        Events.setname(1,"blobdag")
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 0, True)
        Events.setinfo(1, "det er blobdag når man starter en ny uge")
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 0, True)
        Events.deletethis(1)
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 1, True)
        Events.insert("mandag")
        self.assertEqual(len(Eventdeletehistory.objects.all()) == 1, True)


#TODO: Consider if cascade-deletion is acceptable with this (yes?)
class WaresingroupsHistoriesMethodTests(TestCase):
    
    def test_Waresingroupcreatehistory(self):
        self.assertEqual(len(WINcreatehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        Waregroups.insert("slik")
        Waregroups.insert("snack")
        Waregroups.insert("sodavand")
        Waregroups.insert("drikkevand")
        Waregroups.insert("sprut")
        self.assertEqual(len(WINcreatehistory.objects.all()) == 0, True)
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(1,3)
        Waresingroup.insert(1,4)
        Waresingroup.insert(1,5)
        Waresingroup.insert(1,6)
        self.assertEqual(len(WINcreatehistory.objects.all()) == 6, True)
        Waresingroup.deletethis(1,6)
        self.assertEqual(len(WINcreatehistory.objects.all()) == 6, True)
        
    
    def test_Waresingroupdeletehistory(self):
        self.assertEqual(len(WINdeletehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        Waregroups.insert("luksusøl")
        Waregroups.insert("basisøl")
        Waregroups.insert("eksotiske øl")
        Waregroups.insert("slik")
        Waregroups.insert("snack")
        Waregroups.insert("sodavand")
        Waregroups.insert("drikkevand")
        Waregroups.insert("sprut")
        self.assertEqual(len(WINdeletehistory.objects.all()) == 0, True)
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(1,3)
        Waresingroup.insert(1,4)
        Waresingroup.insert(2,5)
        Waresingroup.insert(1,6)
        self.assertEqual(len(WINdeletehistory.objects.all()) == 4, True)
        Waresingroup.deletethis(1,6)
        self.assertEqual(len(WINdeletehistory.objects.all()) == 5, True)
        Wares.deletethis(1)
        self.assertEqual(len(WINdeletehistory.objects.all()) == 5, True)
        Wares.deletethis(2)
        # Shows that Wares.delethis() cascade effect does not register here
        self.assertEqual(len(WINdeletehistory.objects.all()) == 5, True)
        self.assertEqual(len(Waresingroup.objects.all()) == 0, True)
    
#TODO: Consider if cascade-deletion is acceptable with this (yes?)
class PricesineventsMethodTests(TestCase):
    
    def test_Pricesineventcreatehistory(self):
        self.assertEqual(len(PIEcreatehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        self.assertEqual(len(PIEcreatehistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(PIEcreatehistory.objects.all()) == 0, True)
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(1,4)
        Pricesinevent.insert(1,5)
        Pricesinevent.insert(1,6)
        Pricesinevent.insert(1,7)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(3,1)
        self.assertEqual(len(PIEcreatehistory.objects.all()) == 9, True)
        Pricesinevent.deletethis(1,1)
        Pricesinevent.deletethis(1,2)
        Pricesinevent.deletethis(2,1)
        self.assertEqual(len(PIEcreatehistory.objects.all()) == 9, True)


    def test_Pricesineventpricehistory(self):
        self.assertEqual(len(PIEpricehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        self.assertEqual(len(PIEpricehistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(PIEpricehistory.objects.all()) == 0, True)
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(1,4)
        Pricesinevent.insert(1,5)
        Pricesinevent.insert(1,6)
        Pricesinevent.insert(1,7)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(3,1)
        self.assertEqual(len(PIEpricehistory.objects.all()) == 0, True)
        Pricesinevent.setprice(1,1,1)
        Pricesinevent.setprice(1,1,2)
        Pricesinevent.setprice(1,1,2)
        Pricesinevent.setprice(1,2,10)
        Pricesinevent.setprice(1,3,100)
        Pricesinevent.setprice(1,4,-10)
        Pricesinevent.setprice(1,5,0)
        Pricesinevent.setprice(1,6,50)
        Pricesinevent.setprice(1,7,12)
        Pricesinevent.setprice(2,1,5)
        Pricesinevent.setprice(3,1,9)
        self.assertEqual(len(PIEpricehistory.objects.all()) == 11, True)
        Pricesinevent.deletethis(1,1)
        Pricesinevent.deletethis(1,2)
        Pricesinevent.deletethis(2,1)
        self.assertEqual(len(PIEpricehistory.objects.all()) == 11, True)
    
    def test_Pricesineventdeletehistory(self):
        self.assertEqual(len(PIEdeletehistory.objects.all()) == 0, True)
        Wares.insert("Carlsberg")
        try:
            Wares.insert("Carlsberg")
        except Alreadymade:
            pass        
        Wares.insert("Carlsberg Light")
        Wares.insert("Yankeebar")
        Wares.insert("Haribo Clickmix")
        Wares.insert("Mokai")
        Wares.insert("Heineken")
        Wares.insert("Tuborg")
        self.assertEqual(len(PIEdeletehistory.objects.all()) == 0, True)
        Events.insert("mandag")
        Events.insert("tirsdag")
        Events.insert("onsdag")
        Events.insert("torsdag")
        Events.insert("fredag")
        Events.insert("lørdag")
        Events.insert("søndag")
        self.assertEqual(len(PIEdeletehistory.objects.all()) == 0, True)
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(1,4)
        Pricesinevent.insert(1,5)
        Pricesinevent.insert(1,6)
        Pricesinevent.insert(1,7)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(3,1)
        self.assertEqual(len(PIEdeletehistory.objects.all()) == 0, True)
        Pricesinevent.deletethis(1,1)
        Pricesinevent.deletethis(1,2)
        Pricesinevent.deletethis(2,1)
        self.assertEqual(len(PIEdeletehistory.objects.all()) == 3, True)
    
    
class EventsMethodTests(TestCase):
    
    def test_insertevent(self):
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        self.assertEqual(len(Events.objects.all()) == 3, True)
        self.assertEqual(len(Events.objects.all().filter(eventname="Paaske")) == 1, True)

    def test_seteventname(self):
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        Events.setname(1,"merePaaske")
        self.assertEqual(len(Events.objects.all()) == 3, True)
        self.assertEqual(len(Events.objects.all().filter(eventname="Paaske")) == 1, False)
        self.assertEqual(len(Events.objects.all().filter(eventname="merePaaske")) == 1, True)
        
    def test_seteventinfo(self):
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        Events.setinfo(1,"Paaske skal have billige oeller")
        self.assertEqual(len(Events.objects.all()) == 3, True)
        self.assertEqual(len(Events.objects.all().filter(eventinfo="Paaske skal have billige oeller")) == 1, True)
        
    def test_removeevent(self):
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        self.assertEqual(len(Events.objects.all()) == 3, True)
        Events.deletethis(1)
        self.assertEqual(len(Events.objects.all()) == 2, True)

    def test_nameavailable(self):
        self.assertEqual(Events.nameisavailable("Paaske"), True)
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        self.assertEqual(Events.nameisavailable("Paaske"), False)
        self.assertEqual(Events.nameisavailable("frebar"), False)
        self.assertEqual(Events.nameisavailable("hverdag"), False)
        self.assertEqual(Events.nameisavailable("ikke brugt"), True)
        Events.deletethis(1)
        self.assertEqual(Events.nameisavailable("Paaske"), True)




class PricesineventMethodTests(TestCase):
    
    def test_insertpricing(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.setstandardprice(1,500) #Carlsberg er dyrt
        Wares.setstandardprice(2,50)
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(2,2)
        Pricesinevent.insert(2,3)
        self.assertEqual(len(Events.objects.all()) == 3, True)
        self.assertEqual(len(Pricesinevent.objects.all()) == 6, True)

    def test_setpricing(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.setstandardprice(1,500) #Carlsberg er dyrt
        Wares.setstandardprice(2,50)
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(2,2)
        Pricesinevent.insert(2,3)
        self.assertEqual(len(Events.objects.all()) == 3, True)
        self.assertEqual(len(Pricesinevent.objects.all()) == 6, True)
        self.assertEqual(len(Pricesinevent.objects.all().filter(price=-50)) == 0, True)
        Pricesinevent.setprice(1,1,-50)
        self.assertEqual(len(Pricesinevent.objects.all().filter(price=-50)) == 1, True)
        self.assertEqual(len(Pricesinevent.objects.all().filter(price=-50)) == 0, False)        
                
    def test_geteventprice(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.setstandardprice(1,500) #Carlsberg er dyrt
        Wares.setstandardprice(2,50)
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(2,2)
        Pricesinevent.insert(2,3)
        
        newprice = Pricesinevent.geteventprice(1,1)
        self.assertEqual(newprice==500, True)

        Pricesinevent.setprice(1,1,-50)
        
        newprice = Pricesinevent.geteventprice(1,1)
        self.assertEqual(newprice==500, False)
        self.assertEqual(newprice==450, True)
        
        Pricesinevent.setprice(1,1,-50)
        newprice = Pricesinevent.geteventprice(1,1)
        self.assertEqual(newprice==450, True)

        Pricesinevent.setprice(2,1,-50)
        newprice = Pricesinevent.geteventprice(2,1)
        self.assertEqual(newprice==0, True)

        Pricesinevent.setprice(2,1,-100)
        newprice = Pricesinevent.geteventprice(2,1)
        self.assertEqual(newprice==-50, True)
        
        
class WaregroupMethodTests(TestCase):
    
    def test_insertgroup(self):
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waregroups.insert("Snacks")
        Waregroups.insert("Slik")
        self.assertEqual(len(Waregroups.objects.all()) == 4, True)
        self.assertEqual(len(Waregroups.objects.all()) == 0, False)                
        self.assertEqual(len(Waregroups.objects.all()) == 3, False)
        self.assertEqual(len(Waregroups.objects.all()) == 5, False)
        self.assertEqual(len(Waregroups.objects.all().filter(wgname="Slik")) == 1, True)
    
    def test_setname(self):
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waregroups.insert("Snacks")
        Waregroups.insert("Slik")
        Waregroups.setname(1, "Nyeoeller")
        self.assertEqual(len(Waregroups.objects.all().filter(wgname="Nyeoeller")) == 1, True)
    
    def test_setinfo(self):
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waregroups.insert("Snacks")
        Waregroups.insert("Slik")
        Waregroups.setinfo(1, "De er ekstra gode")
        self.assertEqual(len(Waregroups.objects.all().filter(wginfo="")) == 3, True)
        self.assertEqual(len(Waregroups.objects.all().filter(wginfo="De er ekstra gode")) == 1, True)
        
    def test_removewg(self):
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waregroups.insert("Snacks")
        Waregroups.insert("Slik")
        self.assertEqual(len(Waregroups.objects.all()) == 4, True)
        Waregroups.deletethis(2)
        self.assertEqual(len(Waregroups.objects.all()) == 3, True)
        Waregroups.deletethis(4)
        self.assertEqual(len(Waregroups.objects.all()) == 2, True)
        
    def test_nameavailable(self):
        self.assertEqual(Waregroups.nameisavailable("Paaske"), True)
        Waregroups.insert("Paaske")
        Waregroups.insert("frebar")
        Waregroups.insert("hverdag")
        self.assertEqual(Waregroups.nameisavailable("Paaske"), False)
        self.assertEqual(Waregroups.nameisavailable("frebar"), False)
        self.assertEqual(Waregroups.nameisavailable("hverdag"), False)
        self.assertEqual(Waregroups.nameisavailable("ikke brugt"), True)        
        
        
#TODO: Find way to extract all wares for given waregroup
class WaresingroupMethodTests(TestCase):

    def test_insertgrouping(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        self.assertEqual(len(Wares.objects.all()) == 2, True)
        self.assertEqual(len(Waregroups.objects.all()) == 2, True)
        self.assertEqual(len(Waresingroup.objects.all()) == 2, True)
        
    def test_getwares(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        Waresingroup.insert(3,1)
        self.assertEqual(len(Waresingroup.getwares(1)) == 1, True)
        self.assertEqual(len(Waresingroup.getwares(2)) == 2, True)
    
    def test_getwaresingroup(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.insert("Tuborg2")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(3,1)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        self.assertEqual(len(Waresingroup.getwares(1)) == 1, True)
        self.assertEqual(len(Waresingroup.getwares(2)) == 2, True)

    def test_getthis(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        Waresingroup.insert(3,1)
        test1 = Waresingroup.getthis(1,2)
        self.assertEqual(test1.ware.warename == "Carlsberg", True)
        self.assertEqual(test1.waregroup.wgname == "Basisoeller", True)
        test2 = Waresingroup.getthis(3,1)
        self.assertEqual(test2.ware.warename == "Heineken", True)
        self.assertEqual(test2.waregroup.wgname == "Luxusoeller", True)
    
    def test_getgroupsforware(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.insert("Tuborg2")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(3,1)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        self.assertEqual(len(Waresingroup.getwaregroups(1)) == 1, True)
        self.assertEqual(len(Waresingroup.getwaregroups(2)) == 1, True)
        self.assertEqual(len(Waresingroup.getwaregroups(3)) == 1, True)

    
    def test_getwaregroups(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        Waresingroup.insert(3,1)
        self.assertEqual(len(Waresingroup.getwaregroups(1)) == 1, True)
        self.assertEqual(len(Waresingroup.getwaregroups(2)) == 1, True)
        
 
    def test_deleteonrelations1(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        self.assertEqual(len(Waresingroup.objects.all()) == 4, True)
        Wares.deletethis(1)
        self.assertEqual(len(Waresingroup.objects.all()) == 2, True)
        
    def test_deleteonrelations1(self):
        Wares.insert("Carlsberg")
        Wares.insert("Tuborg")
        Waregroups.insert("Luxusoeller")
        Waregroups.insert("Basisoeller")
        Waresingroup.insert(1,1)
        Waresingroup.insert(1,2)
        Waresingroup.insert(2,1)
        Waresingroup.insert(2,2)
        self.assertEqual(len(Waresingroup.objects.all()) == 2, True)
        Waregroups.deletethis(2)
        self.assertEqual(len(Waresingroup.objects.all()) == 0, True)


class openingsMethodTests(TestCase):
    
    def nothingdoneyet(self):
        try:
            Openandclose.isbaropen()
            whatisexpected = False
        except Noopeningsyet as e:
            whatisexpected = True
        self.assertEqual(whatisexpected, True)
        
    def somethingdone(self):    
        Openandclose.openbar()
        try:
            Openandclose.isbaropen()
            whatisexpected = False
        except Noopeningsyet as e:
            whatisexpected = True
        self.assertEqual(whatisexpected, False)
    
    def testraiseerrors(self):
        Events.insert("mandag")
        counter = 0
        Openandclose.openbar(1, "")
        Openandclose.closebar("")
        Openandclose.openbar(1, "")
        try:
            Openandclose.openbar(1, "")
        except Alreadyopen as e:
            counter += 1
        Openandclose.closebar("")
        try:
            Openandclose.closebar("")
        except Alreadyclosed as e:
            counter += 1
        self.assertEqual(counter == 2, True)
        self.assertEqual(len(Openandclose.objects.all()) == 4, True)    
        

class ExtrafunctionsMethodTest(TestCase):
    
    
    def test_getprice(self):
        Wares.insert("Carslberg")
        Wares.insert("Tuborg")
        Wares.insert("Heineken")
        Wares.setwareinbar(1,5)
        Wares.setwareinstockroom(1,5)
        Wares.setstandardprice(1,500) #Carlsberg er dyrt
        Wares.setstandardprice(2,50)
        Wares.setstandardprice(3,50) 
        self.assertEqual(len(Wares.objects.all().filter(standardprice=500)) == 1, True)
        self.assertEqual(len(Wares.objects.all().filter(standardprice=50)) == 2, True)
        self.assertEqual(len(Wares.objects.all()) == 3, True)
        Events.insert("Paaske")
        Events.insert("frebar")
        Events.insert("hverdag")
        Pricesinevent.insert(1,1)
        Pricesinevent.insert(1,2)
        Pricesinevent.insert(1,3)
        Pricesinevent.insert(2,1)
        Pricesinevent.insert(2,2)
        Pricesinevent.insert(2,3)
        Pricesinevent.setprice(1,1,-50)
        self.assertEqual(Extrafunctions.getprice(1,1) == 450, True)
        
        
