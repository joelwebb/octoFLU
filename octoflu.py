import os
import sys
import subprocess
from shutil import which
from shutil import copyfile
from shutil import move
import PySimpleGUI as sg

def main():
	#make it a pretty color
	sg.theme('Dark Blue 3') 



	#define the actual layout order of the tabs: extraction --> merge --> analysis
	layout = [[sg.Text("\nPlease select the fasta files you want to process using OctoFLU:", font=( "Default 10 bold"))],
						[sg.Text("Fasta Files:   ", font=( "Default 10 bold")),sg.In(size=(80,10), key='fasta_file'), sg.FilesBrowse()],
						[sg.Text('Select a folder where you would like the output to go:',font=( "Default 10 bold"))],
						[sg.Text("Output Folder:", font=( "Default 10 bold")),sg.In(size=(80,10), key="output_directory"), sg.FolderBrowse()],
						[sg.OK("Run OctoFLU", key="run")],
						[sg.Text('Copyright Boehringer-Ingelheim 2020', font=( "Default 10 bold"))],
						]

	#define the window
	window = sg.Window("BI OctoFLU GUI", layout, grab_anywhere=False, size=(775,225), resizable=True)
	#read the variables

	while True:	
		event, values = window.Read()	
		# print(event,values)
					#run octoflu
		

		if event is None or event == 'Exit':		   # always,  always give a way out!	
			break 
			#close the window
			window.Close()

		elif event == "run":
			output_folder = values['output_directory']
			inputFile = values['fasta_file']
			# ===== Input and Output
			baseName = os.path.basename(inputFile)
			outDir = baseName + "_output"

			#check if path exists
			if os.path.exists(outDir):
				window.Close()
				sg.Popup("Directory " + outDir + " already exists. Please Select a new output directory.")
				sys.exit(1)
			else:
				os.mkdir(outDir)
				pass
			window.Close()
			integer = 0



				### TODO
			# programfiles X86 --- OctoFLU --- 



			

			# ===== Connect your reference here
			reference = "reference_data/reference.fa"

			# ===== Connect your programs here, Linux style
			BLASTN = "blastn"
			MAKEBLASTDB = "makeblastdb"
			SMOF = "smof"
			MAFFT = "mafft"
			FASTTREE = "FastTree.exe"
			NN_CLASS = "treedist.py"
			PYTHON = "python"



			# Attempt to use python3, but if not there check if python is python3
			if sys.version_info[0] < 3:
			    system.exit("Must be using Python 3")



			# Formal check of dependencies
			Err = 0
			if which(BLASTN) is None:
				print("blastn      .... need to install")
				Err = 1
			else:
				print("blastn      .... good")

			if which(MAKEBLASTDB) is None:
				print("makeblastdb      .... need to install")
				Err = 1
			else:
				print("makeblastdb      .... good")
				
			if which(MAFFT) is None:
				print("mafft      .... need to install")
				Err = 1
			else:
				print("mafft      .... good")
				
			if which(FASTTREE) is None:
				print("fastTree      .... need to install")
				Err = 1
			else:
				print("fastTree      .... good")
				
			if which(SMOF) is None:
				print("smof      .... need to install")
				Err = 1
			else:
				print("smof      .... good")
				
			if (Err == 1):
			    sys.exit("Link or install any of your 'need to install' programs above")
			
			
			# ===== Remove pipes in query header
			with open(inputFile, 'r') as file :
			  fileData = file.read()
			fileData = fileData.replace('|', '_')
			with open(baseName + ".clean", 'w') as file:
			  file.write(fileData)
			  
			# ===== Create your Blast Database
			# ${MAKEBLASTDB} -in ${REFERENCE} -parse_seqids -dbtype nucl      # requires no spaces in header
			subprocess.call([MAKEBLASTDB,"-in",reference,"-dbtype","nucl"])

			# ===== Search your Blast Database
			subprocess.run([BLASTN,"-db",reference,"-query",baseName + ".clean","-num_alignments","1","-outfmt","6","-out",outDir + "/blast_output.txt"], check = True)

			print("... results in " + outDir + "/blast_output.txt")

			# ===== Split out query into 8 segments
			H1list = []
			H3list = []
			N1list = []
			N2list = []
			PB2list = []
			PB1list = []
			PAlist = []
			NPlist = []
			Mlist = []
			NSlist = []

			with open(outDir + "/blast_output.txt", 'r') as file :
				for line in file:
					fields = line.strip().split()
					if("|H1|" in fields[1]):
						H1list.append(fields[0])
					if("|H3|" in fields[1]):
						H3list.append(fields[0])
					if("|N1|" in fields[1]):
						N1list.append(fields[0])
					if("|N2|" in fields[1]):
						N2list.append(fields[0])
					if("|PB2|" in fields[1]):
						PB2list.append(fields[0])
					if("|PB1|" in fields[1]):
						PB1list.append(fields[0])
					if("|PA|" in fields[1]):
						PAlist.append(fields[0])
					if("|NP|" in fields[1]):
						NPlist.append(fields[0])
					if("|M|" in fields[1]):
						Mlist.append(fields[0])
					if("|NS|" in fields[1]):
						NSlist.append(fields[0])
						
			#Make lists unique https://stackoverflow.com/questions/30650474/python-rename-duplicates-in-list-with-progressive-numbers-without-sorting-list
			def makeDistinct(elemList):
				return list(map(lambda x: x[1] + str(elemList[:x[0]].count(x[1]) + 1) if elemList.count(x[1]) > 1 else x[1], enumerate(elemList)))
			H1list = makeDistinct(H1list)
			H3list = makeDistinct(H3list)
			N1list = makeDistinct(N1list)
			N2list = makeDistinct(N2list)
			PB2list = makeDistinct(PB2list)
			PB1list = makeDistinct(PB1list)
			PAlist = makeDistinct(PAlist)
			NPlist = makeDistinct(NPlist)
			Mlist = makeDistinct(Mlist)
			NSlist = makeDistinct(NSlist)

						
			with open(outDir + "/H1.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in H1list])
			with open(outDir + "/H3.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in H3list])
			with open(outDir + "/N1.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in N1list])
			with open(outDir + "/N2.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in N2list])
			with open(outDir + "/PB2.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in PB2list])
			with open(outDir + "/PB1.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in PB1list])
			with open(outDir + "/PA.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in PAlist])
			with open(outDir + "/NP.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in NPlist])
			with open(outDir + "/M.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in Mlist])
			with open(outDir + "/NS.ids", 'w') as file:
				file.writelines(["%s\n" % item  for item in NSlist])

			ARR = ["H1", "H3", "N1", "N2", "PB2", "PB1", "PA", "NP", "M", "NS"]

			   
			# Fast part, separating out the sequences and adding references
			for segment in ARR:
				print(segment)
				segmentFile = outDir + "/" + segment + ".ids"
				print("Running SMOF...please wait")
				
				if os.path.isfile(segmentFile)  and os.path.getsize(segmentFile) > 0:
					#Translators note: import smof, do smoffy things would be better
					subprocess.run(SMOF + " grep -Xf " + outDir + "/" + segment + ".ids " + baseName + ".clean" + " > " + outDir + "/" + segment + ".fa", shell = True, check = True)
					subprocess.run(SMOF + " grep \"|" + segment + "|\" " + reference + " >> " + outDir + "/" + segment + ".fa", shell = True, check = True) 
					


				
			# Slow part, building the alignment and tree; slower from shell spin ups
			for segment in ARR:
				print(segment)
				segmentFile = outDir + "/" + segment + ".fa"
				if os.path.isfile(segmentFile):
					#subprocess.check_output([MAFFT, "--auto", "--reorder", outDir + "/" + segment + ".fa", ">", outDir + "/" + segment + "_aln.fa"], shell = True)
					subprocess.check_output(MAFFT + " --auto --reorder " + outDir + "/" + segment + ".fa > " + outDir + "/" + segment + "_aln.fa", shell = True)
					print("Running MAFFT......please wait")
					#subprocess.check_output([FASTTREE,"-nt","-gtr","-gamma",outDir + "/" + segment + "_aln.fa",">",outDir + "/" + segment + ".tre"], shell = True) # can drop -gtr -gamma for faster results
					subprocess.check_output(FASTTREE + " -nt -gtr -gamma " + outDir + "/" + segment + "_aln.fa" + " > " + outDir + "/" + segment + ".tre", shell = True) # can drop -gtr -gamma for faster results
					print("Running FASTTREE...please wait")
				if(os.path.isfile(outDir + "/" + segment + ".fa")):	
					os.remove(outDir + "/" + segment + ".fa")

			# Fast again, pull out clades
				finalOutputFile = outDir + "/" + segment + "_Final_Output.txt"
				if os.path.isfile(finalOutputFile):
					os.remove(finalOutputFile)
					
			#touch ${BASENAME}_Final_Output.txt
			# Annotations are based upon reading reference set deflines. For example, H1 genes have
			# the H1 gene at pipe 5, the US HA clade at pipe 1, and the Global HA clade at pipe 8.
			# These positions may be modified, or extended, to return any metadata required.
			print("Building trees...")
			if os.path.isfile(outDir + "/H1.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/H1.tre -c 5,1,8 i>> " + baseName + "_Final_Output.txt", shell = True)
				print("...")
			if os.path.isfile(outDir + "/H3.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/H3.tre -c 5,1,8 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/N1.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/N1.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/N2.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/N2.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/PB2.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/PB2.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/PB1.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/PB1.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/PA.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/PA.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/NP.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/NP.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/M.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/M.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")
			if os.path.isfile(outDir + "/NS.tre"):
				subprocess.run(PYTHON + " " + NN_CLASS + " " + "-i" + outDir + "/NS.tre -c 5,1 >> " + baseName + "_Final_Output.txt", shell = True, check = True)
				print("...")

			print("Finishing Up...")
			copyfile(baseName + "_Final_Output.txt", outDir + "/" + baseName + "_Final_Output.txt")
			move(outDir, output_folder)
			os.remove(baseName + ".clean")
			os.remove(baseName + "_Final_Output.txt")
			print("==== Final results in  " + baseName + "_Final_Output.txt and the alignment/tree files in the '" + outDir + "' folder")

if __name__ == '__main__':
	main()