# Modeling Equations in the DLFM collection
## dlmf-process.py 
* Extract equations from the Digital Library of Mathematical Functions (dlmf), dlmf.nist.gov
## tf_idf_model.py
* Generates tf-idf vector from the SLT (syntax layout tree) representation of equations
* Computes distance metrics across all equations in a DLMF section
## tml_disp_eq_comp_res.py
* Processes a ranked list of equation pairs and generates a html table with equation images
* Equation images are linked to DLMF source page
* Input is a tsv file where the first two columns are the DLMF equation enumerators and the third column is the similarity value
## js_disp_eq_comp_res.py	
* Processes a ranked list of equation pairs and generates a JavaScript variable file. The file is used to display local equation images in an html table
