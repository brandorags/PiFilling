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


import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient, HttpRequest, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Constants } from '../common/constants';
import { FileMetadata } from '../models/file/file-metadata';
import { FileRename } from '../models/file/file-rename';
import { FileDownload } from '../models/file/file-download';
import { FileDelete } from '../models/file/file-delete';
import { FileMove } from '../models/file/file-move';
import { Folder } from '../models/file/folder';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  fileListEventEmitter: EventEmitter<FileList> = new EventEmitter();
  newFolderEventEmitter: EventEmitter<string> = new EventEmitter();

  constructor(private http: HttpClient) { }

  getFilesForPath(path: string): Observable<FileMetadata[]> {
    const params = new HttpParams()
      .set('path', path);

    return this.http.get<FileMetadata[]>(Constants.apiBaseUrl + 'api/file/file-metadata', { params: params, withCredentials: true })
      .pipe(map(res => res.map(fm => new FileMetadata(fm.filename, fm.fileSize,
        fm.fileType, fm.modifiedDate, fm.isDirectory, false))));
  }

  getFoldersForPath(path: string): Observable<Folder[]> {
    const params = new HttpParams()
      .set('path', path);

      return this.http.get<Folder[]>(Constants.apiBaseUrl + 'api/file/directory-list', { params: params, withCredentials: true });
  }

  uploadFile(formData: FormData, folderPath: string): Observable<any> {
    const headers = new HttpHeaders({'Current-Directory': folderPath});
    const uploadRequest = new HttpRequest('POST', Constants.apiBaseUrl + 'api/file/upload-file', formData, {
      headers: headers,
      withCredentials: true,
      reportProgress: true
    });

    return this.http.request<any>(uploadRequest);
  }

  renameFile(fileToRename: FileRename): Observable<string> {
    return this.http.post<string>(Constants.apiBaseUrl + 'api/file/rename-file', fileToRename, Constants.httpOptionsAuth);
  }

  downloadFiles(fileDownload: FileDownload): Observable<any> {
    const downloadRequest = new HttpRequest('POST', Constants.apiBaseUrl + 'api/file/download-files', fileDownload, {
      withCredentials: true,
      responseType: 'blob'
    });

    return this.http.request<any>(downloadRequest);
  }

  deleteFiles(filesToDelete: FileDelete[]): Observable<any> {
    const deleteRequest = new HttpRequest('DELETE', Constants.apiBaseUrl + 'api/file/delete-files', filesToDelete, {
      withCredentials: true
    });

    return this.http.request<any>(deleteRequest);
  }

  moveFiles(filesToMove: FileMove[]): Observable<any> {
    return this.http.post<any>(Constants.apiBaseUrl + 'api/file/move-files', filesToMove, Constants.httpOptionsAuth);
  }

  createNewFolder(newFolder: Folder): Observable<Folder> {
    return this.http.post<Folder>(Constants.apiBaseUrl + 'api/file/new-directory', newFolder, Constants.httpOptionsAuth);
  }

}
