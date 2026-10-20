          seed = -1
       seqfile = data/aln_mtCDNApri123.txt
      treefile = data/tree_mtCDNApri.tree
       outfile = out

         ndata = 3
       seqtype = 0    * 0: nucleotides; 1:codons; 2:AAs
       usedata = 1    * 0: no data; 1:seq like; 2:use in.BV; 3: out.BV
         clock = 1    * 1: global clock; 2: independent rates; 3: correlated rates

         model = 0    * 0:JC69, 1:K80, 2:F81, 3:F84, 4:HKY85
         alpha = 0    * alpha for gamma rates at sites
         ncatG = 5    * No. categories in discrete gamma

     cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?

       BDparas = 1 1 0 C  * birth, death, sampling
   kappa_gamma = 6 2      * gamma prior for kappa
   alpha_gamma = 1 1      * gamma prior for alpha

   rgene_gamma = 2 2      * gamma prior for overall rates for genes
  sigma2_gamma = 1 10     * gamma prior for sigma^2     (for clock=2 or 3)

         print = 1
        burnin = 200
      sampfreq = 10
       nsample = 2000
*    checkpoint = 1 0.01 mcmctree.ckpt1 * flag(0: none;  1: save;  2: resume) prob filename
