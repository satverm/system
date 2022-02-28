# This program is for converting the various system of the main system into and object and do various operatoins and also link with a database file for storin the data of many instances of the object

import sqlite3 as sq
import os

class System:

    # class attributes
##    system_id = 'uas' # input("Enter the system id: ")
##    system_name = 'TAPAS'  # input("Enter the system name: ")
##    filename = 'tapas.db'  # input("Enter the database filename (anyfile.db):")
     
    
    def __init__(self,system_id= None, system_name = None, filename = None):

        # The init attributes are define and value is given for testing. The __init__ can be made to take user inputs.
        if system_id == None:
            self.system_id = 'uas' #input("Enter the system ID: ")
        if system_name == None:
            self.system_name = 'tapas'  #input("Enter the system Name: ")
        if filename == None:
            self.filename = 'tapas.db'   #input("Enter the database filename(anyfilename.db): ")
        print("A system object has been created:{}, {}".format(self.system_id,self.system_name))
        print("The database file is : {}".format(self.filename))
        self.create_database('blank', self.filename)

    
    
    # create the database and various tables 
    # we can have just one table for the parent-child data
    def create_database(self, filepath = None, filename = None):
        if filepath is None:
            filepath = input("Enter the file path:")
        if filename is None:
            filename = input("Enter the database file name(anysystem.db):")
        con = sq.connect(filename)
        cur = con.cursor()
        # creating master tables

        # create a parent-child table which will have all the parents and the children systems and thus it will form the
        # product breakdown structure or hierarchy.
        cur.execute('''CREATE TABLE IF NOT EXISTS parent_child(dataid integer NOT NULL primary key autoincrement, parent_code text, child_code text, child_name text)''')
        # we can create functions which can create the system hierarchy using the above parent_child table data
        con.commit()
        con.close()
        print("New database created: {}".format(filename))


    def add_record(self, filepath = None, filename = None, new_record = None):
        if filepath is None:
            filepath = input("Enter the file path:")
        if filename is None:
            filename = input("Enter the database file name(anysystem.db):")
        if new_record is None:
            new_record = self.create_child_systems()
        con = sq.connect(filename)
        cur = con.cursor()
        # write the record in the parent_child table:
        cur.execute('INSERT INTO parent_child(parent_code, child_code, child_name) VALUES(?,?,?)',new_record)
        con.commit()
        print("New record added: ",new_record)
        con.close()


    # for making the pbs or the system hierarchy we can call create_child_systems() fun as many times
    def create_child_systems(self ,parent_system_id = None):
        print("Add a child system:")
        # we need to select the parent sys using a function select_parent_sys()
        if parent_system_id == None:
            parent_system_id = self.select_parent_sys()
        child_system_id = input("Enter the child system id:")
        child_system_name = input("Enter the child system name:")
        
        new_record = (parent_system_id, child_system_id,child_system_name)
        self.add_record('blank',self.filename,new_record)

    
    def add_main_systems(self):
        print("Add the main systems of a system which will be at the top most level:\n")
        while True:
            # here the parent system id will be the system_id since we are creating topmost main systems
            
            new_record = self.create_child_systems(self.system_id)
            self.add_record('',self.filename, new_record)
            more_records = input("press yes or Enter for adding more systems:(yes/no) ")
            if more_records.lower() == 'no':
                print("Main systems added !!")
                break
    
    # here we can select one parent and then keep adding children
    def add_child_systems(self, parent_code = None):
        pass
        
    # This can be modified to first select the main systes and then the child systems for the selected main system and so on
    def view_hierarchy(self):  

        con = sq.connect(self.filename)
        cur = con.cursor()
        # write the record in the parent_child table:
        cur.execute("SELECT * FROM parent_child")
        sel_record = cur.fetchall()
        for item in sorted(sel_record):
            print(item)
        con.close()
        
 
    def select_parent_sys(self):
        sel_prnt = str(input("Press Y or y to see all the parent child systems:"))
        if sel_prnt.lower() == 'y':
            self.view_hierarchy()
               
        selected_id = input("Enter the record id for which you want create child sytems: ")
        con = sq.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM parent_child WHERE dataid = (?) ",(selected_id,))
        sel_record = cur.fetchone()
        print("The selected record to make new child systems is: ",sel_record)
        new_parent = sel_record[0]
        print(new_parent)
        con.close()
        return(new_parent)
    
    
    def view_main_systems(self):
        
        selected_id = self.system_id  #we select system_id as the parent_code to get all the main systems
        con = sq.connect(self.filename)
        cur = con.cursor()
        cur.execute("SELECT * FROM parent_child WHERE parent_code = (?) ",(selected_id,)) # this logic can be inverted to only view child systems
        main_systems = cur.fetchall()
        print("The main systems of the System {} are: ".format(self.system_name))
        for item in main_systems:
            print(item)
        con.close()
        return(main_systems)

 
    def ui_menu(self):

        print('This Program can be used to store and retrieve passwords in a secure way.')
        menu_items = ['0: Exit the program!!','1: Create main systems','2: Create child systems','3: View main systems', "4: View a system's hierarchy"]
        while True:
            for k in menu_items:
                print(k)
            sel_opt = str(input("Enter the number for the selected option: "))
            print('The selected option is {}'.format(sel_opt))
            if sel_opt == '1':
                self.add_main_systems()
            elif sel_opt == '2':
                self.create_child_systems()
            elif sel_opt == '3':
                self.view_main_systems()
            elif sel_opt == '4':
                self.view_hierarchy()
            elif sel_opt == '0':
                print("Program finished!!")
                break
            else:
                print("Not a valid input !!")

auav = System()

auav.ui_menu()


# Testing
# newsystem = System()
# subsystem = newsystem.create_sub_systems(newsystem.system_id)
# print("The systemid and systemname are", subsystem)
        
        
