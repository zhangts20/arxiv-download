import argparse

from arxiv_download.client import Client


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query",
                        type=str,
                        default="LLM",
                        help="The keyword of papers to query and download")
    parser.add_argument("--max-results",
                        type=int,
                        default=10,
                        help="The number of files to download")
    parser.add_argument(
        "--sort-by",
        type=str,
        default="lastUpdatedDate",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
        help="The options to sort search results")
    parser.add_argument("--sort-order",
                        type=str,
                        default="descending",
                        choices=["ascending", "descending"],
                        help="The options to order search results")
    parser.add_argument("--max-workers",
                        type=int,
                        default=2,
                        help="The max workers to download files")
    parser.add_argument("--output-dir",
                        type=str,
                        default="./output",
                        help="The output directory to save files")
    parser.add_argument("--use-proxy",
                        action="store_true",
                        help="Whether to use proxy to download files")
    parser.add_argument("--num-retries",
                        type=int,
                        default=5,
                        help="The number of retries to search results")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    client = Client(query=args.query,
                    max_results=args.max_results,
                    max_workers=args.max_workers,
                    output_dir=args.output_dir,
                    sort_by=args.sort_by,
                    sort_order=args.sort_order,
                    num_retries=args.num_retries)
    client.download_files(args.use_proxy)
