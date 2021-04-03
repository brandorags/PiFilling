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


export class FileMetadata {
  filename: string;
  fileSize: number;
  fileType: string;
  modifiedDate: string;
  isDirectory: boolean;
  isSelected: boolean;

  constructor(filename: string, fileSize: number, fileType: string,
    modifiedDate: string, isDirectory: boolean, isSelected: boolean) {
      this.filename = filename;
      this.fileSize = fileSize;
      this.fileType = fileType;
      this.modifiedDate = modifiedDate;
      this.isDirectory = isDirectory;
      this.isSelected = isSelected;
    }

  isImageFile(): boolean {
    let imageFileExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff'];
    return imageFileExtensions.includes(this.fileType.toLowerCase());
  }
}
