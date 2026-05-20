# Comparative analysis of sulfoquinovose metabolism across herbivorous animal microbiomes 🐄

### Goal
To identify microbial taxa and metabolic pathways associated with sulfoquinovose (SQ) utilization in herbivores 

### Data source
- [Compendium of 4,941 rumen metagenome-assembled genomes for rumen microbiome biology and enzyme discovery | Nature Biotechnology](https://www.nature.com/articles/s41587-019-0202-3)

- https://www.ncbi.nlm.nih.gov/bioproject/522726

## Notebooks and scripts information
- `genomes_download.py` - script for downloading genome assemblies from NCBI using a list of assembly IDs (GCF/GCA)
- `bakta_annot.sh` - script for genome annotation using Bakta (https://github.com/oschwengers/bakta) with pre-download of a light database
- `diamond.sh` - performs DIAMOND-based protein alignment (https://github.com/bbuchfink/diamond)
- `build_meta.py`
- `sq-clusters.ipynb`
- `clusters_visualization.ipynb`
- `co-occurance.ipynb`   
- `loci.ipynb`
- `tree.ipynb`
- `distribution_analysis.ipynb`
- `vizualize_landscape.ipynb`

## Data information
- SQ_ref_enzymes.tsv
- sq_enzymes.faa
- mags_metadata.tsv
- assemblies_ids.txt
- bakta_annotation
- unique_sq_best_hits.tsv
- gtdbtk_summary_all.csv
- SQ_metatable_all.tsv
- clusters_candidates.tsv
- final_table.csv
- df_filtered.csv 
- classify               
