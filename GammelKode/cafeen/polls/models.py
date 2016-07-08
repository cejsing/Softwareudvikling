"""
This is where the functions are written, and classes are deffind.

Acronyms
WIN = WareInGroups
PIE = Price In Event

Remember to comment in code what your line does!
"""

# Import relevant packages.

from django.db import models
from django.db.models import Q
from django.utils import timezone
from polls.exceptions import Alreadyopen, Alreadyclosed, Noopeningsyet, Alreadymade
from django.core.urlresolvers import reverse


#TODO: for all: deletion, checks?
#TODO: for all histories: make getthis-functions?

#Only added for testing purposes
class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('test2', kwargs={'pk': self.pk})



# ------------------------- FUNCTIONS RELATED TO WARES -------------------------

# Making class
class Wares(models.Model):
    id = models.AutoField(primary_key=True)
    warename = models.CharField(max_length=200)
    inbar = models.IntegerField(default=0)
    instockroom = models.IntegerField(default=0)
    standardprice = models.IntegerField(default=0)
    
    # Makes object return the name, instead of 'OBJECT'
    def __str__(self):
        return self.warename
    
    
    #def get_absolute_url(self):
        #return reverse('detail', kwargs={'pk': self.pk})
    
    
    # ------------------------- functions related to Making a Ware
    # Inserting and saving a Ware    
    def insert(name):
        if (Wares.nameisavailable(name)):
            ware = Wares(warename=name)
            ware.save()
            Waresnamehistory.insert(ware.id)
        else:
            raise Alreadymade

    # Makes sure the name is not in use        
    def nameisavailable(name):
        ourfilter = Wares.objects.all().filter(warename=name)
        isavailable = len(ourfilter) == 0
        return isavailable
    
    # Search by WareID
    def getthis(wareid):
        ourfilter = Wares.objects.all().filter(id=wareid)
        ourware = ourfilter[0] # Since there is only one object in the queryset
        return ourware
    
    # ------------------------- functions related to Opening    
    # TODO: Q for åbnet vare should only matter if either it or the previous ware contains anything
    def getopeningwares():
        ourfilter = Wares.objects.all().filter(Q(instockroom__gt=0) | Q(inbar__gt=0) | Q(warename__contains=" (åbnet vare)"))
        return ourfilter
    
    def getstdprice(wareid):
        ourware = Wares.getthis(wareid)
        return ourware.standardprice
        
    # ------------------------- functions related to changing a Ware
    # Changes the number of wares in the bar    
    def setwareinbar(wareid, numberofwares):    
        ourware = Wares.getthis(wareid)
        ourware.inbar = numberofwares
        ourware.save()
        Waresinbarhistory.insert(wareid)
        
    # Changes the number of wares in the stockroom    
    def setwareinstockroom(wareid, numberofwares):    
        ourware = Wares.getthis(wareid)
        ourware.instockroom = numberofwares
        ourware.save()
        Waresinstockhistory.insert(wareid)
        
    # Changes the name of a given ware       
    def setwarename(wareid, newname):    
        if (Wares.nameisavailable(newname)):
            ourware = Wares.getthis(wareid)
            ourware.warename = newname
            ourware.save()
            Waresnamehistory.insert(wareid)
        else:
            raise Alreadymade
        
    #Changes the standard price used for calculating eventprices    
    def setstandardprice(wareid, newprice):
        ourware = Wares.getthis(wareid)
        ourware.standardprice = newprice
        ourware.save()
        Waresstdpricehistory.insert(wareid)
        
    #Removes a ware from the database given unique identifier    
    def deletethis(wareid):
        ourware = Wares.getthis(wareid)
        Waresdeletehistory.insert(wareid)
        ourware.delete()
        
    #TODO: test    
    def get_last():
        lastware = Wares.objects.latest('id')
        return lastware


# ------------------------- functions related making Ware History

