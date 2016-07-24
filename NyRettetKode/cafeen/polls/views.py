from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

from django.views import generic
from django.views.generic.edit import FormView, CreateView, UpdateView

from polls.models import Wares, Waregroups, Events, Waresingroup, Pricesinevent, Waresnamehistory, Waresstdpricehistory, Waresinbarhistory, Waresinstockhistory, Openandclose, Refreshstock, Eventnamehistory, Eventinfohistory, Eventdeletehistory, Waresdeletehistory

from polls.exceptions import Noopeningsyet, MyError

from polls.forms import NameForm, PriceForm, WareForm, WaregroupForm, WaregrouppriceForm, GroupeventpriceForm

from django.template import Template, Context

#TODO: all: handle exceptions
#TODO: write "if request.POST:" in relevant places

#------------------Index of app

def index(request):
    allevents = Events.objects.all()
    allwares = Wares.objects.all()
    allwg = Waregroups.objects.all()
    template = loader.get_template('polls/index.html')
    context = {'allwares': allwares, 'allevents' : allevents, 'allwg': allwg}
    #output = ', '.join([q.warename for q in allwares])
    return render(request, 'polls/index.html', context)







#------------------- Handling of Wares

# Gives information on a given ware and makes it possible to change each instant
def detail(request, wares_id):
    ware = Wares.getthis(wares_id)
    waregroups = Waresingroup.getwaregroups(wares_id)
    try:
        waregroup = waregroups[0].waregroup
    except IndexError:
        waregroup = None
    if request.method == "POST":
        form = WareForm(request.POST)
        form.change_wareid(wares_id)
        #TODO: make redirect work so changes appear
        #return redirect(, {'form': form, 'ware':ware})
    else:
        form = WareForm()
        form.change_wareid(wares_id)
    return render(request, 'polls/detail.html', {'form': form, 'ware':ware, 'waregroup': waregroup})
    
#TODO: errorhandling if name taken    
#TODO: ask if other wares whould be made
#Creates a ware in the database
def createware(request):
    error = [] 
    if ('valgnavn' in request.POST): 
        newname = request.POST['valgnavn']
        if newname == "":
            error.append("Du skal vælge et navn")
        elif 'ja' in request.POST:
            Wares.insert(newname)
            ware = Wares.get_last()
            form = WareForm()
            Wares.insert(newname + " (åbnet vare)")
            #Sends user to details for ware
            return render(request, 'polls/detail.html', {'form': form,'ware':ware})

        else:
            Wares.insert(newname)
            ware = Wares.get_last()
            form = WareForm()
            #Sends user to details for ware
            return render(request, 'polls/detail.html', {'form': form, 'ware':ware})
    return render(request, 'polls/skab_vare.html', {'error': error})    
    
def waredelete(request, wares_id):
    ware = Wares.getthis(wares_id)
    message = []
    if "slet" in request.POST:
        Wares.deletethis(ware.id)
        message.append("Varen er nu slettet. Oplysninger om varen ligger stadigt gemt i historikken")
    return render(request, 'polls/slet_vare.html', {'message': message, 'ware': ware})
    
# Shows history of warenames    
def hisnavn(request):
    allwares = Waresnamehistory.objects.all()
    context = {'allwares': allwares,}
    template = loader.get_template('polls/hisnavn.html')
    return render(request, 'polls/hisnavn.html', context)    
    
    
#Describes changes to all wares (includes deletions)
def hisvareantal(request):
    allbar = Waresinbarhistory.objects.all()
    allstock = Waresinstockhistory.objects.all()
    alldeletes = Waresdeletehistory.objects.all()
    context = {'allbar':allbar, 'allstock': allstock, 'alldeletes': alldeletes}
    template = loader.get_template('polls/hisvareantal.html')
    return render(request, 'polls/hisvareantal.html', context)

#Describes changes to ware-prices    
def hisvarepriser(request):
    allwares = Waresstdpricehistory.objects.all() 
    context = {'allwares': allwares,}
    template = loader.get_template('polls/hisvarepriser.html')
    return render(request, 'polls/hisvarepriser.html', context)        
    
    
    
    
    
    


#-------------------- Handling of waregroups

# Gives information on a given ware and makes it possible to change each instant
def wgdetail(request, wg_id):
    waregroup = Waregroups.getthis(wg_id)
    varer = Waresingroup.getwares(wg_id)
    error = [] 
    if request.method == "POST":
        form = WaregroupForm(request.POST)
        form.change_wgid(wg_id)
        #TODO: make redirect work so changes appear
        #return redirect(, {'form': form, 'ware':ware})
    else:
        form = WaregroupForm()
        form.change_wgid(wg_id)
    return render(request, 'polls/wgdetail.html', {'form': form, 'waregroup': waregroup, 'varer': varer, 'error':error})    


