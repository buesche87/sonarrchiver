import os
import requests
import urllib3
import logging

# Setup logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
SONARR_API_URL = os.environ["SONARR_API_URL"]
SONARR_API_KEY = os.environ["SONARR_API_KEY"]
TEST_SERIES_TITLE = os.getenv("TEST_SERIES_TITLE", "")

# Gather 'tag:/folder' pairs
tag_folder_map = []
index = 1

while True:
    pair = os.getenv(f"TAG_FOLDER_PAIR_{index}")
    if not pair:
        break
    if ":" in pair:
        tag, folder = pair.split(":", 1)
        tag_folder_map.append((tag.strip(), folder.strip()))
    else:
        logging.warning(f"Invalid format in TAG_FOLDER_PAIR_{index}, expected 'tag:/path'")
    index += 1

# Headers for API requests
headers = {
    'X-Api-Key': SONARR_API_KEY
}

# Log request and response details
def log_request_response(response):
    logging.debug(f"Request URL: {response.request.url}")
    logging.debug(f"Request Method: {response.request.method}")
    logging.debug(f"Request Headers: {response.request.headers}")
    if response.request.body:
        logging.debug(f"Request Body: {response.request.body}")
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Content: {response.text}")

# Get the list of series from Sonarr
def get_series():
    logging.info("Fetching series from Sonarr...")
    url = f"{SONARR_API_URL}/series"
    response = requests.get(url, headers=headers, verify=False)
    log_request_response(response)
    return response.json()

# Get the list of tags from Sonarr
def get_tags():
    logging.info("Fetching tags from Sonarr...")
    url = f"{SONARR_API_URL}/tag"
    response = requests.get(url, headers=headers, verify=False)
    log_request_response(response)
    return {tag['id']: tag['label'] for tag in response.json()}

# Get root folders from Sonarr
def get_root_folders():
    logging.info("Fetching root folders from Sonarr...")
    url = f"{SONARR_API_URL}/rootfolder"
    response = requests.get(url, headers=headers, verify=False)
    log_request_response(response)
    return response.json()

# Update the series root folder and path
def update_series_root_folder(series, new_root_folder_id, new_root_folder_path):
    logging.info(f"Updating root folder for series: {series['title']}")
    series['rootFolderPath'] = new_root_folder_path
    series['rootFolderId'] = new_root_folder_id
    series['path'] = f"{new_root_folder_path}/{series['title']}"  # Update the path as well

    url = f"{SONARR_API_URL}/series/{series['id']}"
    response = requests.put(
        url,
        json=series,
        headers=headers,
        params={'moveFiles': True},
        verify=False
    )
    log_request_response(response)
    return response.status_code

# Main script execution
def main():
    series_list = get_series()
    tags = get_tags()
    root_folders = get_root_folders()

    # Map tag names to IDs
    tag_ids = {name: id for id, name in tags.items()}

    for tag_name, new_root_folder in tag_folder_map:
        tag_id = tag_ids.get(tag_name)
        if tag_id is None:
            logging.warning(f"Tag '{tag_name}' not found in Sonarr. Skipping.")
            continue

        for series in series_list:
            if TEST_SERIES_TITLE and series['title'] != TEST_SERIES_TITLE:
                continue

            logging.debug(f"Processing series: {series['title']}")
            if tag_id in series.get('tags', []) and series['rootFolderPath'] == new_root_folder:
                logging.info(f"Series '{series['title']}' with tag '{tag_name}' is already in the correct root folder.")
            elif tag_id in series.get('tags', []):
                status_code = update_series_root_folder(series, tag_id, new_root_folder)
                if status_code == 202:
                    logging.info(f"Updated root folder for '{series['title']}' to '{new_root_folder}'")
                else:
                    logging.error(f"Failed to update '{series['title']}': Status {status_code}")
            else:
                logging.debug(f"Series '{series['title']}' does not have tag '{tag_name}'")

if __name__ == "__main__":
    main()