# Name History
class Waresnamehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    warename = models.CharField(max_length=200)

    def __str__(self):
        information = "ID: " + str(self.wareid) + " now has the name ' " + self.warename + "'"
        return information
    
    def insert(warid):
        warehis = Waresnamehistory()
        ware = Wares.getthis(warid)
        
        warehis.wareid = ware.id
        warehis.warename = ware.warename
        warehis.save()
        
    #TODO: make tests    
    def getinbetweendates(datefrom,dateto):
        ourfilter = Waresnamehistory.objects.all().filter(pub_date__gt=datefrom).filter(pub_date__lt=dateto)
        return ourfilter
        

# Numbers in Bar history        
class Waresinbarhistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    inbar = models.IntegerField(default=0)
    
    def __str__(self):
        information = "ID: " + str(self.wareid) + " now has " + str(self.inbar) + " in the bar"
        return information
    
    def insert(warid):
        ware = Wares.getthis(warid)
        warehis = Waresinbarhistory()
        
        warehis.wareid = warid
        warehis.inbar = ware.inbar
        warehis.save()        


# Numbers in stock History
class Waresinstockhistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    instockroom = models.IntegerField(default=0)
    
    # Makes object return a string, instead of 'OBJECT'
    def __str__(self):
        return "Ware with id#: " + str(wareid) + " has " + str(instockroom) + " in stock"

    
    def insert(warid):
        ware = Wares.getthis(warid)
        warehis = Waresinstockhistory()
        
        warehis.wareid = warid
        warehis.instockroom = ware.instockroom
        warehis.save()  
        
        
# Standardprice History
class Waresstdpricehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    standardprice = models.IntegerField(default=0)
    
    def __str__(self):
        information = "ID: " + str(self.wareid) + " is now priced at " + str(self.standardprice)
        return information
    
    
    def insert(warid):
        ware = Wares.getthis(warid)
        warehis = Waresstdpricehistory()
        
        warehis.wareid = warid
        warehis.standardprice = ware.standardprice
        warehis.save()          

# Deleted wares History
class Waresdeletehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    

    # Makes object return a string, instead of 'OBJECT'
    def __str__(self):
        return "Ware with id#: " + str(wareid) + " deleted"

    def insert(warid):
        ware = Wares.getthis(warid)
        warehis = Waresdeletehistory()
        
        warehis.wareid = warid
        warehis.save()


# ------------------------- FUNCTIONS RELATED TO WARE GROUPS -------------------------

class Waregroups(models.Model):
    id = models.AutoField(primary_key=True)
    wgname = models.CharField(max_length=200)
    wginfo = models.CharField(max_length=200)

    # Returns the given name instead of object
    def __str__(self):
        return self.wgname
    
    def getthis(wgid):
        ourfilter = Waregroups.objects.all().filter(id=wgid)
        ourwg = ourfilter[0] # Since there is only one object in the queryset
        return ourwg
    
    # ------------------------- functions related to changing a WareGroup
    # Inserting and saving name
    def insert(name):
        if (Waregroups.nameisavailable(name)):
            waregroup = Waregroups(wgname=name)
            waregroup.save()
            Wgnamehistory.insert(waregroup.id)
        else:
            raise Alreadymade
    
    # Makes sure name is not in use already
    def nameisavailable(name):
        ourfilter = Waregroups.objects.all().filter(wgname=name)
        isavailable = len(ourfilter) == 0
        return isavailable        
    
    # ------------------------- functions related to changing a WareGroup
    # Changes the name of the waregroup while keeping relations 
    def setname(wgid, newname):
        if (Waregroups.nameisavailable(newname)):
            ourwg = Waregroups.getthis(wgid)
            ourwg.wgname = newname
            ourwg.save()
            Wgnamehistory.insert(wgid)
        else:
            raise Alreadymade
        
        
    # Changes the info of the waregroup while keeping relations    
    def setinfo(wgid, newinfo):
        ourwg = Waregroups.getthis(wgid)
        ourwg.wginfo = newinfo
        ourwg.save()
        Wginfohistory.insert(wgid)

    # Removes a waregroup from the database given unique identifier    
    def deletethis(wgid):
        ourwg = Waregroups.getthis(wgid)
        Wgdeletehistory.insert(wgid)
        ourwg.delete()
        
    #TODO: test  
    # Finds the waregroup that was created last
    def get_last():
        lastware = Waregroups.objects.latest('id')
        return lastware    
        
