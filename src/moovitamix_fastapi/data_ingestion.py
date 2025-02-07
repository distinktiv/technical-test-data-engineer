import logging
import pandas as pd
import httpx

logging.basicConfig(level=logging.INFO)


# ---------------------------------------------------------------------
# Batch Processing: Methods to fetch data in batches
# ---------------------------------------------------------------------
async def fetch_all_data():
    await fetch_and_save("tracks")
    await fetch_and_save("users")
    await fetch_and_save("listen_history", True)
    logging.info("All data fetched successfully.")


async def fetch_and_save(endpoint: str, allow_duplicates: bool = False):

    all_data = await fetch_batch(endpoint)

    if all_data:
        return await process_and_save_data(all_data, allow_duplicates)
    else:
        logging.info(f"No data returned from endpoint '{endpoint}' to process.")


async def fetch_batch(endpoint: str, batch_size: int = 10):
    base_url = "http://127.0.0.1:8000"
    all_data = []
    page = 1

    async with httpx.AsyncClient() as client:
        while True:
            url = f"{base_url}/{endpoint}?page={page}&size={batch_size}"
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                if len(data['items']) == 0:
                    break
                all_data.extend(data['items'])
                page += 1
            except httpx.ReadTimeout:
                logging.error("Timeout occurred while fetching data.")
                raise
            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logging.error(f"An unexpected error occurred: {str(e)}")
                raise

    return all_data


async def process_and_save_data(data, allow_duplicates: bool = False, unique_key: str = "id"):
    # Create a DataFrame from the items
    df = pd.DataFrame(data)

    # Remove duplicate items based on the unique key
    if not allow_duplicates:
        df = df.drop_duplicates(subset=[unique_key], keep="last")

    logging.info(f"Saved {len(df)} unique records to dataframe")
    return df
