import os
import pathlib

from datetime import datetime
from app.models.file_metadata import FileMetadata


class DirectoryContentParser(object):

    @staticmethod
    def parse_directory_content(path):
        file_metadata_list = []

        with os.scandir(path) as dir_content:
            for file in dir_content:
                file_stat = file.stat()

                filename = file.name
                file_size = file_stat.st_size
                file_type = pathlib.Path(filename).suffix
                modified_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
                is_dir = file.is_dir()

                file_metadata = FileMetadata(filename=filename, file_size=file_size, file_type=file_type,
                                             modified_date=modified_date, is_directory=is_dir)
                file_metadata_list.append(file_metadata)

        return sorted(file_metadata_list, key=lambda fm: fm.filename)

    @staticmethod
    def get_file(filename_with_path):
        file = pathlib.Path(filename_with_path)
        file_stat = file.stat()

        filename = file.name
        file_size = file_stat.st_size
        file_type = file.suffix
        modified_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S')
        is_dir = file.is_dir()

        file_metadata = FileMetadata(filename=filename, file_size=file_size, file_type=file_type,
                                     modified_date=modified_date, is_directory=is_dir)

        return file_metadata
