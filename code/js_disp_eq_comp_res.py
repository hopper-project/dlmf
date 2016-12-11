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
    parser = argparse.ArgumentParser(description="Create HTML Table of Similar Equations")
    parser.add_argument('--res_file', type=str, default="dlmf2_res_cos_top100",
                        help='File list containing the path of the .tpl files.')
    parser.add_argument('--png_folder', type=str, default="../raw",
                        help='Directory path containing equation png files')
    return parser.parse_args()
def main(args):
    create_js_file(args.res_file,args.png_folder)
args = get_arguments()
main(args)
