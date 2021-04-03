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


import { TestBed, inject } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AuthenticationService } from '../../app/common/authentication.service';

import { User } from '../../app/models/login/user';
import { Constants } from '../../app/common/constants';

describe('AuthenticationService', () => {
  let mockHttp: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthenticationService]
    });

    mockHttp = TestBed.get(HttpTestingController);
  });

  afterEach(() => {
    mockHttp.verify();
  });

  it('should be created', inject([AuthenticationService], (service: AuthenticationService) => {
    expect(service).toBeTruthy();
  }));

  it('should log the user in', inject([AuthenticationService], (service: AuthenticationService) => {
    let user = new User();
    user.username = 'test';
    user.password = 'password';

    service.login(user).subscribe(response => {
      expect(response).toEqual(user);
    });

    let mockRequest = mockHttp.expectOne(Constants.apiBaseUrl + 'api/login');

    expect(mockRequest.request.method).toEqual('POST');
    expect(mockRequest.request.withCredentials).toBeTruthy();
    expect(mockRequest.request.responseType).toEqual('json');

    mockRequest.flush(user);
  }));

  it('should log the user out', inject([AuthenticationService], (service: AuthenticationService) => {
    service.logout().subscribe();

    let mockRequest = mockHttp.expectOne(Constants.apiBaseUrl + 'api/logout');

    expect(mockRequest.request.method).toEqual('POST');
    expect(mockRequest.request.withCredentials).toBeTruthy();
    expect(mockRequest.request.responseType).toEqual('json');
  }));

  it('should have a logged in status set to true', inject([AuthenticationService], (service: AuthenticationService) => {
    let loggedInStatus: boolean;

    service.isUserLoggedInObservable.subscribe(isLoggedIn => loggedInStatus = isLoggedIn);
    service.setLoggedInStatus(true);

    expect(loggedInStatus).toBeTruthy();
  }));
});
