#processes a ranked list of equation pairs and generates a JavaScript variable file
#the file is used to display local equation images in an html table
#It requires two input files:
# 1. tsv file where the first two columns are the DLMF equation enumerators and the third column is the similarity value
# 2. path of the local directory where equation images reside
#kk, december 9, 2016


import argparse

def create_js_file(res_file, png_folder):

    js_file = open(res_file+".js",'w')
    js_file.write("var equations = [\n")

    files = open(res_file, 'r')
    rank=0
    for pair in files.readlines():
        rank+=1
        pair = pair.replace('\n','')
        eq = pair.split("\t")

        eq1_path = png_folder+"/"+eq[0].split(".")[0]+"/"+eq[0].split(".E")[0]+"/"+eq[0]+".png"
        eq2_path = png_folder + "/" + eq[1].split(".")[0] + "/" + eq[1].split(".E")[0] + "/" + eq[1]+".png"
        comp_result = eq[2]
        
        js_file.write("{\"eq1\": \""+eq1_path+"\", \"eq2\": \""+eq2_path+"\", \"sim_val\": \""+str(comp_result)+"\"},\n")
    
    js_file.write("];")
    js_file.close()

def get_arguments():
    parser = argparse.ArgumentParser(description="Create JavaScript variable file")
    parser.add_argument('--res_file', type=str, default="dlmf2_res_cos_top100",
                        help='tsv file that contains ranked list of equation pairs and their simlarity score.')
    parser.add_argument('--png_dir', type=str, default="../raw",
                        help='directory path containing equation png files.')
    return parser.parse_args()

def main(args):
    create_js_file(args.res_file,args.png_folder)
args = get_arguments()
main(args)