#TODO: change from createware    
#TODO: errorhandling if name taken
def createwg(request):
    if ('valgnavn' in request.POST): 
        newname = request.POST['valgnavn']
        Waregroups.insert(newname)
        waregroup = Waregroups.get_last()
        form = WaregroupForm()
        #Sends user to details for ware
        return render(request, 'polls/wgdetail.html', {'form': form, 'waregroup':waregroup})
    return render(request, 'polls/skab_varegruppe.html')   

def waregroupdelete(request, wg_id):
    waregroup = Waregroups.getthis(wg_id)
    message = []
    if "slet" in request.POST:
        Waregroups.deletethis(waregroup.id)
        message.append("Varegrupen er nu slettet. Oplysninger om varegruppen ligger stadigt gemt i historikken")
    return render(request, 'polls/slet_varegruppe.html', {'message': message, 'waregroup': waregroup})
    

#TODO: make it work!
def wgpris(request, wg_id):
    waregroup = Waregroups.getthis(wg_id)
    varer = Waresingroup.getwares(wg_id)
    error = []
    if Openandclose.isbaropen():
        error.append("Man bør ikke ændre priser mens baren er åben")
    if request.method == "POST":
        form = WaregrouppriceForm(request.POST)
        form.change_wgid(wg_id)
        #TODO: make redirect work so changes appear
        #return redirect(, {'form': form, 'ware':ware})
    else:
        form = WaregrouppriceForm()
        form.change_wgid(wg_id)
    return render(request, 'polls/saetprisvaregruppe.html', {'form': form, 'waregroup': waregroup, 'varer': varer, 'error': error})    




#------------------------Handling of events

def createevent(request):
    if ('valgnavn' in request.POST): 
        newname = request.POST['valgnavn']
        Events.insert(newname)
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/skab_event.html')    


def events(request):
    allevents = Events.objects.all()
    if request.POST:
        if ('eventsubmit' in request.POST):
            if ('event' in request.POST):
                event = Events.getthis(int(request.POST['event']))
                #return redirect(request,  'polls/eventpriser.html', {'event': event})
                return render(request, 'polls/eventpriser.html', {'event': event})
            
    context = {'allevents': allevents,}
    
    return render(request, 'polls/events.html', context)

def eventdetail(request, event_id):
    event = Events.getthis(event_id)
    if ('valgnavn' in request.POST): 
        newname = request.POST['valgnavn']
        Events.setname(event.id, newname)
    else:
        pass
    if ('valginfo' in request.POST): 
        newinfo = request.POST['valginfo']
        Events.setinfo(event.id, newinfo)
    else:
        pass

    return render(request, 'polls/eventdetail.html', {'event': event})

#TODO: templates for deletemethods are almost identical as is the actual methods. Make codebase leaner later.    
def eventdelete(request, event_id):
    event = Events.getthis(event_id)
    message = []
    if "slet" in request.POST:
        Events.deletethis(event.id)
        message.append("Begivenheden er nu slettet. Oplysninger om begiveheden ligger stadigt gemt i historikken")
    return render(request, 'polls/slet_begivenhed.html', {'message': message, 'event': event})    
    
    


def eventhistory(request):
    alleventnames = Eventnamehistory.objects.all()
    alleventinfos = Eventinfohistory.objects.all()
    alleventdeletes = Eventdeletehistory.objects.all()
    
    context = {'alleventnames': alleventnames,'alleventinfos': alleventinfos,'alleventdeletes': alleventdeletes}
    
    return render(request, 'polls/hisbegivenhed.html', context)







#----------Handling of eventprices


# TODO: Make fixes similar to aaben and luk methods
def prisskift(request, event_id):
    
    event = Events.getthis(event_id)
    allwares = Wares.objects.all()
    inputlist = []
    #context = {'event': event}    
    if Openandclose.isbaropen():
        pass # TODO: errorhandling with page?
    else:
        for ware in allwares:
            if (str(ware.id) in request.POST):
                price = int(request.POST[str(ware.id)]) - ware.standardprice
                Pricesinevent.insert(ware.id,event_id)
                Pricesinevent.setprice(ware.id, event_id, price)
            
            else:
                pass
            inputlist.append((ware.warename, ware.id))
    context = {'event': event, 'inputlist': inputlist}    
    return render(request, 'polls/skiftpris.html', context)


