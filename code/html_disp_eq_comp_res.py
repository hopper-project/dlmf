#processes a ranked list of equation pairs and generates a html table with equation images
#equation images are linked to DLMF source page
#input is a tsv file where the first two columns are the DLMF equation enumerators and the third column is the similarity value
#kk, december 9, 2016

import argparse

def create_html_table(res_file):
    html = open(res_file + ".html", 'w')

    html.write("<!DOCTYPE html>\n")
    html.write("<html>\n")
    html.write("<head>\n")
    html.write("<title> HTML Table Header </title >\n")
    html.write("</head>\n")
    html.write("<body>\n")
    html.write("<table border = \"1\", cellpadding=\"10\">\n")
    html.write("<tr align=\"center\"><th>Rank</th><th> Equation Number</th> <th> Equation </th> <th> Cos(Eq1,Eq2) </th> </tr>\n")

    files = open(res_file, 'r')
    rank=0
    for pair in files.readlines():
        rank+=1
        pair = pair.replace('\n','')
        eq = pair.split("\t")
        eq1b_path = "http://dlmf.nist.gov/"+eq[0]+".png"
        eq2b_path = "http://dlmf.nist.gov/"+eq[1]+".png"
        comp_result = eq[2]
        html.write("<tr><td  align=\"center\", rowspan=\"2\">" + str(rank) + "</td><td align=\"left\">"+eq[0]+"</td><td><a href=\"http://dlmf.nist.gov/"+eq[0].split(".E")[0]+"#E"+
                           eq[0].split(".E")[1]+"\"><img src = \"" + eq1b_path + "\"></td><td  align=\"left\". rowspan=\"2\", padding=30px >" + str(comp_result) + "</td>  </tr>\n")
        html.write("<tr><td>"+eq[1]+"</td><td><a href=\"http://dlmf.nist.gov/"+eq[1].split(".E")[0]+"#E"+
                           eq[1].split(".E")[1]+"\"><img src = \"" + eq2b_path + "\"></td>  </tr>\n")

    html.write("</table>")
    html.write("</body>")
    html.write("</html>")
    html.close()
   
def get_arguments():
    parser = argparse.ArgumentParser(description="Create HTML Table of Ranked Equation Pairs")
    parser.add_argument('--res_file', type=str, default="dlmf_res_cos_top100",
                        help='tsv file that contains ranked list of equation pairs and their simlarity score')
    return parser.parse_args()


def main(args):
    create_html_table(args.res_file)
args = get_arguments()
main(args)
