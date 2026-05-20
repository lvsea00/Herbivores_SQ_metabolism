# Comparative analysis of sulfoquinovose metabolism across herbivorous animal microbiomes 🌿

The project aims to investigate the metabolic capacity of gut microbiomes from herbivorous animals to utilize **sulfoquinovose (SQ)**, a plant-derived sugar that is known to be metabolized by the gut microbiota. To identify microbial taxa and metabolic pathways associated with sulfoquinovose (SQ) utilization we created a workflow for the searching and classification of potential loci of sulfoquinose metabolism in **metagenomically assembled genomes (MAGs)**

**Data source**:
Here we focused on studying cattle microbiomes leveraging publicly available metagenomic datasets (4,941 rumen microbial MAGs from 282 ruminant cattle 🐄)
- [Compendium of 4,941 rumen metagenome-assembled genomes for rumen microbiome biology and enzyme discovery | Nature Biotechnology](https://www.nature.com/articles/s41587-019-0202-3)

- https://www.ncbi.nlm.nih.gov/bioproject/522726

## Workflow
### Data collection
With `genomes_download.py` script collect MAGs from NCBI using a list of assembly IDs (GCF/GCA)

### Data preparation
1. **Quality control** (>70% completeness): **CheckM2** (https://github.com/chklovski/CheckM2)
2. **Dereplication** (<5% contamination): **dRep** (https://github.com/MrOlm/drep)
   
### Data processing
1. **MAGs annotation** with `bakta_annot.sh` - script for genome annotation using Bakta (https://github.com/oschwengers/bakta) with pre-download of a light bakta database
2. **MAGs taxonomy: GTDBtk** (https://github.com/ecogenomics/gtdbtk)
3. **Homology search**: `diamond.sh` - diamond (https://github.com/bbuchfink/diamond)
4. **Build up meta-table**: `build_meta.py`
   
### Data analysis
1. Co-localization check and SQ-loci classification - `sq-clusters.ipynb`
2. Genes co-occurrence - `co-occurance.ipynb`
3. Study of the most complete loci - `loci.ipynb`
4. Phylogenetic tree reconstruction - `tree.ipynb`
5. Distribution analysis - `distribution_analysis.ipynb`
6. SQ-loci visualization - `vizualize_landscape.ipynb`

## Data information
- SQ_ref_enzymes.tsv - a table with information on enzymes of different metabolic pathways of sulfoquinose degradation
- sq_enzymes.faa - protein fasta sequences of sulfoquinose degradation enzymes
- assemblies_ids.txt - list of MAGs IDs after CheckM2 and dRep (data preparation step)
- bakta_annotation - a directory with annotation results (only the genomes visualized further are presented) 
- unique_sq_best_hits.tsv - `diamond.sh` output file with best diamond hits
- gtdbtk_summary_all.csv - GTDBtk output table
- SQ_metatable_all.tsv - `build_meta.py` output table with meta information about diamond hits
- clusters_candidates.tsv
- final_table.csv
- clusters_filtered.csv 
- classify             
