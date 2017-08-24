import requests
import tempfile

from tqdm import tqdm

def download(url):
    """
        Download url, returns false if fails, bytes otherwise
    """
    request = requests.head(url)
    request.raise_for_status()
    content_size = int(request.headers['content-length'])

    response = requests.get(url, stream=True)

    # Initiate progressbar
    task = tqdm(
        desc="Downloading",
        total=content_size,
        unit='B',
        unit_scale=True
    )

    with task as t:
        with tempfile.TemporaryFile() as temp:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    temp.write(chunk)
                    t.update(len(chunk))
            # Go at the beginning and read the file
            temp.seek(0)
            return temp.read()

    return false
