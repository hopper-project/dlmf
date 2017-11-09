# Modeling Equations in the DLFM collection
* Extract equations from the Digital Library of Mathematical Functions (dlmf), dlmf.nist.gov
# john lafferty

## Topic Modeling 
* The ptm/tm directory contains  code used for topic modeling:  
  * the ptm_funcs.R file contains the functions used to process raw data, run LDA, and extract concepts and concept distributions.
  * the ptm_driver.R shows how to use the functions in ptm_funcs.R  .
  * the lda_1.4.3.tar.gz file contains modified C code to run the "PTM1" model. It is based on [the R package lda](https://cran.r-project.org/web/packages/lda/).
    * To install it from the command line, run: R CMD INSTALL lda_1.4.3.tar.gz. **Warning: this will overwrite your current version of lda**.
* To download the raw data, click [here](https://www.dropbox.com/s/u93t9fzn3knbxnr/PTM_DATA_01.tar.gz?dl=0).  
  * The stat-th_pruned directory contains a pruned subset (38) of the wikipedia documents corresponding to "Statistical Theory"  
  * The arxiv_processed_trunc directory contains 3631 documents listed under the 'stat-th' category.  
    * The document have been truncated at 1000 words and the LaTeX has been stripped. 
    * Date range: 03/2011 - 11/2015  

## tf-idf 
* The ptm/tf-idf directory contains code for generating tf-idf scores for purposes of finding relevant mathematical/statistical topics for arxiv papers.
	* The ptm/tf-idf/keyword_search directory contains code which, given a list of concepts (provided in the directory) computes tf-idf scores for this list of concepts for each document in a specified corpus.
		* The keyword_functions.py file contains functions used to generate regular expressions and to compute tf-idf scores. The tf-idf scores are stored in python dictionaries.
		* The keyword_driver.py file shows how to use the functions in keyword_functions.py.
	* okapi_bm25 scores have been added as well.

* The raw text data for wiki pages and arxiv papers used can be found [here](https://drive.google.com/file/d/0B3wYZ-b_JMsWSHB0NE1jQ2hmWG8/view?usp=sharing)
* This may be the same data that Matt specified above, but this is what I specifically used.
# dlmf
# extract equations from the Digital Library of Mathematical Functions (dlmf), dlmf.nist.gov
# john lafferty


