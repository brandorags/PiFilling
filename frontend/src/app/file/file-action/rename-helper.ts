import { Injectable } from '@angular/core';

import { FileService } from '../file.service';
import { FileMetadata } from 'src/app/models/file/file-metadata';
import { FileRename } from 'src/app/models/file/file-rename';

@Injectable({
  providedIn: 'root'
})
export class RenameHelper {

  constructor(private fileService: FileService) { }

  renameFile(fileSelected: FileMetadata, newFilename: string, files: FileMetadata[], folderPath: string) {
    let fileToRename = new FileRename();
    fileToRename.oldFilename = fileSelected.filename;
    fileToRename.newFilename = newFilename + fileSelected.fileType;
    fileToRename.path = folderPath;

    this.fileService.renameFile(fileToRename).subscribe(
      newName => {
        for (let f of files) {
          if (f.filename === fileToRename.oldFilename) {
            f.filename = newName;
            break;
          }
        }
      },
      error => {
        console.log(error);
      }
    );
  }

}
