import { Injectable } from '@angular/core';

import { FileService } from '../file.service';

import { FileDelete } from 'src/app/models/file/file-delete';
import { FileMetadata } from 'src/app/models/file/file-metadata';

@Injectable({
  providedIn: 'root'
})
export class DeleteHelper {

  constructor(private fileService: FileService) { }

  deleteFiles(files: FileMetadata[], folderPath: string): void {
    let filesToDelete = [];
    for (let f of files) {
      if (f.isSelected) {
        let fileToDelete = new FileDelete();
        fileToDelete.filename = f.filename;
        fileToDelete.path = folderPath;
        fileToDelete.isDirectory = f.isDirectory;

        filesToDelete.push(fileToDelete);
      }
    }

    this.fileService.deleteFiles(filesToDelete).subscribe(
      () => {
        for (let deletedFile of filesToDelete) {
          let deletedFileIndex = files.findIndex(f => f.filename === deletedFile.filename);
          if (deletedFileIndex !== -1) {
            files.splice(deletedFileIndex, 1);
          }
        }
      },
      error => {
        console.log(error);
      }
    );
  }

}
