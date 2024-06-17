# Usage
```
usage: main.py [-h] [--query QUERY] [--max-results MAX_RESULTS] [--sort-by {relevance,lastUpdatedDate,submittedDate}] [--sort-order {ascending,descending}] [--max-workers MAX_WORKERS] [--output-dir OUTPUT_DIR] [--use-proxy]
              [--num-retries NUM_RETRIES]

options:
  -h, --help            show this help message and exit
  --query QUERY         The keyword of papers to query and download
  --max-results MAX_RESULTS
                        The number of files to download
  --sort-by {relevance,lastUpdatedDate,submittedDate}
                        The options to sort search results
  --sort-order {ascending,descending}
                        The options to order search results
  --max-workers MAX_WORKERS
                        The max workers to download files
  --output-dir OUTPUT_DIR
                        The output directory to save files
  --use-proxy           Whether to use proxy to download files
  --num-retries NUM_RETRIES
                        The number of retries to search results
```
# References
https://info.arxiv.org/help/api/user-manual.html