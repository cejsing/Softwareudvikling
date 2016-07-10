from django import forms
from django.forms import ModelForm
from polls.models import Pricesinevent, Wares, Events, Waregroups, Waresingroup
from polls.exceptions import Alreadymade, MyError


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    
    
class PriceForm(forms.Form):
    wareid = 0
    eventid = 0
    
    evprice = forms.IntegerField(label='Koster nu: ', required=False)


    def clean_evprice(self):
        price = self.cleaned_data['evprice']
        if (price == None):
            pass
        else:
            Pricesinevent.insert(self.wareid,self.eventid)
            Pricesinevent.setprice(self.wareid, self.eventid, price)
        
        
        
    def change_eventid(self, eventid):
        self.eventid = eventid
    
    def change_wareid(self, wareid):
        self.wareid = wareid
    
    def set_price(self):
        self.clean_evprice()
    


    
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
            

    
class WaregroupForm(forms.Form):    
    wgid = 0
    name = forms.CharField(label='Varegruppens nye navn: ', max_length=100, required=False)
    info = forms.CharField(label='Ny beskrivelse af varegruppe: ', max_length=100, required=False)
    
    def change_wgid(self, wgid):
        self.wgid = wgid
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if (name == None):
            pass
        elif (name == ""):
            pass
        else:
            if Waregroups.nameisavailable(name):
                Waregroups.setname(self.wgid, name)
            
    def change_waregroup(self):
        self.clean_name()
        self.clean_info()
        pass
            
        
    def clean_info(self):
        info = self.cleaned_data['info']
        if (info == None):
            pass
        else:
            Waregroups.setinfo(self.wgid, info)
    

#TODO: Make it work!
class WaregrouppriceForm(forms.Form):    
    wgid = 0
    price = forms.IntegerField(label='Ny standardpris', required=True)
    
    
    def change_wgid(self, wgid):
        self.wgid = wgid
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if (price == None):
            pass
        else:
            Ourwares = Waresingroup.getwares(self.wgid)
            for warerelation in Ourwares:
                Wares.setstandardprice(warerelation.ware.id, price)
                
                
#TODO: Make it work!
class GroupeventpriceForm(forms.Form):    
    wgid = 0
    eventid = 0
    price = forms.IntegerField(label='', required=False)
    
    
    def change_wgid(self, wgid):
        self.wgid = wgid

    def change_eventid(self, eventid):
        self.eventid = eventid
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if (price == None):
            print("no price for wg: " + str(self.wgid) + " and ev: " + str(self.eventid))
        else:
            if self.wgid == 0:
                raise MyError("wgid ikke initialiseret i form")
            elif self.eventid == 0:
                raise MyError("eventid ikke initialiseret i form")
            else:
                Ourwares = Waresingroup.getwares(self.wgid)
                for warerelation in Ourwares:
                        Pricesinevent.insert(warerelation.ware.id, self.eventid)
                        Pricesinevent.setprice(warerelation.ware.id, self.eventid, price)
