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
import { Router } from '@angular/router';

import { SimpleTimer } from 'ng2-simple-timer';

import { AuthenticationService } from './authentication.service';
import { Constants } from './constants';

@Injectable({
  providedIn: 'root'
})
export class SessionTimerService {

  readonly sessionTimerId = 'sessionTimer';

  constructor(
    private timer: SimpleTimer,
    private router: Router,
    private authService: AuthenticationService
  ) { }

  startTimer(): void {
    let interval = 5;
    let counter = 0;

    this.timer.newTimer(this.sessionTimerId, interval);
    this.timer.subscribe(this.sessionTimerId, () => {
      counter += interval;

      if (counter >= Constants.lengthOfSession) {
        this.stopTimer();
        this.authService.logout().subscribe(
          () => {
            console.log('You have been logged out due to inactivity.');
            this.router.navigate(['/login']);
          },
          error => {
            console.log(error.message);
          }
        );
      }
    });
  }

  stopTimer(): void {
    let subscriptions = this.timer.getSubscription();
    this.timer.unsubscribe(subscriptions[0]);
    this.timer.delTimer(this.sessionTimerId);
  }

  refreshTimer(): void {
    if (this.isTimerRunning()) {
      this.stopTimer();
      this.startTimer();
    }
  }

  isTimerRunning(): boolean {
    let runningTimers = this.timer.getTimer();
    return runningTimers.length > 0 ? true : false;
  }

}
