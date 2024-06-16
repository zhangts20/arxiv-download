import argparse

from arxiv_download.client import Client


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query",
                        type=str,
                        default="LLM",
                        help="The keyword to papers to query and download")
    parser.add_argument("--max-results",
                        type=int,
                        default=10,
                        help="The number of files to download")
    parser.add_argument("--max-workers",
                        type=int,
                        default=2,
                        help="The max workers to download files")
    parser.add_argument("--output-dir",
                        type=str,
                        default="./output",
                        help="The output directory to save files")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    client = Client(query=args.query,
                    max_results=args.max_results,
                    max_workers=args.max_workers,
                    output_dir=args.output_dir)
    client.download_files()
