#!/bin/sh

sinbad --domain2domain=../docs/domain2domain.txt --gene2svars=../docs/gene2svars.txt  --svar2protein=../docs/svar2protein.txt --gene2gene=../docs/gene2gene.biogrid.txt --svar2domains=../docs/svar2domains.txt --significant_svars=../docs/LUAD.NEEP.first100.txt --expression=../docs/LUAD.isoform_expression.first100.csv --min_threshold=0.15 --output=.

echo "test complete";
