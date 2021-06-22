"""
Assuming all mapped transcripts are indicating real gene models, this script can be used to generate corresponding splice sites.

Typical target is transcripts with good mapping quality bu failed because of unkown splice sites.

Input: PASA validation results (e.g. "alignment.validations.output")

Output to stdout: splice_site_donor splice_site_acceptor scaffold start end

"""

import re,sys


pasa_validation_results = sys.argv[1]

class SpliceSite(object):

    def __init__(self):
        self.donor = None
        self.acceptor = None
        self.scaffold = None
        self.start = None
        self.end = None


def get_rc(string):
    seq=string.upper()
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    bases = list(seq) 
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)    
    return bases


class SplicedAlignment(object):
    transcript = None
    scaffold = None

    def __init__(self,validation_record):
        record = validation_record.strip().split("\t")
        transcript = record[1]
        scaffold = record[4]
        strand = "+"

        align_string = record[13][21:]

        # guess strand by splice site
        if align_string.upper().count("CT") > align_string.upper().count("AG"):
            strand = "-"

        splice_site_strings = re.findall('[0-9]+\([0-9]+\)>[a-zA-Z]{2}\.{4}[a-zA-Z]{2}<[0-9]+\([0-9]+\)',align_string)

        for splice_site_string in splice_site_strings: 
            splice_site = SpliceSite()
            splice_site.scaffold=scaffold
            if strand == "+":
                splice_site.donor=re.findall('[a-zA-Z]{2}',splice_site_string)[0].upper()
                splice_site.acceptor=re.findall('[a-zA-Z]{2}',splice_site_string)[1].upper()
            else:
                splice_site.donor=get_rc(re.findall('[a-zA-Z]{2}',splice_site_string)[1]).upper()
                splice_site.acceptor=get_rc(re.findall('[a-zA-Z]{2}',splice_site_string)[0]).upper()

            splice_site.start=str(int(re.findall('[0-9]+',splice_site_string)[0])+1)
            splice_site.end=str(int(re.findall('[0-9]+',splice_site_string)[2])-1)

            print (splice_site.donor+"-"+splice_site.acceptor+"\t"+scaffold+"\t"+splice_site.start+"\t"+splice_site.end)

with open(pasa_validation_results) as f:
    for line in f:
        if line.startswith("#"):
            continue
        else:
            SplicedAlignment(line)
