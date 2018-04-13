"""Download, extract and copy protemplates to autobash bin dir."""
import argparse
import os
from pprint import pformat

import requests

GITHUB_API_URL = "https://api.github.com/repos"
OWNER = "ansrivas"
REPO = "protemplates"
BINARY = "protemplates"


def join_url_words(*words):
    """Join URL words."""
    return "/".join(words)


def main(local_directory):
    """Download, extract and copy protemplates to autobash bin dir."""
    src_directory = os.path.join(local_directory, 'src')
    bin_directory = os.path.join(local_directory, 'bin')
    ############################################################################
    # Get latest release
    # GET /repos/:owner/:repo/releases/latest
    ############################################################################
    print("{}: Fetching latest release ID".format(REPO))

    latest_release_url = join_url_words(GITHUB_API_URL, OWNER, REPO, "releases", "latest")
    print("{}: latest_release_url: {}".format(REPO, latest_release_url))

    r = requests.get(latest_release_url)
    try:
        json_response = r.json()
        assets = json_response['assets']
        assets_urls = [asset['browser_download_url'] for asset in assets]
    except Exception:
        print("Error: Received response from request: {}".format(r.text))
        raise

    ############################################################################
    # Download "linux-amd64.tgz" asset
    ############################################################################
    download_url = [asset_url for asset_url in assets_urls if "linux-amd64.tgz" in asset_url][0]
    print("{}: download_url: {}".format(REPO, download_url))

    download_filename = download_url.split('/')[-1]
    print("{}: download_filename: {}".format(REPO, download_filename))

    dest_filename = os.path.join(src_directory, download_filename)
    print("{}: downloading file to: {}".format(REPO, dest_filename))
    os.system("wget {} -O {}".format(download_url, dest_filename))

    ############################################################################
    # Extract
    ############################################################################
    print("{}: extracting file to: {}".format(REPO, src_directory))
    os.system("tar xvzf {} -C {}".format(dest_filename, src_directory))

    ############################################################################
    # Copy tp bin
    ############################################################################
    extracted_directory = dest_filename[:-4]
    extracted_filename = os.path.join(extracted_directory, "protemplates-linux-amd64")
    print("{}: copying file to bin: {}".format(REPO, extracted_filename))
    dest_binary_filename = os.path.join(bin_directory, BINARY)
    os.system("cp {} {}".format(extracted_filename, dest_binary_filename))
    os.system("chmod u+x {}".format(dest_binary_filename))
    print("{}: successfully copied binary to: {}".format(REPO, dest_binary_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_directory', action='store', dest='local_directory',
                        required=True, help='The autobash local directory.')
    command_args = parser.parse_args()

    main(command_args.local_directory)
