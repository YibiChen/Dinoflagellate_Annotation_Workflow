# PBS headers

# assume you have all intron files within introns.fa

module load blast

cd PBS_O_WORKDIR

cp introns.fa $TMPDIR
cd $TMPDIR

awk '/^>/ {OUT=substr($0,2) ".fa"}; OUT {print >OUT}' introns.fa
rm introns.fa

for var in *.fa;
do
blastn -query test_intron.fa -subject test_intron.fa -strand minus -task blastn-short -outfmt 6 >> self_blast_intron.blast
done

cp self_blast_intron.blast $PBS_O_WORKDIR
