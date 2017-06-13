#!/bin/bash

tabix $1 $2 | awk '$NF<'$3 | cut -f2,3,14 > $6
plink --bfile $4 --extract <(cut -f1 $6) --r2 yes-really --ld-window-kb 100000000000 --ld-window 1000000 --out $6
./ldblock.py $6 $6.ld $6.out $5
Rscript --vanilla -e 'library(RColorBrewer);d=read.table("'$6.out'", header=T, sep=",");pdf("'$6.pdf'", width=15);plot(d$ps, -log10(d$p), col=c("gray", brewer.pal(8, "Set2"))[d$block+1], pch=20, cex=2, xlab="Position on chromosome", ylab=expression(paste("-log"[10], "(p)")));dev.off()'
rm $6.log