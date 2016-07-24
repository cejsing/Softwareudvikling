class MyError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value) 

class Noopeningsyet(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'Baren skal åbnes'


class Alreadyopen(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'Baren er allerede åben'


class Alreadymade(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'Denne relation eksisterer allerede'


class Alreadyclosed(Exception):
    def __init__(self):
         return
    def __str__(self):
         return 'Baren er allerede lukket'
     
     
     