def prislister(request, event_id):
    template = Template("")
    template.name = 'polls/priser.html'
    wares_list = Wares.objects.all()
    event = Events.getthis(event_id)
    groupedelements = []
    
    for ware in wares_list:
        price = Pricesinevent.geteventprice(ware.id, event_id)
        groupedelements.append([ware.warename, ware.id, ware.inbar, ware.instockroom, ware.standardprice, price])
        #template.render(context)
        #response.write("<P>" + ware.warename + str(price) + "</P>")

    context = {'event': event, 'groupedelements': groupedelements, 'wares_list': wares_list }        
    return render(request, template.name, context)

#Handles prices based on waregroups
def eventpriser(request, event_id):
    event = Events.getthis(event_id)
    allwaregroups = Waregroups.objects.all()
    inputlist = []
    message = []
    if Openandclose.isbaropen():
        message.append("baren er åben")
    else:
        for waregroup in allwaregroups:
            if request.POST:
                if (str(waregroup.id) in request.POST):
                    form = GroupeventpriceForm(request.POST)
                    form.change_wgid(waregroup.id)
                    form.change_eventid(event.id)
                else:
                    form = GroupeventpriceForm()
                    form.change_wgid(waregroup.id)
                    form.change_eventid(event.id)
            else:
                form = GroupeventpriceForm()
                form.change_wgid(waregroup.id)
                form.change_eventid(event.id)
            inputlist.append([form, waregroup.wgname, waregroup.id])
    
    context = {'event': event, 'inputlist': inputlist, 'allwaregroups':allwaregroups, 'message':message}    
    
    return render(request, 'polls/eventpriser.html', context)





#--------Day to day functions for the customer 
#--------Open, Close, Restock

#TODO: make sure that it is not possible to edit without editing all. This can be done by first running through all request.POSTs without editing. 
#TODO: make it possible to add an event to an opening and show prices for given event
def aaben(request, event_id):
    event = Events.getthis(event_id)
    message = []

    # Test if there is an open bar
    try:
        truthval = Openandclose.isbaropen()
    except Noopeningsyet:
        truthval = False
    
    # If the bar is open no wares will be displayed
    if (truthval):
        #TODO: make it distinct if there are no wares or bar is open
        allwares = Wares.objects.all().filter(id=0)
        eventpris = 0
        message.append("baren er allerede åben")
        context = {'allwares': allwares, 'event': event, 'eventpris': eventpris}
    else:
        allwares = Wares.getopeningwares()
    
    # TODO: consider if this can be removed
    if (len(allwares) == 0):
        eventpris = 0
        #context = {'allwares': allwares, 'event': event, 'eventpris': eventpris}
    
    #TODO: if the change may not commit unless all forms have been filled, it might be necessary to run through all wares once to test that things are in order
    else:
        for ware in allwares:
            try:
                eventpris = Pricesinevent.geteventprice(ware.id, event.id)
                valgbar = ware.inbar
                valglager = ware.instockroom
                if request.POST:
                    if ("valgbar." + str(ware.id)) in request.POST:
                        valgbar = request.POST["valgbar." + str(ware.id)]
                    else:
                        raise MyError("valgbar for #" + str(ware.id) + " gik galt")      
                    if ("valglager." + str(ware.id)) in request.POST:
                        valglager = request.POST['valglager.' + str(ware.id)]
                    else:
                        raise MyError("valglager for #" + str(ware.id) + " gik galt")
                    Wares.setwareinbar(ware.id, valgbar)
                    Wares.setwareinstockroom(ware.id, valglager)

            except KeyError: 
                message.append("aaben-metoden virker ikke. Tilkald udvikler")
            except ValueError:
                message.append(ware.warename + " blev ikke udfyldt")

        kommentar = ""
        if request.POST:
            if ("kommentar" in request.POST):
                kommentar = request.POST["kommentar"]
                Openandclose.openbar(event_id, kommentar)
            else:
                Openandclose.openbar(event_id, kommentar)
            message.append("Tillykke! Du har nu åbnet baren.")

    context = {'allwares': allwares, 'event': event, 'eventpris': eventpris, 'message': message}

    return render(request, 'polls/Aaben.html', context)

#TODO: make sure that it is not possible to edit without editing all. This can be  done by first running through all request.POSTs without editing.    

