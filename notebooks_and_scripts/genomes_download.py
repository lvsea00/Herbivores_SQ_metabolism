#!/usr/bin/env python3
import requests
import time
import os
import argparse
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_folder_url(base_url, genome_id):
    """
    Fetch the directory page and find the folder URL containing the genome ID.
    """
    resp = requests.get(base_url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if genome_id in href:
            return urljoin(base_url, href)
    raise FileNotFoundError(f"Folder for {genome_id} not found.")


def download_file(url, output_path):
    """
    Download a file from URL to local path.
    """
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                if chunk:
                    f.write(chunk)


def process_genome_id(genome_id, output_dir):
    """
    Process a single genome ID:
    - Construct URL path
    - Find the folder URL
    - Attempt to download main and alternative files
    """
    # Generate URL path based on ID
    prefix, digits_part = genome_id.split('_')
    digits = digits_part.split('.')[0]
    path = f"{prefix}/{digits[:3]}/{digits[3:6]}/{digits[6:9]}/"
    base_url = f"https://ftp.ncbi.nlm.nih.gov/genomes/all/{path}"

    try:
        folder_url = get_folder_url(base_url, genome_id)
    except Exception as e:
        logger.warning(f"Could not find folder for {genome_id}: {e}")
        return False

    # Get the folder name from URL
    folder_name = folder_url.rstrip('/').split('/')[-1]
    formats = ["_genomic.fna.gz", "_genomic.gbff.gz", "_genomic.gff.gz"]
    downloaded = False

    for fmt in formats:
        filename = folder_name + fmt
        download_url = urljoin(folder_url, filename)
        output_path = os.path.join(output_dir, f"{genome_id}{fmt}")

        try:
            download_file(download_url, output_path)
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"Downloaded {genome_id}: {size_mb:.2f} MB")
            logger.info(f"Downloaded {output_path} ({size_mb:.2f} MB)")
            downloaded = True
            break
        except requests.HTTPError:
            # If main file not found, try the next format
            continue
        except requests.RequestException as e:
            logger.warning(f"Failed to download {download_url} for {genome_id}: {e}")
            continue

    if not downloaded:
        print(f"No files found for {genome_id}.")
        logger.warning(f"No files found for {genome_id}.")
    return downloaded


if __name__ == "__main__":
    # Setup logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    full_log_handler = logging.FileHandler('../data/download_full_log.txt')
    full_log_handler.setLevel(logging.INFO)

    error_log_handler = logging.FileHandler('../data/download_errors.log')
    error_log_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    full_log_handler.setFormatter(formatter)
    error_log_handler.setFormatter(formatter)

    logger.addHandler(full_log_handler)
    logger.addHandler(error_log_handler)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Download genome assemblies')
    parser.add_argument('-o', '--output', default='../data/downloaded_genomes', help='Output folder path')
    parser.add_argument('-i', '--input', default='../data/assemblies_ids.txt', help='Input file with IDs')
    args = parser.parse_args()

    output_dir = args.output
    input_file = args.input

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read IDs from input file
    with open(input_file, 'r', encoding='utf-8') as f:
        ids = [line.strip() for line in f if line.strip()]

    print(f"Total IDs: {len(ids)}")
    logger.info(f"Total IDs: {len(ids)}")
    print(f"GCF: {sum(id.startswith('GCF') for id in ids)}")
    logger.info(f"GCF: {sum(id.startswith('GCF') for id in ids)}")
    print(f"GCA: {sum(id.startswith('GCA') for id in ids)}")
    logger.info(f"GCA: {sum(id.startswith('GCA') for id in ids)}")
    print('-' * 50)

    for genome_id in ids:
        try:
            print(f"\nProcessing {genome_id}...")
            success = process_genome_id(genome_id, output_dir)
            if success:
                print(f"{genome_id} downloaded successfully.")
            else:
                print(f"{genome_id} files not found.")
        except Exception as e:
            logger.error(f"Unexpected error for {genome_id}: {e}")
            print(f"Error processing {genome_id}: {e}")
        time.sleep(1)

    print('-' * 50)
    print(f"Download complete! Files saved to: {os.path.abspath(output_dir)}")
    logger.info(f"Download completed. Files saved to: {os.path.abspath(output_dir)}")

    # Summarize downloaded files
    files = os.listdir(output_dir)
    print(f"Total downloaded files: {len(files)}")
    logger.info(f"Total downloaded files: {len(files)}")
