from pymol import cmd
from pymol import stored

########################READ ME ##################################
#Prior to running the program,                                   #
# 1. change the directory to the one with this program           #
# 2. open the original pdb file                                  #
# 3. type in the command:                                        #
#     > create test, (your pdb file name)                        #  
# 4. create an input csv file using excel in the following format#
#     column A: the number of the residue being change           #
#     column B-whatever: the residues that will be altered to    #
#This program can be run on the PyMOL by the folloing command    #
#  > run change_residues.py                                      #
#Output:                                                         #
# The output file names will indicate the residue number, and the#
#  residue that is changed to.                                   #
# Each output file contains X, Y, and Z coordinates of each atom #
#  in a residue in all of the residue's rotamer states.          #
#                                                                #
#My original plan was to output the strains and percentages of   #
# all of the rotamers after doing mutagenesis, but I can't figure#
# out how to output those values after 8 hours of trying.        #
##################################################################

def openFile():
 residues={}
 file=open("residue_input.csv","r")
 for ln in file:
  ln=ln.strip("\n")
  ln=ln.split(",")
  if ln[-1] == '':
   ln=ln[:-1]
  residues[int(ln[0])]=ln[1:]
 return residues

residues=openFile()

def mutXYZposition(atom_num,residues):
 cmd.hide("everything")
 cmd.show("sticks")
 for resi in residues:
  cmd.wizard("mutagenesis")
  cmd.do("refresh_wizard")
  # Mutate
  for caa in residues[resi]:
   print(resi,caa)
   filename="residue"+str(resi)+"to"+caa+".csv"
   outfile= open(filename,"w")
   row=("rotamer"+","+"X"+","+"Y"+","+"Z"+"\n")
   natom=atom_num[caa]
   cmd.get_wizard().set_mode(caa)
   sel="/test//A/"+str(i) 
   cmd.get_wizard().do_select(sel)
   fram= cmd.count_states("mutation")
   #cmd.frame(fram)
   stored.pos = []
   cmd.iterate_state(0, 'mutation', 'stored.pos.append((x,y,z))', atomic=0)
   counter=1
   state=1
   for po in stored.pos:
    if counter < natom:
     row=(str(state)+","+str(po[0])+","+str(po[1])+","+str(po[2])+"\n")
     outfile.write(row)
     counter+=1
    elif counter == natom:
     row=(str(state)+","+str(po[0])+","+str(po[1])+","+str(po[2])+"\n")
     outfile.write(row)
     counter=1
     state+=1
   outfile.close()


atom_num={
'ARG': 16,
'ASN': 8,
'ASP': 8,
'CYS': 4,
'GLN': 12,
'GLU': 12,
'HIS': 8,
'ILE': 8,
'LEU': 8,
'LYS': 16,
'MET': 12,
'RHE': 8,
'PRO': 8,
'SER': 4,
'THR': 4,
'TYR': 8,
'TRP': 8,
'VAL': 4
}

mutXYZposition(atom_num,residues)

 
 # for f in range (1,fram):
 #  s=fram-f
 #  cmd.frame(s)
  # cmd.get_wizard().apply()
  # cmd.save("state"+str(i) +"_"+ str(s) + ".pdb")