# ------------------------- functions related making WareGroup History
# Name History        
class Wgnamehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wgid = models.IntegerField(default=0)
    wgname = models.CharField(max_length=200)

    
    def insert(wargid):
        wghis = Wgnamehistory()
        waregroup = Waregroups.getthis(wargid)
        
        wghis.wgid = waregroup.id
        wghis.warename = waregroup.wgname
        wghis.save()
 
# Info History 
class Wginfohistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wgid = models.IntegerField(default=0)
    wginfo = models.CharField(max_length=200)

    def insert(wargid):
        wghis = Wginfohistory()
        waregroup = Waregroups.getthis(wargid)
        
        wghis.wgid = waregroup.id
        wghis.wginfo = waregroup.wginfo
        wghis.save()        

# Deletion History
class Wgdeletehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wgid = models.IntegerField(default=0)
    
    def insert(wargid):
        wghis = Wgdeletehistory()
        waregroup = Waregroups.getthis(wargid)
        
        wghis.wgid = waregroup.id
        wghis.save()    



# ------------------------- FUNCTIONS RELATED TO EVENTS -------------------------
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    eventname = models.CharField(max_length=200)
    eventinfo = models.CharField(max_length=200)
    
    # Return the events name instead of "Object"
    def __str__(self):
        return self.eventname
    
    # Search by EventID
    def getthis(eventid):
        ourfilter = Events.objects.all().filter(id=eventid)
        ourevent = ourfilter[0] # Since there is only one object in the queryset
        return ourevent
    
    
    # ------------------------- Functions related to making an event
    # Insert and save a new event
    def insert(name):
        if (Events.nameisavailable(name)):
            event = Events(eventname=name)
            event.save()
            Eventnamehistory.insert(event.id)
        else:
            raise Alreadymade
       
    # Makes sure that a name is unused   
    def nameisavailable(name):
        ourfilter = Events.objects.all().filter(eventname=name)
        isavailable = len(ourfilter) == 0
        return isavailable     

    # Changes the name of the event while keeping relations  
    def setname(eventid, newname):
        if (Events.nameisavailable(newname)):
            ourevent = Events.getthis(eventid)
            ourevent.eventname = newname
            ourevent.save()
            Eventnamehistory.insert(eventid)
        else:
            raise Alreadymade
    
    # Changes the info of the Event while keeping relations    
    def setinfo(eventid, newinfo):
        ourevent = Events.getthis(eventid)
        ourevent.eventinfo = newinfo
        ourevent.save()
        Eventinfohistory.insert(eventid)
        
        
    #Removes an event from the database given unique identifier    
    def deletethis(eventid):
        ourevent = Events.getthis(eventid)        
        Eventdeletehistory.insert(eventid)
        ourevent.delete()
        
# ------------------------- functions related to making Event History
# Name History        
class Eventnamehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    eventid = models.IntegerField(default=0)
    eventname = models.CharField(max_length=200)
    
    def insert(evid):
        eventhis = Eventnamehistory()
        event = Events.getthis(evid)
        
        eventhis.eventid = event.id
        eventhis.eventname = event.eventname
        eventhis.save()


# Info History                        
class Eventinfohistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    eventid = models.IntegerField(default=0)
    eventinfo = models.CharField(max_length=200)

    def insert(evid):
        eventhis = Eventinfohistory()
        event = Events.getthis(evid)
        
        eventhis.eventid = event.id
        eventhis.eventinfo = event.eventinfo
        eventhis.save()        

