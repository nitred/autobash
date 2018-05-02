"""Download, extract and copy protemplates to autobash bin dir."""
import argparse
import os

import requests

GITHUB_API_URL = "https://api.github.com/repos"
OWNER = "bazelbuild"
REPO = "bazel"
BINARY = "bazel"                                # What is the final binary supposed to be named?
ASSET_REGEX = "installer-linux-x86_64.sh"       # What is the regex pattern of the asset on github releases?
EXTRACTED_BINARY_ALIAS = "bazel"                # After extraction, what is the name of the original extracted binary called?


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
    download_url = [asset_url for asset_url in assets_urls if ASSET_REGEX in asset_url][0]
    print("{}: download_url: {}".format(REPO, download_url))

    download_basename = download_url.split('/')[-1]
    print("{}: download_basename: {}".format(REPO, download_basename))

    download_filename = os.path.join(src_directory, download_basename)
    print("{}: downloading file to: {}".format(REPO, download_filename))
    os.system("wget -c {} -O {}".format(download_url, download_filename))

    ############################################################################
    # Installation script
    ############################################################################
    print("{}: running installation script: {}".format(REPO, download_filename))
    os.system("chmod u+x {}".format(download_filename))
    # installs things in /bin and /lib directories
    autobash_local_directory = os.path.dirname(bin_directory)
    os.system("bash {} --prefix={}".format(download_filename, autobash_local_directory))
    dest_binary_filename = os.path.join(bin_directory, BINARY)
    print("{}: successfully copied binary to: {}".format(REPO, dest_binary_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_directory', action='store', dest='local_directory',
                        required=True, help='The autobash local directory.')
    command_args = parser.parse_args()

    main(command_args.local_directory)
