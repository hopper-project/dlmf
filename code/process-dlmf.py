# process the dlmf to extract all of the equations. downloads the html, does a crude
# parsing to find the names of all of the equations, and then downloads the .tex, .pmml
# and the .png for all of the equations
# jdl, october 9, 2016

import re, os

outpath = "/Users/lafferty/Desktop/DLMF/"

def make_chapter_directory(path, chapter):
    outdir = "%s%d" % (path, chapter)
    try:
        os.stat(outdir)
    except:
        print "creating directory %s" % outdir
        os.mkdir(outdir)    
    return(outdir)

def make_section_directory(path, chapter, section):
    outdir = "%s%d/%d.%d" % (path, chapter, chapter, section)
    try:
        os.stat(outdir)
    except:
        print "creating directory %s" % outdir
        os.mkdir(outdir)    
    return(outdir)

def download_equation(chapter, section, eqfn, outdir):
    print "  %s" % eqfn
    curlcmd = "curl -s http://dlmf.nist.gov/%s.png > %s/%s.png" % (eqfn, outdir, eqfn)
    os.system(curlcmd)
    curlcmd = "curl -s http://dlmf.nist.gov/%s.pmml > %s/%s.pmml" % (eqfn, outdir, eqfn)
    os.system(curlcmd)
    curlcmd = "curl -s http://dlmf.nist.gov/%s.tex > %s/%s.tex" % (eqfn, outdir, eqfn)
    os.system(curlcmd)

def process_section(chapter, section):
    make_chapter_directory(outpath, chapter)
    outdir = make_section_directory(outpath, chapter, section)

    curlcmd = "curl -s http://dlmf.nist.gov/%d.%d > %s/%d.%d.html" % (chapter, section, outdir, chapter, section)
    print curlcmd
    os.system(curlcmd)

    infn = "%s/%d.%d.html" % (outdir, chapter, section)
    inf = open(infn, 'r')

    s = inf.read()
    e = re.split('\.pmml', s)
    numeq = len(e)
    print 'Section %d.%d has %d equations' % (chapter, section, numeq-1)

    for eqno in range(numeq-1):
        es = e[eqno].split('/')
        eqfn = es[len(es)-1]
        download_equation(chapter, section, eqfn, outdir)
    return(numeq)


def process_chapter(chapter):
    outdir = make_chapter_directory(outpath, chapter)
    curlcmd = "curl -s http://dlmf.nist.gov/%d > %s/%d.html" % (chapter, outdir, chapter)
    print curlcmd
    os.system(curlcmd)

    infn = "%s/%d.html" % (outdir, chapter)
    inf = open(infn, 'r')

    s = inf.read()
    ss = s.split('rel="section" href="')
    numsec = len(ss)
    print 'Chapter %d has %d sections' % (chapter, numsec-1)

    eqs = 0
    for section in range(1,numsec):
        t = ss[section].split('"')[0]
        secnm = t.split('/')[1]
        print "  %s" % secnm
        eqs = eqs + process_section(chapter, section)
    return(eqs)

def process_dlmf():
    total_eqs = 0
    for c in range(1,37):
        eqs = process_chapter(c)
        total_eqs = total_eqs + eqs
        print "Processed chapter %d: %d equations (%d total)" % (c, eqs, total_eqs)


process_dlmf()



