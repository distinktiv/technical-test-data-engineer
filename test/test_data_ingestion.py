from unittest.mock import patch, AsyncMock

import httpx
import pandas as pd
import pytest

from src.moovitamix_fastapi.data_ingestion import fetch_and_save, fetch_batch


@pytest.mark.asyncio
async def test_ingesting_tracks_data_flow():
    mock_data = [
        {"id": 1, "name": "Track 1", "artist": "artiste1"},
        {"id": 2, "name": "Track 2", "artist": "artiste2"},
        {"id": 3, "name": "Track 3", "artist": "artiste3"},
    ]
    mock_tracks_df = pd.DataFrame(mock_data)

    with patch("src.moovitamix_fastapi.data_ingestion.fetch_batch", new_callable=AsyncMock) as mock_fetch_batch:
        mock_fetch_batch.side_effect = mock_data

        with patch("src.moovitamix_fastapi.data_ingestion.process_and_save_data",
                   new_callable=AsyncMock) as mock_process_and_save_data:
            mock_process_and_save_data.return_value = mock_tracks_df

            result_df = await fetch_and_save("tracks")

            mock_fetch_batch.assert_called_once_with("tracks")
            assert isinstance(result_df, pd.DataFrame)
            assert len(result_df) == 3
            assert set(result_df['id']) == {1, 2, 3}


@pytest.mark.asyncio
async def test_fetch_batch_timeout():
    with patch("httpx.AsyncClient.get", side_effect=httpx.ReadTimeout("Timeout occurred")):
        with pytest.raises(httpx.ReadTimeout) as e:
            await fetch_batch("tracks")
        assert str(e.value) == "Timeout occurred"


@pytest.mark.asyncio
async def test_fetch_batch_http_error():
    with patch("httpx.AsyncClient.get",
               side_effect=httpx.HTTPStatusError(
                   "Not Found", request=AsyncMock(), response=AsyncMock(status_code=404))):

        with pytest.raises(httpx.HTTPStatusError) as e:
            await fetch_batch("tracks")
        assert e.value.response.status_code == 404


@pytest.mark.asyncio
async def test_fetch_batch_other_error():
    with patch("httpx.AsyncClient.get", side_effect=Exception("Unexpected error")):
        with pytest.raises(Exception) as e:
            await fetch_batch("tracks")
        assert str(e.value) == "Unexpected error"