# Deletion History
class Eventdeletehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    eventid = models.IntegerField(default=0)
    
    def insert(evid):
        eventhis = Eventdeletehistory()
        event = Events.getthis(evid)
        
        eventhis.eventid = event.id
        eventhis.save()       




# ------------------------- FUNCTIONS RELATED TO RELATIONS -------------------------

# Defines the relation between Wares and Waregroups
class Waresingroup(models.Model):
    ware = models.ForeignKey("Wares", on_delete=models.CASCADE)
    waregroup = models.ForeignKey("Waregroups", on_delete=models.CASCADE)
    
    def __str__(self):
        return "ware id: " + str(self.ware.id) + " with warename: " + self.ware.warename + " and waregroup-id: " +  str(self.waregroup.id) + " with groupname: " + self.waregroup.wgname

    # else should be a raise exception
    def insert(wareid,wgid):
        if (Waresingroup.relationnotmade(wareid,wgid)):
            #Next three lines make certain that only one waregroup exists per ware
            earlier_relations = Waresingroup.getwaregroups(wareid)    
            for relation in earlier_relations:
                Waresingroup.deletethis(relation.ware.id, relation.waregroup.id)
            
            ourware = Wares.getthis(wareid)
            ourwg = Waregroups.getthis(wgid)
            wareingroup = Waresingroup(ware=ourware,waregroup=ourwg)
            wareingroup.save()
            WINcreatehistory.insert(wareid,wgid)
        else:
            raise Alreadymade
    
    def relationnotmade(wareid, wgid):
        ourfilter = Waresingroup.objects.all().filter(ware__id=wareid).filter(waregroup__id=wgid)
        doesnotexist = len(ourfilter) == 0
        return doesnotexist
        
    #TODO: make testcases    
    def getthis(wareid, wgid):
        ourfilter = Waresingroup.objects.all().filter(ware__id=wareid).filter(waregroup__id=wgid) 
        ourrelation = ourfilter[0] # Since there is only one object in the queryset
        return ourrelation

    def getwares(wgid):
        ourfilter = Waresingroup.objects.all().filter(waregroup__id=wgid)
        return ourfilter

    def getwaregroups(wareid):
        ourfilter = Waresingroup.objects.all().filter(ware__id=wareid)
        return ourfilter
    
    #TODO: make testcases
    def deletethis(wareid, wgid):
        ourrelation = Waresingroup.getthis(wareid, wgid)
        WINdeletehistory.insert(wareid, wgid)
        ourrelation.delete()

#WIN = Waresingroup
class WINcreatehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    wgid = models.IntegerField(default=0)
    
    def insert(warid, wargid):
        WINhis = WINcreatehistory()
        
        WINhis.wareid = warid
        WINhis.wgid = wargid
        WINhis.save()

#WIN = Waresingroup
#cascade will remove elements without this activating
class WINdeletehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    wgid = models.IntegerField(default=0)
    
    def insert(warid, wargid):
        WINhis = WINdeletehistory()
        
        WINhis.wareid = warid
        WINhis.wgid = wargid
        WINhis.save()     





