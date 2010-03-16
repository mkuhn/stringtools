#!/usr/bin/env python
# encoding: utf-8

## Use this script to exclude channels from STRING and re-combine the scores
## in a manner that is consistent with the remainder of STRING.

import sys
import os

from compute_scores import compute_combined_score_protein_protein 

def main():

    ## in order to remove biases towards the excluded channels, the new combined score
    ## needs to have the same cutoff as the original data
    cutoff = 0.15

    for line in sys.stdin:
        
        # skip header
        if line.startswith("protein"):
            print line,
            continue
        
        # extract fields, careful: the flat files only contain the part after the "0."
        fields = line.strip("\n").split()
        
        (neighborhood, neighborhood_transferred, fusion, cooccurence, homology, coexpression, coexpression_transferred, experiments, 
                experiments_transferred, database, database_transferred, textmining, textmining_transferred, combined_score) = ( 0.001 * float(x) for x in fields[2:] )

        ## Uncomment the channels you want to discard
        # neighborhood = 0
        # neighborhood_transferred = 0
        # fusion = 0
        # cooccurence = 0
        # homology = 0
        # coexpression = 0
        # coexpression_transferred = 0
        # experiments = 0
        # experiments_transferred = 0
        # database = 0
        # database_transferred = 0
        # textmining = 0
        # textmining_transferred = 0
                
        # apply prior correction
        combined_score = compute_combined_score_protein_protein(neighborhood, neighborhood_transferred, fusion, cooccurence, homology, coexpression, 
                        coexpression_transferred, experiments, experiments_transferred, database, database_transferred, textmining, textmining_transferred)
                        
        if combined_score < cutoff: continue
        
        # put the output together
        fields[2:] = ( "%d" % round(1000*x) for x in (neighborhood, neighborhood_transferred, fusion, cooccurence, homology, coexpression, coexpression_transferred, experiments, 
                experiments_transferred, database, database_transferred, textmining, textmining_transferred, combined_score) )
        
        print " ".join(fields)
    
    


if __name__ == '__main__':
    main()

