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


import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import { AuthenticationService } from '../common/authentication.service';
import { SessionTimerService } from '../common/session-timer.service';

import { User } from '../models/login/user';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  user = new User();

  @ViewChild('usernameTextbox', { static: true })
  usernameTextbox: any;
  @ViewChild('loginButton', { static: true })
  loginButton: any;

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private authService: AuthenticationService,
    private sessionTimerService: SessionTimerService
  ) { }

  ngOnInit() {
    this.usernameTextbox.nativeElement.focus();
  }

  loginUser(): void {
    this.loginButton.disabled = true;

    this.authService.login(this.user)
      .subscribe(
        user => {
          this.sessionTimerService.startTimer();
          this.router.navigate(['/files']);
          this.snackBar.open(`Welcome, ${user.username}!`);
        },
        error => {
          console.log(error.message);
          this.loginButton.disabled = false;
        }
      );
  }

}
