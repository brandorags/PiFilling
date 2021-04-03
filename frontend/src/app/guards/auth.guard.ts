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
import { CanActivate, Router } from '@angular/router';

import { SessionTimerService } from '../common/session-timer.service';
import { Constants } from '../common/constants';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private router: Router,
    private sessionTimerService: SessionTimerService
  ) { }

  canActivate() {
    if (this.isUserLoggedIn()) {
      this.sessionTimerService.refreshTimer();
      return true;
    } else {
      this.router.navigate(['/login']);
    }

    return false;
  }

  private isUserLoggedIn(): boolean {
    let currentUserCookie = Constants.userCookieKey;
    if (document.cookie.includes(currentUserCookie)) {
      return true;
    }

    return false;
  }

}
