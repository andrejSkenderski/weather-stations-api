import os
import pandas as pd

from models.dtos import CityTemperatureStatsCacheEntryDto


class DataProcessingService:
    def __init__(self, csv_file_path: str):
        self._csv_file_path = csv_file_path

    def get_file_modified_time(self) -> float:
        return os.path.getmtime(self._csv_file_path)

    def load_data_and_calculate_stats(self) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        df = self._load_csv()
        stats = self._calculate_stats(df)
        return stats

    def _load_csv(self) -> pd.DataFrame:
        return pd.read_csv(self._csv_file_path, delimiter=';')

    @staticmethod
    def _calculate_stats(df: pd.DataFrame) -> dict[str, CityTemperatureStatsCacheEntryDto]:
        agg = df.groupby('city')['temp_celsius'].agg(['min', 'max', 'mean'])
        agg = agg.round(2)

        return {
            city: CityTemperatureStatsCacheEntryDto(
                min_temp=row['min'],
                max_temp=row['max'],
                avg_temp=row['mean']
            )
            for city, row in agg.iterrows()
        }
