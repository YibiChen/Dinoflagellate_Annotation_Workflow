source ../env.sh

run_cmd "perl ${GENEMARK}/gmes_petap.pl --ES --cores $NCPUS --v --sequence ${GENOME_NAME}.masked 1>&2> genemark.log"

# Convert the GeneMark-ES genemark.gtf file into genemark.gff3 for use in EvidenceModler. 
run_cmd "perl ${MAKER}/genemark_gtf2gff3 genemark.gtf > genemark.gff3"

