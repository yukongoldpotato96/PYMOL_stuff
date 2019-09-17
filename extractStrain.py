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
#This program can be run on PyMOL by the folloing command         #
#  > run extractStrain.py                                         #
#Output:                                                          #
# The output file names will indicate the residue number, and the #
#  residue that is changed to.                                    #
# Each output file contains X, Y, and Z coordinates of each atom  #
#  in a residue in all of the residue's rotamer states.           #
# Edit: Dawn suggested that it will be helpful to output          #
#        all the rotamers in pdb form, which can then be          #
#        access through importing from the directory file         #
#                                                                 #
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

def extractStrain(residues):
 cmd.hide("everything")
 cmd.show("sticks")
 for resi in residues:
  for caa in residues[resi]:
   filename="residue"+str(resi)+"to"+caa+".csv"
   outfile= open(filename,"w")
   print(resi,caa)
   cmd.wizard("mutagenesis")
   cmd.do("refresh_wizard")
   cmd.get_wizard().set_mode(caa)
   sel="/test//A/"+str(resi)
   cmd.get_wizard().do_select(sel)
   bump_name="_bump_check"
   cmd.sculpt_activate(bump_name)
   cmd.set("sculpt_vdw_vis_mode",1,bump_name)
   for rotamer in range(1,1+cmd.count_states(bump_name)):
    score = cmd.sculpt_iterate(bump_name, rotamer, 1)
    row=(str(rotamer)+","+str(score)+"\n")
    outfile.write(row)
   outfile.close()
   cmd.get_wizard().clear()

extractStrain(residue_input)

