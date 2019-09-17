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
#  > run doubleMut.py                                             #
#This is the double-mutation version of extractStain.py           #                                                              
###################################################################

residues=["GLY","ALA","SER","THR","CYS",
          "VAL","LEU","ILE","MET","PRO",      
          "PHE","TYR","TRP","ASP","GLU",  
          "ASN","GLN","HIS","LYS","ARG"]
three=["ARG","SER","GLN"]

def getPositions():
 positions=[]
 file=open("doubleMut_input.csv","r")
 original=file.readline().strip("\n").split(",")[1]
 file.readline()
 for ln in file:
  position=ln.strip("\n").split(",")
  positions.append([position[2],position[1]])
 return (original,positions)

rungetPos=getPositions()
original=rungetPos[0]
positions=rungetPos[1]

def doubleMut(original,positions,residues):
 cmd.hide("everything")
 cmd.show("sticks")

 posone=positions[0][0]
 chainone=positions[0][1]
 postwo=positions[1][0]
 chaintwo=positions[1][1]

 outfile=open("forheatmap.csv","w")

 #generate the protein with one mutation
 for a in residues:
  cmd.create(a, original)
  cmd.wizard("mutagenesis")
  cmd.do("refresh_wizard")
  cmd.get_wizard().set_mode(a)
  sel="/"+a+"//"+str(chainone)+"/"+str(posone)
  cmd.get_wizard().do_select(sel)
  cmd.get_wizard().apply()

 for m in residues: #for all the mutations generated
  for i in residues:  #for each residue to which will be mutated
   name=m+"2"
   cmd.create(name,m)
   cmd.wizard("mutagenesis")
   cmd.do("refresh_wizard")
   cmd.get_wizard().set_mode(i)
   se="/"+name+"//"+str(chaintwo)+"/"+str(postwo)
   cmd.get_wizard().do_select(se)
   mut_name="mutation"
   if cmd.count_states(mut_name) != 1:
    bump_name="_bump_check"
    cmd.sculpt_activate(bump_name)
    scores=[]
    for rotamer in range(1,1+cmd.count_states(bump_name)):
     score = cmd.sculpt_iterate(bump_name, rotamer, 1)
     scores.append(score)
    scores.sort(reverse=True)
    row=(i+","+m+","+str(scores[0])+"\n")
   else:
    row=(i+","+m+","+"?"+"\n")
   outfile.write(row)
 outfile.close()

doubleMut(original,positions, residues)