class Pricesinevent(models.Model):
    ware = models.ForeignKey("Wares", on_delete=models.CASCADE)
    event = models.ForeignKey("Events", on_delete=models.CASCADE)    
    price = models.IntegerField(default=0) #This represents the difference to the standardprice  

    def __str__(self):
        return "ware id: " + str(self.ware.id) + " with warename: " + self.ware.warename + " and event-id: " +  str(self.event.id) + " with name: " + self.event.eventname + " and price: " + str(self.price)
    
    #else should raise exception
    def insert(wareid,eventid):
        if (Pricesinevent.relationnotmade(wareid,eventid)):
            try:
                ourfilter1 = Wares.objects.all().filter(id=wareid)
                ourware = ourfilter1[0] # Since there is only one object in the queryset
            except IndexError:
                print("wareid does not exist: " + str(wareid))
                return
            try:
                ourfilter2 = Events.objects.all().filter(id=eventid)
                ourevent = ourfilter2[0]
            except IndexError:
                print("event does not exist: " + str(eventid))
                return
            priceinevent = Pricesinevent(ware=ourware,event=ourevent)
            priceinevent.save()
            PIEcreatehistory.insert(wareid, eventid)
        else:
            return
    
    #TODO: make testcases    
    def getthis(wareid, eventid):
        ourfilter = Pricesinevent.objects.all().filter(ware__id=wareid).filter(event__id=eventid) 
        ourrelation = ourfilter[0] # Since there is only one object in the queryset
        return ourrelation
        
    
    def relationnotmade(wareid, eventid):
        ourfilter = Pricesinevent.objects.all().filter(ware__id=wareid).filter(event__id=eventid)
        doesnotexist = len(ourfilter) == 0
        return doesnotexist
        
    def getthis(wareid, eventid):
        ourfilter = Pricesinevent.objects.all().filter(ware__id=wareid).filter(event__id=eventid) 
        ourevent = ourfilter[0] # Since there is only one object in the queryset
        return ourevent
        
    def setprice(wareid, eventid, newprice):
        ourevent = Pricesinevent.getthis(wareid, eventid)
        ourevent.price = newprice
        ourevent.save()
        PIEpricehistory.insert(wareid, eventid, newprice)
        
    def geteventprice(wareid, eventid):
        try:
            ourevent = Pricesinevent.getthis(wareid, eventid)
        except IndexError:
            ware = Wares.getthis(wareid)
            return ware.standardprice
        eventdiff = ourevent.price
        baseprice = ourevent.ware.standardprice
        return eventdiff + baseprice
    
    def deletethis(wareid,eventid):
        ourrelation = Pricesinevent.getthis(wareid, eventid)
        PIEdeletehistory.insert(wareid, eventid)
        ourrelation.delete()


#PIE = Pricesinevent
class PIEcreatehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    eventid = models.IntegerField(default=0)
    
    def insert(warid, evid):
        PIEhis = PIEcreatehistory()
        
        PIEhis.wareid = warid
        PIEhis.eventid = evid
        PIEhis.save()

#PIE = Pricesinevent
#cascade will remove elements without this activating
class PIEdeletehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    eventid = models.IntegerField(default=0)
    
    def insert(warid, evid):
        PIEhis = PIEdeletehistory()
        
        PIEhis.wareid = warid
        PIEhis.eventid = evid
        PIEhis.save()

#PIE = Pricesinevent
class PIEpricehistory(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)
    wareid = models.IntegerField(default=0)
    eventid = models.IntegerField(default=0)
    price = models.IntegerField()
    
    def insert(warid, evid, newprice):
        PIEhis = PIEpricehistory()
        
        PIEhis.wareid = warid
        PIEhis.eventid = evid
        PIEhis.price = newprice
        PIEhis.save()
        
#TODO: test
class Openandclose(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey("Events")    
    pub_date = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=500, default="")
    opennow = models.BooleanField() 
    
    
    def __str__(self):
        if self.opennow:
            return "åbnet"
        else:
            return "lukket"
    
    def insert(openorclosed, eventid, kommentar):
        nowopen = Openandclose(opennow = openorclosed, event = Events.getthis(eventid), comments=kommentar)
        nowopen.save()
    
    def getlast():
        lastopenclose = Openandclose.objects.latest('pub_date')
        return lastopenclose
    
    #Opens the bar unless it is already open
    def openbar(eventid, kommentar):
        if (len(Openandclose.objects.all()) > 0):
            if (Openandclose.getlast().opennow):
                raise Alreadyopen
            else:
                opening = True
                Openandclose.insert(opening, eventid, kommentar)
        else:
            opening = True
            Openandclose.insert(opening, eventid, kommentar)
            
    #Closes the bar unless it is already closed
    def closebar(kommentar):
        if (len(Openandclose.objects.all()) > 0):
            lastopenclose = Openandclose.getlast()
            if (lastopenclose.opennow):
                opening = False
                eventid = lastopenclose.event.id
                Openandclose.insert(opening, eventid, kommentar)
            else:
                raise Alreadyclosed
        else:
            raise Noopeningsyet

    def isbaropen():
        if (len(Openandclose.objects.all()) > 0):
            isopen = Openandclose.getlast().opennow
            return isopen
        else:
            raise Noopeningsyet

