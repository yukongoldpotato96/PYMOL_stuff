from pymol import cmd
from pymol import stored

########################READ ME ###################################
#Prior to running the program,                                    #
# 1. change the directory to the one with this program            #
# 2. open the original pdb file                                   #
# 3. type in the command:                                         #
#     > create test, (your pdb file name)                         #  
# 4. create an input csv file using excel in the following format #
#     column A: the number of the residue being change            #
#     column B-whatever: the residues that will be altered to     #
#This program can be run on the PyMOL by the folloing command     #
#  > run change_residues.py                                       #
#Output:                                                          #
# The output file names will indicate the residue number, and the #
#  residue that is changed to.                                    #
# Each output file contains X, Y, and Z coordinates of each atom  #
#  in a residue in all of the residue's rotamer states.           #
# Edit 4/26/19pm: Dawn suggested that it will be helpful to output#
#                all the rotamers in pdb form, which can then be  #
#                access through importing from the directory file #
#                                                                 #
#My original plan was to output the strains and percentages of    #
# all of the rotamers after doing mutagenesis, but I can't figure # 
# out how to output those values after 8 hours of trying.         #
###################################################################

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

residue_input=openFile()

def mutXYZposition(residues):
 cmd.hide("everything")
 cmd.show("sticks")
 for resi in residues:
  for caa in residues[resi]:
   print(resi,caa)
   filename="residue"+str(resi)+"to"+caa+".csv"
   outfile= open(filename,"w")
   row=("rotamer"+","+"X"+","+"Y"+","+"Z"+"\n")
   cmd.wizard("mutagenesis")
   cmd.do("refresh_wizard")
   cmd.get_wizard().set_mode(caa)
   sel="/test//A/"+str(resi) 
   cmd.get_wizard().do_select(sel)
   fram= cmd.count_states("mutation")
   stored.pos = []
   cmd.iterate_state(0, 'mutation', 'stored.pos.append((x,y,z))', atomic=0)
   counter=1
   state=1
   natom=int(len(stored.pos)/fram)
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
   cmd.frame(fram)
   cmd.get_wizard().apply()
   cmd.set_wizard("done")
   cmd.save("residue"+str(resi)+"to"+caa+"rotamer"+str(fram)+".pdb")
   for f in range(1,fram):
    fra=fram-f
    cmd.wizard("mutagenesis")
    cmd.do("refresh_wizard")
    cmd.get_wizard().do_select(sel)
    cmd.frame(fra)
    cmd.get_wizard().apply()
    cmd.set_wizard("done")
    cmd.save("residue"+str(resi)+"to"+caa+"rotamer"+str(fra)+".pdb")
mutXYZposition(residue_input)

