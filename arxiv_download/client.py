import os
import requests
import feedparser

from typing import List
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


@dataclass
class Entry:
    # the arxiv-id of article
    arxiv_id: str
    # the title of article
    title: str
    # the abstract of article
    summary: str
    # the authors of article
    authors: List[str]
    # the links of article, used to download pdf
    links: List[dict]

    @property
    def num_authors(self) -> int:
        return len(self.authors)

    def download_link(self, use_proxy: bool) -> str:
        dlink: str = None
        for link in self.links:
            if "title" in link and link["title"] == "pdf":
                dlink = link["href"]
        assert dlink is not None, "Key = href not found in links."
        if use_proxy:
            dlink = dlink.replace("arxiv.org", "xxx.itp.ac.cn")

        return dlink


class Client:

    def __init__(
        self,
        query: str = "electron",
        start_id: int = 0,
        max_results: int = 10,
        max_workers: int = 8,
        output_dir: str = "./output",
    ) -> None:
        # base api query url
        base_url = "http://export.arxiv.org/api/query?"

        # the parameters of query search
        self.query = query
        self.max_results = max_results
        parameters = f"search_query=all:{query}&start={start_id}&max_results={max_results}"

        # the request url
        self.request_url = f"{base_url}{parameters}"

        # the max workers to download files
        self.max_workers = max_workers

        # the output directory to save download files
        self.output_dir = output_dir

    def get_output_paths(self, entry: Entry) -> str:
        filename = entry.arxiv_id.split("/")[-1].strip()

        return os.path.join(os.getcwd(), self.output_dir, filename + ".pdf")

    @staticmethod
    def download_file(url: str, output_path) -> None:
        response = requests.get(url, stream=True)
        assert response.status_code == 200
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

    def download_files(self, use_proxy: bool = False) -> None:
        print(f"[INFO] the request url: {self.request_url}")
        response: dict = feedparser.parse(self.request_url)
        assert response["status"] == 200

        # get entries, each entry is a query result
        assert "entries" in response.keys()
        query_entries: List[dict] = response["entries"]
        num_results = len(query_entries)
        if num_results != self.max_results:
            print(
                f"[WARNING] expected {self.max_results} results, found {num_results}."
            )

        entries: List[Entry] = []
        for entry in query_entries:
            entries.append(
                Entry(entry["id"], entry["title"], entry["summary"],
                      entry["authors"], entry["links"]))

        # download files parallelly
        print(
            f"[INFO] begin to download {num_results} files about {self.query} and save to {self.output_dir}"
        )
        urls = [e.download_link(use_proxy) for e in entries]
        output_paths = [self.get_output_paths(e) for e in entries]
        with ProcessPoolExecutor(max_workers=self.max_workers) as e:
            list(
                tqdm(e.map(self.download_file, urls, output_paths),
                     total=num_results,
                     desc="Downloading files"))
        print(
            f"[INFO] {num_results} files have been downloaded to {self.output_dir}"
        )