def luk(request):
    # Used for displaying information to user
    message = []
    
    # Test if there is an open bar
    if (not Openandclose.isbaropen()):
        allwares = Wares.objects.all().filter(id=0)
        message.append("baren er allerede lukket")
        
    else:
        allwares = Wares.getopeningwares()
        for ware in allwares:
            try:
                valgbar = ware.inbar
                valglager = ware.instockroom
                if request.POST:
                    if ("valgbar." + str(ware.id)) in request.POST:
                        valgbar = request.POST["valgbar." + str(ware.id)]
                    else:
                        raise MyError("valgbar for #" + str(ware.id) + " gik galt")      
                    if ("valglager." + str(ware.id)) in request.POST:
                        valglager = request.POST['valglager.' + str(ware.id)]
                    else:
                        raise MyError("valglager for #" + str(ware.id) + " gik galt")
                Wares.setwareinbar(ware.id, int(valgbar))
                Wares.setwareinstockroom(ware.id, int(valglager))
                
            except KeyError: 
                message.append("luk-metoden virker ikke. Tilkald udvikler")
                
                #return render(request, 'polls/Luk.html', context)
            except ValueError:
                message.append(ware.warename + " blev ikke udfyldt")
                #return render(request, 'polls/Luk.html', context)
        kommentar = ""
        if request.POST:
            if ("kommentar" in request.POST):
                kommentar = request.POST["kommentar"]
                Openandclose.closebar(kommentar)
            else:
                Openandclose.closebar(kommentar)
            message.append("Tillykke! Du har nu lukket baren.")
    context = {'allwares': allwares,'message':message}    
    return render(request, 'polls/Luk.html', context)


def aabenhistorik(request):
    allthings = Openandclose.objects.all()
    template = loader.get_template('polls/aabenhistorik.html')
    context = {'allthings': allthings}
    return render(request, 'polls/aabenhistorik.html', context)




#TODO: ^^ lav to tomme lister. tilføj tupler af wareid + int i try. derefter for-løkke af hver liste hvor ændringerne indsættes inden man så lukker.
#TODO: make it possible to restock take from aaben and luk    
def nymodtagelse(request):
    message = []
    try:
        truthval = Openandclose.isbaropen()
    except Noopeningsyet:
        truthval = False
        message.append("")
    if (truthval):
        #TODO: make it distinct if there are no wares or bar is open
        allwares = Wares.objects.all().filter(id=0)
        message.append("Varemodtagelse er ikke muligt med åben bar")
        context = {'allwares': allwares, 'message': message}
    else:
        allwares = Wares.objects.all()
        for ware in allwares:
            try:
                if request.POST:
                    valgbar = request.POST["valgbar." + str(ware.id)]
                    valglager = request.POST['valglager.' + str(ware.id)]
                    valgbar = int(valgbar) + ware.inbar
                    valglager = int(valglager) + ware.instockroom
                    Wares.setwareinbar(ware.id, valgbar)
                    Wares.setwareinstockroom(ware.id, valglager)
            except KeyError: 
                message.append("OBS: metoden virker ikke for " + ware.warename + "Tilkald udvikleren.")
                #return render(request, 'polls/modtagelser/ny.html', context)
            except ValueError:
                message.append("OBS: alt blev ikke udfyldt fra" + ware.warename)
                #return render(request, 'polls/modtagelser/ny.html', context)
        Refreshstock.insert()
        if request.POST:
            message.append("Ændringerne er nu foretaget")
    context = {'allwares': allwares, 'message': message}
    return render(request, 'polls/modtagelser/ny.html', context)


def modtagehistorik(request):
    allthings = Refreshstock.objects.all()
    context = {'allthings': allthings}

    return render(request, 'polls/modtagelser/historik.html', context)












#------------- Testing and junkcode



def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('')
    else:
        form = NameForm()
            
    return render(request, 'polls/test.html', {'form': form})
    

"""    

def prisskift(request, event_id):
    formtest = PriceForm(["300"])
    formtest.change_wareid(1)
    formtest.change_eventid(1)
    
    event = Events.getthis(event_id)
    allwares = Wares.objects.all()
    inputlist = []
    #context = {'event': event}    
    for ware in allwares:
        if (str(ware.id) in request.POST):
            form = PriceForm(request.POST[str(ware.id)])
            form.change_wareid(ware.id)
            form.change_eventid(event_id)
            #form.set_price()
            #Sends user to details for ware
            print(request.POST)

        else:
            print(request.POST)
            form = PriceForm()
            form.change_wareid(ware.id)
            form.change_eventid(event_id)
        inputlist.append((ware.warename, ware.id, form))
    context = {'event': event, 'inputlist': inputlist}    
    return render(request, 'polls/skiftpris.html', context)

"""
