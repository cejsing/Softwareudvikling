#!/usr/bin/python


# Test-database. Only exists while script is running!
"""
engine = create_engine('sqlite:///:memory:', echo=True)


# Should be moved once testing-phase is done

metadata = MetaData()
wares = Table( 
             'wares', metadata, 
             Column('wareid', Integer, primary_key=True),
             Column('warename', String(50)),
             Column('inbar', Integer),
             Column('instockroom', Integer)
             )
metadata.create_all(engine)
"""


    

"""
# This function should be called when new wares are added.
def insertware (wareidint, namestr):
    ins = wares.insert().values(wareid=wareidint, warename=namestr, inbar=0, instockroom=0)
    conn = engine.connect()
    result = conn.execute(ins)
    return 0
    


    



## code-testing:


insertware(1,'test')




def testfunction ():
    print("test")
    return 0

print (testfunction ())


print(sqlalchemy.__version__)
"""