#This is a tf-idf model for retrieving similar equations.
#The code can run in two "modes".
#In both instances it excepts as an input a set of files where
#each file contains the slt (syntax layout tree) representation of the equation
# First mode goes over all .tpl files and for each tuple it computes the frequency count and document frequency
# Second mode assumes that the document frequency has already been computed and the slt vocabulary has been created
#kk, december 9, 2016

import argparse
import collections
import math
import numpy as np
from scipy.spatial import distance
#from tqdm import tqdm

#Compute tf-idf and equation vectors similarities
def compute_df_tf_idf(filelist):
    vocabulary = dict()
    df = dict()
    large_collection=""
    files = open(filelist, 'r')
    num_docs=0
    for filename in files.readlines():
        num_docs+=1
        filename = filename.replace('\n','')
        local_vocab = dict()
        with open(filename, 'r') as tpl_file:
            words = tpl_file.read().replace('\n', ' ')
            large_collection = large_collection+" "+words
        words = words.split()
        local_fc = collections.Counter(words)
        for word in local_fc.keys():
            local_vocab[word] = local_fc.get(word)
            if (df.get(word)):
                df[word]= df.get(word)+1
            else:
                df[word]=1

    large_collection = large_collection.split()
    fc_count = collections.Counter(large_collection)

    #Store frequency counts
    fc_file = open(filelist+".fc", 'w')
    vocab_file = open(filelist + ".vocab", 'w')
    for word in fc_count.keys():
        vocabulary[word] = len(vocabulary)
        fc_file.write(str(word)+"\t"+str(fc_count.get(word))+"\n")
        vocab_file.write(str(word) + "\t" + str(len(vocabulary)-1) + "\n")
    fc_file.close()
    vocab_file.close()

    #Store document frequency
    df_file = open(filelist + ".df", 'w')
    for word in df.keys():
        df_file.write(str(word) + "\t" + str(df.get(word)) + "\n")
    df_file.close()

    #Now compute tf-idf vectors
    size = (num_docs,len(vocabulary))
    equations_tfidf = np.zeros((num_docs,len(vocabulary)))
    doc_vocab = open(filelist + ".doc_map", 'w')
    doc_enum = []
    enum_doc = []
    files = open(filelist, 'r')
    doc_num=0;

    #pbar = tqdm(total=num_docs)
    #Store tf-idf vectors
    for filename in files.readlines():
        #pbar.update(1)
        filename = filename.replace('\n','')
        file_prefix= filename.split("/")[3].split(".tpl")[0]
        doc_vocab.write(file_prefix+"\t"+str(doc_num)+"\n")
        doc_enum.append(doc_num)
        enum_doc.append(file_prefix)
        tfidf_file = open(filename + ".tfidf_small", 'w')
        local_vocab = dict()
        with open(filename, 'r') as tpl_file:
            words = tpl_file.read().replace('\n', ' ')
        words = words.split()
        doc_len  = len(words)
        local_fc = collections.Counter(words)
        for word in local_fc.keys():
            fc = local_fc.get(word)
            local_vocab[word] = fc
            tf = fc/doc_len
            idf = math.log(num_docs/df.get(word))
            tf_idf = tf*idf
            tfidf_file.write(word+"\t"+str(vocabulary.get(word))+"\t"+str(fc)+'\t'+str(round(tf,6))+'\t'+str(round(idf,6))+"\t"+str(round(tf_idf,6))+"\n")
            equations_tfidf[doc_num][vocabulary.get(word)]=tf_idf
        tfidf_file.close()
        doc_num += 1
    #pbar.close()
    ComputeSimilarityMetrics(equations_tfidf, doc_enum, enum_doc)

#Compute tf-idf using already stored df files
def compute_tf_idf(filelist,df_file, vocab_file, num_docs):
    #first load vocabulary and document files:
    vocab_file = open(vocab_file, 'r')
    vocabulary = dict()
    df = dict()
    num_lines=0
    for vocab_tokens in vocab_file.readlines():
        word = vocab_tokens.replace('\n', ' ').split("\t")
        vocabulary[word[0]] = int(word[1])
    vocab_file.close()

    df_file = open(df_file, 'r')
    for dict_tokens in df_file.readlines():
        word = dict_tokens.replace('\n', ' ').split("\t")
        df[word[0]] = int(word[1])
    df_file.close()

    list_file = open(filelist, 'r')
    num_files=0
    for lines in list_file.readlines():
       num_files+=1
    list_file.close()

    size = (num_files,len(vocabulary))
    equations_tfidf = np.zeros((num_files,len(vocabulary)))
    doc_vocab = open(filelist + ".doc_map", 'w')
    doc_enum = []
    enum_doc = []
    files = open(filelist, 'r')
    doc_num=0;
    #pbar = tqdm(total=num_docs)
    for filename in files.readlines():
        #pbar.update(1)
        filename = filename.replace('\n','')
        file_prefix= filename.split("/")[3].split(".tpl")[0]
        doc_vocab.write(file_prefix+"\t"+str(doc_num)+"\n")
        doc_enum.append(doc_num)
        enum_doc.append(file_prefix)
        tfidf_file = open(filename + ".tfidf_small", 'w')
        local_vocab = dict()
        tpl_file = open(filename, 'r')
        words = ""
        #print('Processing=' + str(filename))
        for tpl_tokens in tpl_file.readlines():
            tuple = tpl_tokens.replace('\n', '')
            #print('Tuple=' + tuple)
            simple_tuple = SimplyfyTuple(tuple)
            words = words + " " + simple_tuple
        words = words.strip()
        words = words.split()
        doc_len  = len(words)
        local_fc = collections.Counter(words)
        for word in local_fc.keys():
            fc = local_fc.get(word)
            local_vocab[word] = fc
            tf = fc/doc_len
            idf = math.log(num_docs/df.get(word))
            tf_idf = tf*idf
            tfidf_file.write(word+"\t"+str(vocabulary.get(word))+"\t"+str(fc)+'\t'+str(round(tf,6))+'\t'+str(round(idf,6))+"\t"+str(round(tf_idf,6))+"\n")
            equations_tfidf[doc_num][vocabulary.get(word)]=tf_idf
        tfidf_file.close()
        doc_num += 1
    #pbar.close()
    #np.savetxt(filelist+'.tfidf', equations_tfidf)
    ComputeSimilarityMetrics(equations_tfidf, doc_enum, enum_doc)

