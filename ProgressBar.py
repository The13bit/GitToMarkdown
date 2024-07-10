from git import RemoteProgress
from tqdm import tqdm
class ClonedProgreeBar(RemoteProgress):
    def __init__(self) -> None:
        super().__init__()
        self.pbar=tqdm()
    def update(self, op_code: int, cur_count: str | float, max_count: str | float | None = None, message: str = "") -> None:
        self.pbar.total=max_count
        self.pbar.n=cur_count
        self.pbar.refresh()
