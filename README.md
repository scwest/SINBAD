# SINBAD: Survival-significant Isoform Networks By Altered Domain-inclusion
## Purpose
This code should be used for identifying potential protein-protein interaction (PPI) mechanistic changes based on survival analysis significance. In short, the code identifies multi-granularity graphs as *splice\_variant-domain-domain-splice\_variant* paths. 

The first splice variant must be significant for patient survival. The first domain must be either gained or ghost. The splice variants must belong to a known physical PPI.

Gained domains are those domains that are found in significant splice variants but not found in insignificant splice variants (within the same gene).
Ghost domains are those domains that are missing in significant splice variants but found in insignificant splice variants (within the same gene).

One could use the output to visualize these PPI and subsequently address whether they represent interesting mechanisms for patient survival.

This code is meant to be used in conjunction with NEEP (https://github.com/thecodingdoc/neep) but can be used with any files in the required format. So, one could use Cox PH for the survival values or use any alternative PPI, DDI, or splice variant annotation sources. 

## Installation
Prior to installation:
Graphviz must be installed for Python as well as for the system.

Using pip:

```console
cd /protein_mechanism_graphs
pip install .
```

Using setuptools:

```console
cd /protein_mechanism_graphs
python setup.py install
```

## Before Use
Some user construction of input files is required (to standardize information format). We provide examples of these files in the SINBAD/docs folder. These examples were created using prior versions of Ensembl, 3did, and BioGRID. We suggest that the user create up-to-date versions of these files using their desired databases. 
Specifically, SINBAD requires the following files:

**Domain-domain interaction file**
A file that contains physical domain interaction predictions/annotations.
Required format:
```
<domain>\t<domain>
...
```

**Gene to splice variant file**
A file that maps genes to splice variants in a 1-to-many fashion.
Required format:
```
<gene>\t<splice variant 1>,<splice variant2>,...,<final splice variant>
...
```

**Splice variant to protein file**
A file that maps splice variants to proteins in a 1-to-1 fashion. Note, this is only for protein-coding validation.
Required format:
```
<splice variant>\t<protein>
...
```

**Gene to gene file**
A file that maps genes to other genes in a 1-to-many fashion. Note, the gene products of a mapping must belong to physical PPIs. 
Required format:
```
<gene>\t<gene 1>,<gene 2>,...,<final gene>
...
```

**Splice variant to domain file**
A file that contains the domains for each splice variant in a 1-to-many fashion.
Required format:
```
<splice variant>\t<domain 1>,<domain2>,...,<final domain>
...
```

**Expression file**
The file for expression in the same input format as required by NEEP.
Required format:
```
,<patient 1>,<patient 2>,...,<final patient>
<splice variant or gene>,<patient 1 expression>,<patient 2 expression>,...,<final patient expression>
...
```

## Test
```console
cd SINBAD/test/
source test_output.txt
```

## Usage
command: multi\_granularity\_graphs

required parameters:\
	-d	--domain2domain=		\<Domain-domain interaction file>\
	-s	--gene2svars=			\<Gene to splice variant file>\
	-p	--svar2protein=			\<Splice variant to protein file>\
	-g	--gene2gene=			\<Gene to gene file; products are physical PPIs>\
	-i	--svar2domains=			\<Splice variant to domain file>\
	-a	--significant_svars=	\<NEEP output; 1st col: name, 4th col: adjusted significance value>\
	-e	--expression=			\<CSV expression file>
	
optional parameters:\
	-m	--min_threshold=		\<The minimum threshold used for NEEP. (default: 0.15)>\
	-o	--output=				\<The directory for the SVG MGG files. (default: ./)>\
	-h	--help=					\<Print help message>
	
## Output
Two examples of the output are placed into SINBAD/docs. These two examples were created using the LUAD cancer data set from The Cancer Genome Atlas. Each output file (.svg) is a multi-granularity graph (MGG). These are aggregated visualizations of the *splice\_variant-domain-domain-splice\_variant* paths. The MGG has four rows. The first row are the survival-significant splice variants, in purple. The second row are the gained/ghost domains that belong to the significant splice variant. Each of these domain nodes are split into two sides, with two colors. The left side is for calculating the gained/ghost/neither membership of the domain using ALL splice variants belonging to the parent gene. The right side filters the splice variants used by requiring them to have greater than 1-*min_threshold* patients expressed. For this row, green is a gained domain, blue is a ghost domain, and white is neither. The third row are the physical domain targets of the gained/ghost domains, in gray. The final row are the potentially interacting splice variants, in dark blue. These splice variants are merged if they have the same edge pattern and come from the same gene.

