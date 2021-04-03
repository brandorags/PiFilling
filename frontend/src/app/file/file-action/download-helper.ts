import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';

import { saveAs } from 'file-saver';

import { FileService } from '../file.service';
import { SessionTimerService } from 'src/app/common/session-timer.service';

import { FileDownload } from 'src/app/models/file/file-download';
import { FileDelete } from 'src/app/models/file/file-delete';
import { FileMetadata } from 'src/app/models/file/file-metadata';

@Injectable({
  providedIn: 'root'
})
export class DownloadHelper {

  constructor(
    private fileService: FileService,
    private sessionTimerService: SessionTimerService
  ) { }

  downloadFiles(files: FileMetadata[], folderPath: string): void {
    let filesToDownload = [];
    for (let f of files) {
      if (!f.isSelected) {
        continue;
      }

      filesToDownload.push(f);
    }

    let fileDownload = new FileDownload();
    fileDownload.path = folderPath;
    fileDownload.files = filesToDownload;

    let filename: string;
    this.fileService.downloadFiles(fileDownload)
      .subscribe(response => {
        if (response instanceof HttpResponse) {
          filename = this.saveFile(response);
        }

        this.sessionTimerService.refreshTimer();
      })
      .add(() => {
        if (filename && filename.split('.').pop() === 'zip') {
          let fileToDelete = new FileDelete();
          fileToDelete.filename = filename;
          fileToDelete.path = '';
          fileToDelete.isDirectory = false;

          this.fileService.deleteFiles([fileToDelete]).subscribe();
        }
      });
  }

  private saveFile(response: HttpResponse<any>): string {
    let blob = new Blob([response.body]);
    let contentDispositionHeader = response.headers.get('Content-Disposition');
    let headerRegex = /filename=([^;]+)/ig.exec(contentDispositionHeader);
    let filename = (headerRegex.length > 1) ? headerRegex[1].trim() : 'file';

    saveAs(blob, filename);

    return filename;
  }

}