#Simplfy each SLT tuple
def SimplyfyTuple(tuple):
    tuple = tuple.replace("{","")
    tuple = tuple.replace("}","")
    elements = tuple.split(",")
    elem1 = GetSymbol(elements[0])
    elem2 = GetSymbol(elements[1])
    return "{"+elem1+","+elem2+"}"
def GetSymbol(elem):
    symbol = str(elem)
    if (len(symbol)==1):
        return symbol
    if (symbol.find("!")!=-1):
        symbol=symbol[symbol.find("!")+1:]
        if symbol=="!":
            return ""
        else:
            return symbol
    else:
        return symbol

# Compute Euclidean, Cosine and Jaccard metrics across all equation pairs in a given chapter
def ComputeSimilarityMetrics(equations_tfidf, doc_enum, enum_doc):
    enum_doc = np.asarray(enum_doc)
    bla = np.zeros((1,equations_tfidf.shape[1]))
    already_computed_eu = dict()
    already_computed_cos = dict()
    already_computed_jac = dict()
    for i in range(0, equations_tfidf.shape[0]):
        bla[0] = equations_tfidf[i]
        cosine2 = distance.cdist(bla, equations_tfidf, 'cosine')
        euclidean2 = distance.cdist(bla, equations_tfidf, 'euclidean')
        jaccard2 = distance.cdist(bla, equations_tfidf, 'jaccard')
        source = enum_doc[i]
        source_section = source.split(".")[0]+"."+source.split(".")[1]
        fhandle_eu = open(source_section + ".res_eu_small", "a")
        fhandle_cos = open(source_section + ".res_cos_small", "a")
        fhandle_jac = open(source_section + ".res_jac_small", "a")

        eu_sort = np.argsort(euclidean2[0])
        cos_sort = np.argsort(cosine2[0])
        jaccard_sort = np.argsort(jaccard2[0])

        euclidean2  = euclidean2[0][eu_sort]
        eu_words= enum_doc[eu_sort]

        cosine2 = cosine2[0][cos_sort]
        cos_words = enum_doc[cos_sort]

        jaccard2 = jaccard2[0][jaccard_sort]
        jac_words = enum_doc[jaccard_sort]

        for j in range(0, equations_tfidf.shape[0]):
            target = eu_words[j]
            target_section = target.split(".")[0] + "." + target.split(".")[1]
            if (target_section==source_section):
                if (already_computed_eu.get(source+"_"+target)==None) and (already_computed_eu.get(target+"_"+source)==None) and (source!=target):
                    fhandle_eu.write(source+"\t"+target+"\t"+str(round(euclidean2[j],6))+"\n")
                    already_computed_eu[source+"_"+target]=1

            target = cos_words[j]
            if (target_section == source_section):
                if (already_computed_cos.get(source + "_" + target) == None) and (already_computed_cos.get(target + "_" + source) == None) and (source!=target):
                    fhandle_cos.write(source + "\t" + target + "\t" + str(round(cosine2[j], 6)) + "\n")
                    already_computed_cos[source + "_" + target]=1

            target = jac_words[j]
            if (already_computed_jac.get(source + "_" + target) == None) and (already_computed_jac.get(target + "_" + source) == None) and (source!=target):
                fhandle_jac.write(source + "\t" + target + "\t" + str(round(jaccard2[j], 6)) + "\n")
                already_computed_jac[source + "_" + target]=1

        fhandle_eu.close()
        fhandle_cos.close()
        fhandle_jac.close()


def read_arguments():
    parser = argparse.ArgumentParser(description="tf-idf model for mathematical equations where each equation is represented as a set of symbols.")
    parser.add_argument('-fl', type=str, default="in.fl",
                        help='File list containing the path of the .tpl files.')
    parser.add_argument('-df', type=str, default="tpl.fl.df_small",
                        help='Document frequency file.')
    parser.add_argument('-num_docs', type=int, default=9884,
                        help='Number of documents in the collection.')
    parser.add_argument('-vocab', type=str, default="tpl.fl.vocab_small",
                        help='Vocabulary file.')
    parser.add_argument('-mode', type=str, default=1,
                        help='1 - represents equations as tf-idf vectors and computes all-pairs distances. '
                             '2 - represents equations as tf-idf vectors using computed df from 1. It also computes all-pairs distances. ')
    return parser.parse_args()
def main(args):

    if (args.mode==1):
        compute_df_tf_idf(args.fl)

    elif (args.mode==2):
        files = open(args.fl, 'r')
        for filename in files.readlines():
            filename = filename.replace('\n', '')
            print("Processing="+str(filename))
            compute_tf_idf(filename,args.df,args.vocab, args.num_docs)
    else:
        print("Wrong mode entered.")

if __name__ == '__main__':
    args = read_arguments()
    main(args)