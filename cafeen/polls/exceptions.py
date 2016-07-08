class MyError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value) 

class Noopeningsyet(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'you need to open the bar at least once' 


class Alreadyopen(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'the bar is already open' 


class Alreadymade(Exception):
     def __init__(self):
         return
     def __str__(self):
         return 'The same relation cannot be made twice' 


class Alreadyclosed(Exception):
    def __init__(self):
         return
    def __str__(self):
         return 'the bar is already closed' 
     
     
     
