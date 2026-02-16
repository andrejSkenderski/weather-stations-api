import os
import pandas as pd

from models.dtos import CityTemperatureStatsCacheEntryDto


class DataProcessingService:
    def __init__(self, csv_file_path: str, chunk_size: int):
        self._csv_file_path = csv_file_path
        self._chunk_size = chunk_size

    def get_file_modified_time(self) -> float:
        return os.path.getmtime(self._csv_file_path)

    def load_data_and_calculate_stats(self) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        city_aggregates: dict[str, dict] = {}

        for chunk in pd.read_csv(self._csv_file_path, delimiter=';', chunksize=self._chunk_size):
            self._process_chunk(chunk, city_aggregates)

        return self._finalize_stats(city_aggregates)

    @staticmethod
    def _process_chunk(chunk: pd.DataFrame, city_aggregates: dict[str, dict]) -> None:
        chunk_agg = chunk.groupby('city')['temp_celsius'].agg(['sum', 'count', 'min', 'max'])

        for city, row in chunk_agg.iterrows():
            if city not in city_aggregates:
                city_aggregates[city] = {
                    'sum': 0.0,
                    'count': 0,
                    'min': float('inf'),
                    'max': float('-inf'),
                }

            agg = city_aggregates[city]
            agg['sum'] += row['sum']
            agg['count'] += row['count']
            agg['min'] = min(agg['min'], row['min'])
            agg['max'] = max(agg['max'], row['max'])

    @staticmethod
    def _finalize_stats(city_aggregates: dict[str, dict]) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        return {
            city: CityTemperatureStatsCacheEntryDto(
                min_temp=round(agg['min'], 2),
                max_temp=round(agg['max'], 2),
                avg_temp=round(agg['sum'] / agg['count'], 2),
            )
            for city, agg in city_aggregates.items()
        }
