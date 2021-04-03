/**
 * Copyright Brandon Ragsdale
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


import { Component, OnInit, HostListener } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { FileService } from './file.service';
import { UploadHelper } from './file-action/upload-helper';
import { DownloadHelper } from './file-action/download-helper';
import { RenameHelper } from './file-action/rename-helper';
import { MoveHelper } from './file-action/move-helper';
import { DeleteHelper } from './file-action/delete-helper';

import { RenameFileDialogComponent } from './rename-file-dialog/rename-file-dialog.component';
import { DeleteFileDialogComponent } from './delete-file-dialog/delete-file-dialog.component';
import { MoveFileDialogComponent } from './move-file-dialog/move-file-dialog.component';

import { Constants } from '../common/constants';
import { FileMetadata } from '../models/file/file-metadata';
import { QueuedFile } from '../models/file/queued-file';
import { Folder } from '../models/file/folder';
import { FolderPath } from '../models/file/folder-path';

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.scss']
})
export class FileComponent implements OnInit {

  files: FileMetadata[] = [];
  loadingFiles = false;
  filesSelectedCount = 0;

  queuedFiles: QueuedFile[] = [];
  queuedFilesRemaining = 0;

  folderPath: FolderPath = new FolderPath();

  fileStorageBaseUrl = Constants.fileStorageBaseUrl;

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
  .pipe(
    map(result => result.matches)
  );

  constructor(
    private breakpointObserver: BreakpointObserver,
    private snackBar: MatSnackBar,
    private dialog: MatDialog,
    private fileService: FileService,
    private uploadHelper: UploadHelper,
    private downloadHelper: DownloadHelper,
    private renameHelper: RenameHelper,
    private moveHelper: MoveHelper,
    private deleteHelper: DeleteHelper
  ) {
    this.fileService.fileListEventEmitter.subscribe(fileList => {
      this.uploadFiles(fileList);
    });

    this.fileService.newFolderEventEmitter.subscribe(folderName => {
      let newFolder = new Folder();
      newFolder.name = folderName;
      newFolder.path = this.folderPath.toString();

      this.createNewFolder(newFolder);
    });
  }

  ngOnInit() {
    this.getFiles(this.folderPath.toString());
    this.initFileDrop();
  }

  navigateToHomeFolder(): void {
    if (this.folderPath.pathArray.length > 0) {
      this.folderPath.pathArray = [];
      this.getFiles(this.folderPath.toString());
    } 
  }

  navigateFromFolderPath(folderIndex: number): void {
    this.folderPath.pathArray.length = folderIndex + 1;
    this.getFiles(this.folderPath.toString());
  }

  navigateFromFolderCard(folderName: string): void {
    this.folderPath.pathArray.push(folderName);
    this.getFiles(this.folderPath.toString());
  }

  onCardClick(event: any, file: FileMetadata, isRightClick: boolean): void {
    event.stopPropagation();

    if (event.shiftKey) {
      this.multiSelectCards(file);
    } else if (event.ctrlKey || event.metaKey) {
      this.singleSelectCard(file, isRightClick);
    } else {
      this.unselectAllCards();
      this.singleSelectCard(file, isRightClick);
    }
  }

  singleSelectCard(file: FileMetadata, isRightClick: boolean): void {
    let selectedCardEl = document.getElementById(`file_${file.filename}`);

    let fileCardSelectedCssClass = 'file-card-selected';
    let isCardAlreadySelected = selectedCardEl.classList.contains(fileCardSelectedCssClass);

    if (isCardAlreadySelected) {
      if (isRightClick) {
        return;
      }

      selectedCardEl.classList.remove(fileCardSelectedCssClass);
      file.isSelected = false;
      this.filesSelectedCount--;

      selectedCardEl.blur();
    } else {
      selectedCardEl.classList.add(fileCardSelectedCssClass);
      file.isSelected = true;
      this.filesSelectedCount++;
    }
  }

  multiSelectCards(file: FileMetadata): void {
    let selectedCardIndices = [];
    for (let i = 0; i < this.files.length; i++) {
      let f = this.files[i];
      if (f.isSelected) {
        selectedCardIndices.push(i);
      }
    }

    let selectedCardIndex = this.files.findIndex(f => f.filename === file.filename);
    let firstCardToSelectIndex: number;
    let lastCardToSelectIndex: number;
    if (selectedCardIndex < selectedCardIndices[0]) {
      firstCardToSelectIndex = selectedCardIndex;
      lastCardToSelectIndex = selectedCardIndices[0];
    } else {
      firstCardToSelectIndex = selectedCardIndices[0];
      lastCardToSelectIndex = selectedCardIndex;
    }

    for (let i = 0; i < this.files.length; i++) {
      let f = this.files[i];
      let cardEl = document.getElementById(`file_${f.filename}`);
      let fileCardSelectedCssClass = 'file-card-selected';

      if (i >= firstCardToSelectIndex && i <= lastCardToSelectIndex) {
        cardEl.classList.add(fileCardSelectedCssClass);
        f.isSelected = true;
        this.filesSelectedCount++;
      } else {
        cardEl.classList.remove(fileCardSelectedCssClass);
        f.isSelected = false;
        this.filesSelectedCount--;
      }
    }
  }

  @HostListener('document:keydown', ['$event'])
  selectAllCards(event: KeyboardEvent): void {
    // select all cards when the user presses ctrl+a or cmd+a
    if ((event.ctrlKey || event.metaKey) && event.keyCode === 65) {
      let cardEls = document.getElementsByClassName('file-card');
      for (let cardEl of cardEls as any) {
        cardEl.classList.add('file-card-selected');
      }

      for (let f of this.files) {
        f.isSelected = true;
      }

      this.filesSelectedCount = this.files.length;
    }
  }

  unselectAllCards(): void {
    let cardEls = document.getElementsByClassName('file-card');
    for (let cardEl of cardEls as any) {
      cardEl.classList.remove('file-card-selected');
    }

    for (let f of this.files) {
      f.isSelected = false;
    }

    this.filesSelectedCount = 0;
  }

  getFiles(path: string): void {
    this.loadingFiles = true;
    this.files = [];

    this.fileService.getFilesForPath(path).subscribe(
      files => {
        this.files = files;
      },
      error => {
        console.log(error);
      }
    ).add(() => this.loadingFiles = false);
  }

  clearQueuedFiles(): void {
    this.queuedFiles = [];
  }

  uploadFiles(event: any): void {
    let items = (event instanceof DragEvent) ? event.dataTransfer.items : event;
    let filesToUpload = [];
    for (let i = 0; i < items.length; i++) {
      let item = items[i];
      if (item instanceof DataTransferItem && item.kind === 'file') {
        let entry = item.webkitGetAsEntry();
        filesToUpload.push(entry);
      } else {
        filesToUpload.push(item);
      }
    }

    this.uploadHelper.uploadFiles(filesToUpload, this.files, this.queuedFiles,
      this.queuedFilesRemaining, this.folderPath.toString());
  }

  downloadFiles(): void {
    this.downloadHelper.downloadFiles(this.files, this.folderPath.toString());
  }

  renameFile(event: any): void {
    const renameFileDialog = this.dialog.open(RenameFileDialogComponent, {
      width: '350px',
      data: { filename: '' }
    });

    renameFileDialog.afterClosed().subscribe(filename => {
      if (filename) {
        this.renameHelper.renameFile(event.data, filename, this.files, this.folderPath.toString());
      }
    });
  }

  moveFiles(): void {
    const moveFileDialog = this.dialog.open(MoveFileDialogComponent, {
      width: '350px',
      maxWidth: '350px',
      data: {
        files: this.files,
        path: this.folderPath.toString()
      }
    });

    moveFileDialog.afterClosed().subscribe(destinationFolder => {
      if (destinationFolder) {
        let destinationPath = `${destinationFolder.path}/${destinationFolder.name}`;
        this.moveHelper.moveFiles(this.files, this.folderPath.toString(), destinationPath);
      }
    });
  }

  deleteFiles(): void {
    const deleteFileDialog = this.dialog.open(DeleteFileDialogComponent, {
      width: '350px'
    });

    deleteFileDialog.afterClosed().subscribe(deleteFileConfirmed => {
      if (deleteFileConfirmed) {
        this.deleteHelper.deleteFiles(this.files, this.folderPath.toString());
      }
    });
  }

  private createNewFolder(newFolder: Folder): void {
    this.fileService.createNewFolder(newFolder).subscribe(
      createdFolder => {
        this.snackBar.open(`${createdFolder.name} has been created.`);

        let folderMetadata = new FileMetadata(createdFolder.name, 0, null, null, true, false);
        this.files.push(folderMetadata);
      },
      error => {
        console.log(error);
      }
    );
  }

  private initFileDrop(): void {
    let dropArea = document.getElementsByClassName('file-card-container')[0];

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, showActiveFileDrop, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, hideActiveFileDrop, false);
    });

    function preventDefaults(event: any): void {
      event.preventDefault();
      event.stopPropagation();
    }

    function showActiveFileDrop(): void {
      dropArea.classList.add('file-drop-active');
    }

    function hideActiveFileDrop(): void {
      dropArea.classList.remove('file-drop-active');
    }
  }

}
