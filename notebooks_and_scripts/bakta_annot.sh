#!/bin/bash

MAGS_DIR="${1:-../data/downloaded_genomes}"
BAKTA_DB_DIR="${2:-../data/bakta_db}"
ANNOT_DIR="${3:-../data/bakta_annotations}"

mkdir -p "$ANNOT_DIR"
mkdir -p "$BAKTA_DB_DIR"

if [ -d "$BAKTA_DB_DIR/db-light" ]; then
    echo "Bakta database already downloaded."
else
    bakta_db download --output "$BAKTA_DB_DIR" --type light
fi

for genome in "$MAGS_DIR"/*.fna.gz; do
    sample_name=$(basename "$genome" .fna.gz)
    output_dir="$ANNOT_DIR/${sample_name}_annot"

if [ -f "$output_dir/${sample_name}.gff3" ]; then
        echo "Skipping $sample_name - already processed" >&2
        continue
fi

bakta \
    --db "$BAKTA_DB_DIR/db-light" \
    --output "$output_dir" \
    --prefix "${sample_name}" \
    --threads 8 \
    --meta \
    --min-contig-length 200 \
    --keep-contig-headers \
    --verbose \
    "$genome"

    sleep 2
done
