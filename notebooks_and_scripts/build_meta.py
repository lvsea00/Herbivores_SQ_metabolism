#!/usr/bin/env python3
import argparse
import glob
import os

import pandas as pd
from BCBio import GFF


def main():
    parser = argparse.ArgumentParser(description='Build metatable script.')
    parser.add_argument('--hits', default='../data/diamond_after_bakta/unique_sq_best_hits.tsv', help='Path to diamond hits file')
    parser.add_argument('--gff', default='../data/bakta_annotations/', help='Path to the directory containing .gff3 files')
    parser.add_argument('--taxonomy', default='../data/gtdbtk_summary_all.csv', help='Path to taxonomy file')
    parser.add_argument('--output_dir', default='../data/', help='Directory to save the output file')

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, "SQ_metatable_all.tsv")

    # 1. LOAD DIAMOND RESULTS
    cols = [
        "query",
        "target",
        "identity",
        "aln_len",
        "mismatch",
        "gap",
        "qstart",
        "qend",
        "tstart",
        "tend",
        "evalue",
        "bitscore"
    ]

    hits = pd.read_csv(args.hits, sep="\t", names=cols)

    # 2. PARSE TARGET IDS
    hits["MAG"] = hits["target"].str.extract(r"((?:GCA|GCF)_\d+\.\d+)")
    hits["locus_tag"] = hits["target"].str.split("_").str[-2:].str.join("_")

    # 3. PARSE GFF3 FILES
    gff_records = []
    gff_files = glob.glob(os.path.join(args.gff, "*/*.gff3"))

    for gff in gff_files:
        mag = os.path.basename(gff).replace(".gff3", "")
        with open(gff) as f:
            for record in GFF.parse(f):
                for feature in record.features:
                    if feature.type != "CDS":
                        continue

                    quals = feature.qualifiers
                    locus = quals.get("locus_tag", [None])[0]
                    product = quals.get("product", [None])[0]

                    gff_records.append({
                        "MAG": mag,
                        "locus_tag": locus,
                        "contig": record.id,
                        "start": int(feature.location.start) + 1,
                        "end": int(feature.location.end),
                        "product": product
                    })

    gff_df = pd.DataFrame(gff_records)

    # 4. MERGE TABLES
    meta = hits.merge(gff_df, on=["MAG", "locus_tag"], how="left")

    # 5. ADD TAXONOMY
    tax = pd.read_csv(args.taxonomy, sep="\t")
    tax["MAG"] = tax["user_genome"].str.replace("MAG_", "", regex=False)
    tax = tax.rename(columns={"classification": "taxonomy"})
    tax = tax[["MAG", "taxonomy"]]

    meta["MAG"] = meta["MAG"].astype(str).str.strip()
    tax["MAG"] = tax["MAG"].astype(str).str.strip()
    meta = meta.merge(tax, on="MAG", how="left", validate="many_to_one")

    # 6. SELECT FINAL COLUMNS
    meta = meta[[
        "MAG",
        "query",
        "target",
        "identity",
        "aln_len",
        "evalue",
        "bitscore",
        "product",
        "contig",
        "start",
        "end",
        "taxonomy"
    ]]

    # 7. Save the final table
    meta.to_csv(output_file, sep="\t", index=False)
    print(f"File saved to {output_file}")


if __name__ == "__main__":
    main()
