# Comparative analysis of sulfoquinovose metabolism across herbivorous animal microbiomes 🌿🌾🐄

The project aims to investigate the metabolic capacity of gut microbiomes from herbivorous animals to utilize **sulfoquinovose (SQ)**, a plant-derived sugar that is known to be metabolized by the gut microbiota. To identify microbial taxa and metabolic pathways associated with sulfoquinovose (SQ) utilization we created a workflow for the searching and classification of potential loci of sulfoquinose metabolism in **metagenomically assembled genomes (MAGs)**

**Data source**:
Here we focused on studying cattle microbiomes leveraging publicly available metagenomic datasets (4,941 rumen microbial MAGs from 282 ruminant cattle)
- [Compendium of 4,941 rumen metagenome-assembled genomes for rumen microbiome biology and enzyme discovery | Nature Biotechnology](https://www.nature.com/articles/s41587-019-0202-3)

- https://www.ncbi.nlm.nih.gov/bioproject/522726

## 🔀 Workflow
### 🔍 Data collection
With [`genomes_download.py`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/genomes_download.py) script collect MAGs from NCBI using a list of assembly IDs (GCF/GCA)

### 🧹 Data preparation
1. **Quality control** (>70% completeness): **[CheckM2](https://github.com/chklovski/CheckM2)**
2. **Dereplication** (<5% contamination): **[dRep](https://github.com/MrOlm/drep)**
   
### ⚙️ Data processing
1. **MAGs annotation**: **[Bakta](https://github.com/oschwengers/bakta)** annotation with [`bakta_annot.sh`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/bakta_annot.sh)
2. **MAGs taxonomy**: defining taxonomic composition with [GTDBtk](https://github.com/ecogenomics/gtdbtk)
3. **Homology search**: searching for distant homologues of reference proteins from the SQ metabolism pathways in MAGs with **[diamond](https://github.com/bbuchfink/diamond)**, [`diamond.sh`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/diamond.sh)
4. **Build up meta-table**: collecting meta information about the found homologues with [`build_meta.py`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/build_meta.py)
   
### 📊 Data analysis
1. **Co-localization check and SQ-loci classification** - [`sq-clusters.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/sq-clusters.ipynb)
2. **Genes co-occurrence** - [`co-occurance.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/co-occurance.ipynb)
3. **Study of the most complete loci** - [`loci.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/loci.ipynb)
4. **Phylogenetic tree reconstruction** - [`tree.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/tree.ipynb)
5. **Distribution analysis** - [`distribution_analysis.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/distribution_analysis.ipynb)
6. **SQ-loci visualization** - [`vizualize_landscape.ipynb`](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/notebooks_and_scripts/vizualize_landscape.ipynb)

## 🗂️ Data information
- [SQ_ref_enzymes.tsv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/SQ_ref_enzymes.tsv) - a table with information on enzymes of different metabolic pathways of sulfoquinose degradation
- [sq_enzymes.faa](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/sq_enzymes.faa) - protein fasta sequences of sulfoquinose degradation enzymes
- [assemblies_ids.txt](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/assemblies_ids.txt) - list of MAGs IDs after CheckM2 and dRep (data preparation step)
- [bakta_annotation](https://github.com/lvsea00/Herbivores_SQ_metabolism/tree/main/data/bakta_annotations) - a directory with annotation results (only the genomes visualized further are presented) 
- [unique_sq_best_hits.tsv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/unique_sq_best_hits.tsv) - `diamond.sh` output file with best diamond hits
- [gtdbtk_summary_all.csv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/gtdbtk_summary_all.csv) - GTDBtk output table
- [SQ_metatable_all.tsv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/SQ_metatable_all.tsv) - `build_meta.py` output table with meta information about diamond hits
- [clusters_candidates.csv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/clusters_candidates.csv)- table with all the genes that form putative SQ clusters, `sq-clusters.ipynb` output
- [final_table.csv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/final_table.csv) - final table with all putative SQ clusters after pathways searching, `sq-clusters.ipynb` output
- [clusters_filtered.csv](https://github.com/lvsea00/Herbivores_SQ_metabolism/blob/main/data/clusters_filtered.csv)  - table with the most complete SQ clusters, `sq-clusters.ipynb` output
- [classify](https://github.com/lvsea00/Herbivores_SQ_metabolism/tree/main/data/classify) - directory with GTDBtk results

## 📝 Results
**1.** A total of 2175 dereplicated MAGs from 4941 downloaded were analyzed, resulting in the identification of 401 putative SQ-associated loci
**2.** Following gene co-localization and loci classification, 5 of 6 known pathways were detected (sulfo-EMP, sulfo-TAL, sulfo-TK,  sulfo-ASMO, sulfo-ED)
   
<img width="4200" height="1800" alt="image" src="https://github.com/user-attachments/assets/cfc43cdb-1efe-4ec8-80be-2f8c10ff2cfe" />

**3.** The performed phylogenetic reconstruction suggests that *Bacillota*, particularly **Lachnospirales** (enriched in sulfo-TAL) and **Oscillospirales** (enriched in sulfo-TK), are the dominant SQ-degrading bacteria

<img width="4000" height="4088" alt="image" src="https://github.com/user-attachments/assets/e577943e-86d1-41db-9859-6cb05ac8ce04" />

**4.** The genetic context of the most complete and widespread locus variants (sulfo-EMP, sulfo-TAL, sulfo-TK) was reconstructed

## Conclusions

## Contact

