#!/bin/bash

OUTPUT_DIR="../drep_output"

mkdir -p "$OUTPUT_DIR"

dRep dereplicate "$OUTPUT_DIR" \
  -g ../data/downloaded_genomes \
  -comp 70 \
  -con 5 \
  -p 8
  