import os
import pathlib

from datetime import datetime
from app.models.file_metadata import FileMetadata


class DirectoryContentParser(object):

    @staticmethod
    def parse_directory_content(path):
        file_metadata_list = []

        with os.scandir(path) as dir_content:
            for entry in dir_content:
                entry_stats = entry.stat()

                file_name = entry.name
                file_size = entry_stats.st_size
                file_type = pathlib.Path(file_name).suffix
                modified_date = datetime.fromtimestamp(entry_stats.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
                is_dir = entry.is_dir()

                file_metadata = FileMetadata(filename=file_name, file_size=file_size, file_type=file_type,
                                             modified_date=modified_date, is_directory=is_dir)
                file_metadata_list.append(file_metadata)

        return file_metadata_list
