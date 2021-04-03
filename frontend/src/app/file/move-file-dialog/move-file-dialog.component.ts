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


import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { FileService } from '../file.service';

import { Folder } from '../../models/file/folder';
import { FileMetadata } from 'src/app/models/file/file-metadata';

@Component({
  selector: 'app-move-file-dialog',
  templateUrl: './move-file-dialog.component.html',
  styleUrls: ['./move-file-dialog.component.scss']
})
export class MoveFileDialogComponent implements OnInit {

  folderList: Folder[] = [];
  currentFolder: Folder = new Folder();
  selectedFolder: Folder = new Folder();

  selectedFilesToMove: FileMetadata[] = [];

  isLoading = false;

  constructor(
    public dialogRef: MatDialogRef<MoveFileDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any,
    private fileService: FileService
  ) { }

  ngOnInit(): void {
    this.isLoading = true;

    for (let file of this.dialogData.files) {
      if (file.isSelected) {
        this.selectedFilesToMove.push(file);
      }
    }

    this.getFoldersForPath(this.dialogData.path);
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

  navigateOneFolderUp(): void {
    let splitPath = this.currentFolder.path.split('/');
    let pathWithLastFolderRemoved = splitPath.splice(0, splitPath.length - 1).join('/');

    this.getFoldersForPath(pathWithLastFolderRemoved);
  }

  navigateOneFolderDown(): void {
    if (this.selectedFolder.name === undefined) {
      return;
    }

    this.getFoldersForPath(`${this.selectedFolder.path}/${this.selectedFolder.name}`);
  }

  private getFoldersForPath(path: string): void {
    this.fileService.getFoldersForPath(path).subscribe(
      folderList => {
        this.folderList = [];

        // only show unselected folders
        for (let folder of folderList) {
          let folderIndex = this.selectedFilesToMove.findIndex(f => f.filename === folder.name);
          if (folderIndex === -1) {
            this.folderList.push(folder);
          }
        }

        let splitPath = path.split('/');
        this.currentFolder.name = splitPath[splitPath.length - 1];
        this.currentFolder.path = path;
      },
      error => {
        console.log(error);
      }
    ).add(() => this.isLoading = false);
  }

}
