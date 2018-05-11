********************************************
FILES:
********************************************

*** PYTHON: 
Main.py						- parses cim files, creates matpower casefiles, ybus, and database
HelpFunctions.py 			- some generic helping functions, such as printing a matrix with aligned columns		
BusBranch.py 				- defines classes used to construct matpower bus-branch model  
MyCIM.py 					- loads CIM module, defines which cim objects and which values should be parsed from xml 
SQLiteFunctions.py 			- functions for creating a SQLite database

*** MATLAB:
validate_mpc_and_ybus.m		- validate matpower case and y-bus
Total_MG_casefile.m			- mpc from CIM2Matpower (MG_T1)
Total_MG_T1_python.m		- mpc from python (MG_T1)
Total_MG_T1_Ybus.m			- Y-matrix from python (MG_T1) 
T1_BE_python.m 				- mpc from python (T1_BE - assignment 1)
TE_BE_Ybus.m				- Y-matrix from python (T1_BE - assignment 1)

*** SQLITE:
cim_database.sqlite 		- SQLite database


*********************************************
PYTHON CODE DESCRIPTION:
*********************************************

-----------
Main.py 
----------- 

Contains only 1 class ParseXMLtoCIM which is an envelope for all the processing. 
It has the following which should be called in order: 

--- functions ---:
 
* parseEQ() - Parse EQ xml file. CIM objects are constructed for each parsed element 
and saved in dict l. Foreign keys are stored in dict links. Only elements and fields
defined in MyCIM are parsed.   

* parseSSH() - Parse SSH xml file and update CIM objects. 

* update_id_lists() - create internal lists with keys to objects of a specific type,
note that this avoids having to loop through all objects if we wish to access all 
objects of a specific type 

* create_bus_branch_objects() - Create the topological bus-branch model. First group 
connectivity nodes into buses and then create lines, shunts and generators from 
the appropriate objects. Uses classes from BusBranch. 

* print_matpower_case() - From the bus-branch model print the MATPOWER case struct. 

* compute_y_matrix() - Compute the admittance matrix.  

* print_y_matrix() - Print Y-matrix for comparison in MATLAB.

* create_sql_database() - Insert all objects from l into a SQLite database.

Remaining functions are helping functions for the above functions, apart from main 

--- variables ---:

* l - dict with CIM objects using id as key 

* links - dict with dict containing foregin keys using id as key
For ACLineSegments it looks like: 
{'id1_line1':{'EquipmentContainer':id2,'BaseVoltage':id3},'id2_line2':{'EquipmentContainer':id3,'BaseVoltage':id4},...}

-------------
MyCIM.py: 
-------------
Contains the following global variables: 

* registry - Dict with CIM classes stored with simple names as keys. Note that
only objects of the types stored here are stored in the database. Objects of types
not in this dict will be jumped over. 

* object_fields - Dict deciding which fields should be stored for all classes in 
registry, if these fields are found. 

* object_foreign_keys - Dict deciding which foreign keys should be stored for 
all classes in registry. 


******************************************
NOTES
******************************************

1. The XML files are parsed only once. 

2. The SQLITE database is not used for anything. The tables are just created
and populated with the objects. 

3. For the topology processing group_connectivity_nodes() is the main function. 
It relies on other functions like find_connected_nodes() and find_base_voltages(). 
These functions are recursive so that they call themselves. The topology processing 
is not very efficient, becase the same terminal may be transversed several times, 
but this is not a problem for small networks. 

   