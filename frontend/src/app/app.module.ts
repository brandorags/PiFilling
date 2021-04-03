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


// Angular
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';

// third-party modules
import { SimpleTimer } from 'ng2-simple-timer';
import { ShContextMenuModule } from 'context-menu-angular6';

// user-defined modules
import { MaterialModule } from './material/material.module';
import { AppRoutingModule } from './app-routing.module';

// user-defined HTTP interceptor
import { AppHttpInterceptor } from './app-http-interceptor';

// user-defined guards
import { AuthGuard } from './guards/auth.guard';

// user-defined components
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { FileComponent } from './file/file.component';
import { NewFolderDialogComponent } from './file/new-folder-dialog/new-folder-dialog.component';
import { RenameFileDialogComponent } from './file/rename-file-dialog/rename-file-dialog.component';
import { DeleteFileDialogComponent } from './file/delete-file-dialog/delete-file-dialog.component';
import { MoveFileDialogComponent } from './file/move-file-dialog/move-file-dialog.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    NotFoundComponent,
    FileComponent,
    NewFolderDialogComponent,
    RenameFileDialogComponent,
    DeleteFileDialogComponent,
    MoveFileDialogComponent
  ],
  entryComponents: [
    NewFolderDialogComponent,
    RenameFileDialogComponent,
    DeleteFileDialogComponent,
    MoveFileDialogComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    LayoutModule,
    MaterialModule,
    AppRoutingModule,
    ShContextMenuModule
  ],
  providers: [
    AuthGuard,
    SimpleTimer,
    { provide: HTTP_INTERCEPTORS, useClass: AppHttpInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
