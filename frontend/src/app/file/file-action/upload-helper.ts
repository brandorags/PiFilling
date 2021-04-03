import { Injectable } from '@angular/core';
import { HttpEventType } from '@angular/common/http';

import { FileService } from '../file.service';
import { SessionTimerService } from 'src/app/common/session-timer.service';

import { Folder } from 'src/app/models/file/folder';
import { QueuedFile } from 'src/app/models/file/queued-file';
import { FileMetadata } from 'src/app/models/file/file-metadata';

@Injectable({
  providedIn: 'root'
})
export class UploadHelper {

  private files: FileMetadata[];
  private queuedFiles: QueuedFile[];
  private queuedFiledCount = 0;

  constructor(
    private fileService: FileService,
    private sessionTimerService: SessionTimerService
  ) { }

  uploadFiles(filesToUpload: any, files: FileMetadata[], queuedFiles: QueuedFile[],
    queuedFileCount: number, folderPath: string): void {
    this.files = files;
    this.queuedFiles = queuedFiles;
    this.queuedFiledCount = queuedFileCount;

    for (let i = 0; i < filesToUpload.length; i++) {
      let entry = filesToUpload[i];
      if (entry.isFile || entry instanceof File) {
        this.prepareFileForUpload(entry, folderPath);
      } else if (entry.isDirectory) {
        this.prepareDirectoryForUpload(entry, folderPath);
      }
    }
  }

  private prepareFileForUpload(fileEntry: any, folderPath: string): void {
    let filePath = `${folderPath}/${fileEntry.name}`;
    let filePathWithFilenameRemoved = filePath.slice(0, filePath.lastIndexOf('/'));

    if (fileEntry instanceof File) {
      let formData = new FormData();
      formData.append(fileEntry.name, fileEntry, fileEntry.name);

      this.uploadFile(fileEntry.name, formData, folderPath, filePathWithFilenameRemoved);
    } else {
      let fileEntryPromise = new Promise((resolve, reject) => {
        fileEntry.file(
          (file: File) => {
            resolve(file);
          },
          (error: any) => {
            reject(error);
          }
        );
      });
  
      fileEntryPromise.then((file: File) => {
        let formData = new FormData();
        formData.append(file.name, file, file.name);
  
        this.uploadFile(file.name, formData, folderPath, filePathWithFilenameRemoved);
      });
    }
  }

  private prepareDirectoryForUpload(directoryEntry: any, folderPath: string): void {
    let directoryPath = folderPath + directoryEntry.fullPath;
    let directoryPathWithLastFolderRemoved = directoryPath.slice(0, directoryPath.lastIndexOf('/'));
    let directoryName = directoryEntry.name;

    let folder = new Folder();
    folder.name = directoryName;
    folder.path = directoryPathWithLastFolderRemoved;

    this.fileService.createNewFolder(folder).subscribe(
      createdFolder => {
        let folderMetadata = new FileMetadata(createdFolder.name, 0, null, null, true, false);

        // only add to the files list if the folder is in the current path
        if (directoryPathWithLastFolderRemoved === folderPath) {
          this.files.push(folderMetadata);
        }
      },
      error => {
        console.log(error);
      }
    )
    .add(() => {
      let directoryReader = directoryEntry.createReader();
      let directoryReaderPromise = new Promise((resolve, reject) => {
        directoryReader.readEntries(
          (entries: any) => {
            resolve(entries);
          },
          (error: any) => {
            reject(error);
          }
        );
      });

      directoryReaderPromise.then((entries: any) => {
        for (let entry of entries) {
          if (entry.isFile) {
            let filePath = folderPath + entry.fullPath;
            let filePathWithFilenameRemoved = filePath.slice(0, filePath.lastIndexOf('/'));
            this.prepareFileForUpload(entry, filePathWithFilenameRemoved);
          } else if (entry.isDirectory) {
            this.prepareDirectoryForUpload(entry, folderPath);
          }
        }
      });
    });
  }

  private uploadFile(filename: string, formData: FormData, folderPath: string,
    filePathWithFilenameRemoved: string): void {
    let isFileInCurrentFolderPath = (filePathWithFilenameRemoved === folderPath);

    let queuedFile = new QueuedFile(isFileInCurrentFolderPath ? filename : `${filePathWithFilenameRemoved}/${filename}`, 0);
    this.queuedFiles.push(queuedFile);
    this.queuedFiledCount++;

    this.fileService.uploadFile(formData, filePathWithFilenameRemoved).subscribe(
      event => {
        switch (event.type) {
          case HttpEventType.UploadProgress:
            queuedFile.uploadProgress = Math.round(100 * event.loaded / event.total);
            break;
          case HttpEventType.Response:
            let fileMetadata = new FileMetadata(event.body.filename, event.body.fileSize,
              event.body.fileType, event.body.modifiedDate, event.body.isDirectory, false);
            this.queuedFiledCount--;

            if (isFileInCurrentFolderPath) {
              this.files.push(fileMetadata);
            }
        }

        this.sessionTimerService.refreshTimer();
      },
      error => {
        console.log(error);
      }
    );
  }

}
