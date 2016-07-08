# Skeleton-structure of backendfunctions. Many functions have similar needs, so further subfunctions might be made later to avoid redundant code.

#  Used for including new ware to database. Only name is given on initiation. All other information added by other funtions
def insertware (warename):
  return 0

# Changes the name of a ware for a given ID
def changewarename(wareID, warename):
  return 0
    
# Used for updating stock
def changenumberinbar(wareID, inbar):
  return 0
    
# Used for updating stock 
def changenumberinstockroom(wareID, instock):
  return 0

    

# Find ware based on name
def selectware(warename):
  return 0
    
# Finds ware based on ID
def selectware(wareID):
  return 0


# Creates new group. Description can be empty?
def insertwaregroup(groupname, groupdescription):
  return 0
    
# Changes the name of a group for a given ID
def changegroupname(groupID, goupname):
  return 0
    
# Changes the description of a group for a given ID
def changegroupdescription(groupID, groupdescription):
  return 0


# Finds group based on name
def selectgroup(groupname):
  return 0

# Finds group based on ID   
def selectgroup(groupID):
  return 0


# Couples wares and groups.
def putwareingroup(wareID, groupID):
  return 0

# Finds all wares within a group and returns them. Group found via ID   
def selectgroupswares(groupID):
  return 0

# Finds all wares within a group and returns them 
def selectgroupswares(groupname):
  return 0

    
# Events are used for determinig prices of a ware.
def insertevent(eventname):
  return 0

    
# Gives the option of making more reasonable names for events
def changeeventname(eventID, eventname):
  return 0
    

# Makes a price for a given event for at given ware
def setprice(wareID, eventID, price):
  return 0


# Deletes a ware from the list (and all references?)
def removeware(wareID):   
    return 0

# Deletes group and all references in wares/group relation
def removegroup(groupID):
    return 0

# Deletes event and all prices associated with event
def removeevent(eventID):
    return 0 