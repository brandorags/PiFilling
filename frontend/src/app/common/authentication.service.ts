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


import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';

import { User } from '../models/login/user';
import { Constants } from '../common/constants';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private isUserLoggedInSource = new BehaviorSubject<boolean>(false);
  public isUserLoggedInObservable = this.isUserLoggedInSource.asObservable();

  constructor(private http: HttpClient) { }

  login(user: User): Observable<User> {
    return this.http.post<User>(Constants.apiBaseUrl + 'api/login', user, Constants.httpOptionsAuth)
      .pipe(map(
        loggedInUser => {
          this.createUserDataCache(loggedInUser);
          this.setLoggedInStatus(true);

          return loggedInUser;
        },
        error => {
          return error;
        }
      ));
  }

  logout(): Observable<any> {
    return this.http.post<any>(Constants.apiBaseUrl + 'api/logout', JSON.stringify(''), Constants.httpOptionsAuth)
      .pipe(map(
        response => {
          this.deleteUserDataCache();
          this.setLoggedInStatus(false);
          localStorage.clear();

          return response;
        },
        error => {
          return error;
        }
      ));
  }

  setLoggedInStatus(isUserLoggedIn: boolean): void {
    this.isUserLoggedInSource.next(isUserLoggedIn);
  }

  private createUserDataCache(user: User): void {
    document.cookie = Constants.userCookieKey + '=loggedIn';
    localStorage.setItem(Constants.usernameLocalStorageKey, user.username);
  }

  private deleteUserDataCache(): void {
    document.cookie = Constants.userCookieKey + '=; Max-Age=0';
    localStorage.removeItem(Constants.usernameLocalStorageKey);
  }

}
