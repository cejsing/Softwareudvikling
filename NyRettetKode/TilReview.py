
# Wares-klassen fra models.py
class Wares(models.Model):
    id = models.AutoField(primary_key=True)
    warename = models.CharField(max_length=200)
    inbar = models.IntegerField(default=0)
    instockroom = models.IntegerField(default=0)
    standardprice = models.IntegerField(default=0)

    # Makes object return the name, instead of 'OBJECT'
    def __str__(self):
        return self.warename

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

    def get_last():
        lastware = Wares.objects.latest('id')
        return lastware



# Fra views.py
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
        allwares = Wares.objects.all().filter(id=0)
        eventpris = 0
        message.append("baren er allerede åben")
        context = {'allwares': allwares, 'event': event, 'eventpris': eventpris}
    else:
        allwares = Wares.getopeningwares()

    if (len(allwares) == 0):
        eventpris = 0
        #context = {'allwares': allwares, 'event': event, 'eventpris': eventpris}

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


# Fra forms.py
class WareForm(forms.Form):
    wareid = 0
    name = forms.CharField(label='Varenavn', max_length=100, required=False)
    inbar = forms.IntegerField(label='Antal i bar', required=False)
    instock = forms.IntegerField(label='Antal på lager', required=False)
    price = forms.IntegerField(label='Standardpris (kr.)', required=False)
    waregroup = forms.ModelChoiceField(queryset=Waregroups.objects.all(), required=False, empty_label="Intet valgt", label="Varegruppe")

    def change_wareid(self, wareid):
        self.wareid = wareid

    def clean_name(self):
        name = self.cleaned_data['name']
        if (name == None):
            pass
        elif (name == ""):
            pass
        else:
            if Wares.nameisavailable(name):
                Wares.setwarename(self.wareid, name)

    def change_ware(self):
        self.clean_name()
        self.clean_inbar()
        self.clean_instock()
        self.clean_price()
        pass

    def clean_inbar(self):
        inbar = self.cleaned_data['inbar']
        if (inbar == None):
            pass
        else:
            Wares.setwareinbar(self.wareid, inbar)

    def clean_instock(self):
        instock = self.cleaned_data['instock']
        if (instock == None):
            pass
        else:
            Wares.setwareinstockroom(self.wareid, instock)

    def clean_price(self):
        price = self.cleaned_data['price']
        if (price == None):
            pass
        else:
            Wares.setstandardprice(self.wareid, price)

    def clean_waregroup(self):
        try:
            waregroupid = self.cleaned_data['waregroup'].id
            try:
                Waresingroup.insert(self.wareid, waregroupid)
            except Alreadymade:
                pass
        except AttributeError:
            pass