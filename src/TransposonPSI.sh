source ../env.sh
export PATH=${BLAST}:$PATH

run_cmd "perl ${TRANSPOSON_PSI}/transposonPSI_mod.pl ${GENOME_NAME}_pasadb.sqlite.assemblies.fasta.transdecoder.pep.complete_only.filtered.top_coverage.faa prot"

