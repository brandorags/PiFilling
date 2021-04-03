import { Injectable } from '@angular/core';

import { FileService } from '../file.service';

import { FileMove } from 'src/app/models/file/file-move';
import { FileMetadata } from 'src/app/models/file/file-metadata';

@Injectable({
  providedIn: 'root'
})
export class MoveHelper {

  constructor(private fileService: FileService) { }

  moveFiles(files: FileMetadata[], folderPath: string, destinationPath: string): void {
    let filesToMove = [];
    for (let f of files) {
      if (f.isSelected) {
        let fileToMove = new FileMove();
        fileToMove.filename = f.filename;
        fileToMove.sourcePath = `${folderPath}/${f.filename}`;
        fileToMove.destinationPath = destinationPath;

        filesToMove.push(fileToMove);
      }
    }

    this.fileService.moveFiles(filesToMove).subscribe(
      () => {
        for (let movedFile of filesToMove) {
          let movedFileIndex = files.findIndex(f => f.filename === movedFile.filename);
          if (movedFileIndex !== -1) {
            files.splice(movedFileIndex, 1);
          }
        }
      },
      error => {
        console.log(error);
      }
    );
  }

}
