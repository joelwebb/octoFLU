<p align="center">
  <img src="https://github.com/flu-crew/octoFLU/blob/master/img/octoFLU_revised_V3-01.png">
</p>

# octoFLU_GUI: A Graphical User Interface for the automated classification to evolutionary origin of influenza A virus gene sequences detected in U.S. swine

## Use
This package is a fork from the following manuscript that adds a simple graphical user interface, along with code to automate installation of packages and creates an executable:

Chang, J.<sup>+</sup>, Anderson, T.K.<sup>+</sup>, Zeller, M.A.<sup>+</sup>, Gauger, P.C., Vincent, A.L. (2019). octoFLU: Automated classification to evolutionary origin of influenza A virus gene sequences detected in U.S. swine. [*Microbiology Resource Announcements* 8:e00673-19](https://doi.org/10.1128/MRA.00673-19). <sup>+</sup>These authors contributed equally.

Original software can be found here: https://github.com/flu-crew/octoFLU
 

## Input
Unaligned fasta with query sequences (e.g., strain name with protein segment identifier).

## Output
* Text output stating the query name, protein symbol, genetic clade or evolutionary lineage. 
* Text output holding the query name and top BLASTn hit. 
* Inferred maximum likelihood trees with reference gene sets and queries.

## Usage

```
Double click the executable shortcut "OctoFLU_Gui" and select the input fasta file, along with a directory to hold the output.
```

## Installation

```
pip3 install smof
pip3 install dendropy
git clone https://github.com/flu-crew/octoFLU.git
cd octoFLU
```
If you are on linux, you can likely just use pip vs. pip3.

## Running the pipeline

You will need to have an installation of:

* [NCBI Blast](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download), 
* [smof](https://github.com/incertae-sedis/smof),
* [mafft](https://mafft.cbrc.jp/alignment/software/), 
* [FastTree](http://www.microbesonline.org/fasttree/#Install),
* [dendropy](https://dendropy.org/downloading.html),
* and the included `treedist.py` script

Edit the paths in `octoFLU_gui.py` to connect `blastn`, `makeblastdb`, `smof` `mafft`, and `FastTree`.

## Creating the executable file

* Install necessary packages by opening an administer command prompt and running the "install_important_files.py" by typing the command: "python install_important_files.py"
* Run the "create_gui.py" file by typing the command "python create_exe.py"