#TODO: test __str__ amd insert
class Refreshstock(models.Model):
    id = models.AutoField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "opfyldt" #+ str(pub_date)
    
    def insert():
        if (Openandclose.isbaropen()):
            raise Alreadyopen
        else:
            stock = Refreshstock()
            stock.save()
            
            
"""
User rights defined by following ints:
1 = may open and close bar
2 = may edit names of wares, waregroups and events
4 = may restock
8 = user admin
"""        
#TODO: make error AccessDenied
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    rights = models.IntegerField(default=0) 

    def __str__(self):
        return self.username
    
    def set_name(self, newname):
        self.username = newname
    
    def insert(newname):
        user = User()
        user.set_name(newname)
        user.save()
    
    def getthis(userid):
        user = User.objects.all().filter(id=userid)
        return user
    
    def allowed_openandclose(self):
        if self.rights == 1:
            return True
        elif self.rights == 3:
            return True
        elif self.rights == 5:
            return True
        elif self.rights == 7:
            return True
        elif self.rights == 9: 
            return True
        elif self.rights == 11:
            return True     
        elif self.rights == 13:
            return True
        elif self.rights == 15:
            return True
        else:
            return False
    
    def allow_openandclose(self, userid):    
        if self.allowed_admin():
            user = User.getthis(userid)
            if user.allowed_openandclose():
                pass
            else:
                user.rights = user.rights + 1
        else:
            pass
                
        
    def deny_openclose(self, userid):
        if self.allowed_admin():
            user = User.getthis(userid)
            if user.allowed_openandclose():
                user.rights = user.rights - 1
            else:
                pass
        else:
            pass
        
    def allowed_editnames(self):
        if self.rights == 2:
            return True
        elif self.rights == 3:
            return True
        elif self.rights == 6: 
            return True
        elif self.rights == 7: 
            return True
        elif self.rights == 10: 
            return True
        elif self.rights == 11:
            return True     
        elif self.rights == 14:
            return True
        elif self.rights == 15:
            return True
        else:
            return False
        
    def allow_editnames(self, userid):
        if self.allowed_admin():
            user = User.getthis(userid)
            if user.allowed_editnames():
                pass
            else:
                user.rights = user.rights + 2
        else:
            pass
            
    def deny_openclose(self, userid):
        if self.allowed_admin():
            user = User.getthis(userid)
            if user.allowed_openandclose():
                user.rights = user.rights - 2
            else:
                pass
        else:
            pass
        
    def allowed_admin(self):
        if self.rights == 8:
            return True
        elif self.rights == 9:
            return True
        elif self.rights == 10:
            return True
        elif self.rights == 11:
            return True
        elif self.rights == 12: 
            return True
        elif self.rights == 13:
            return True     
        elif self.rights == 14:
            return True
        elif self.rights == 15:
            return True
        else:
            return False
    
    
        
#TODO: consider if geteventprice should be used instead of getprice   
class Extrafunctions():
    
    barisopen = False
    
    def getprice(wareid, eventid):
        std = Wares.getstdprice(wareid)
        diff = Pricesinevent.geteventprice(wareid, eventid)
        return diff #+ std

    #TODO: make function
    #TODO: place in forms?
    #TODO: handle opening an open bar
    #def openbar(eventid):
        #if(Extrafunctions.barisopen)
            #print("error in openbar")
        #else
            #return eventid
    
    
    
    
    
