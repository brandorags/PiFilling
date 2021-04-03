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
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { SimpleTimer } from 'ng2-simple-timer';

import { SessionTimerService } from '../../app/common/session-timer.service';

describe('SessionTimerService', () => {
  let timer: SimpleTimer;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule.withRoutes([])
      ],
      providers: [
        SimpleTimer,
        SessionTimerService
      ]
    });

    timer = TestBed.get(SimpleTimer);
  });

  it('should be created', inject([SessionTimerService], (service: SessionTimerService) => {
    expect(service).toBeTruthy();
  }));

  it('should start the timer', inject([SessionTimerService], (service: SessionTimerService) => {
    let timerIds = timer.getTimer();
    let subscriptionIds = timer.getSubscription();

    expect(timerIds.length).toEqual(0);
    expect(subscriptionIds.length).toEqual(0);

    service.startTimer();

    timerIds = timer.getTimer();
    subscriptionIds = timer.getSubscription();

    expect(timerIds.length).toEqual(1);
    expect(subscriptionIds.length).toEqual(1);

    let timerId = timerIds[0];
    let subscriptionId = subscriptionIds[0];

    expect(timerId).toEqual(service.sessionTimerId);
    expect(subscriptionId).toContain(service.sessionTimerId);
  }));

  it('should stop the timer', inject([SessionTimerService], (service: SessionTimerService) => {
    service.startTimer();

    let timerIds = timer.getTimer();
    let subscriptionIds = timer.getSubscription();

    expect(timerIds.length).toEqual(1);
    expect(subscriptionIds.length).toEqual(1);

    service.stopTimer();

    timerIds = timer.getTimer();
    subscriptionIds = timer.getSubscription();

    expect(timerIds.length).toEqual(0);
    expect(subscriptionIds.length).toEqual(0);
  }));

  it('should have a running timer', inject([SessionTimerService], (service: SessionTimerService) => {
    service.startTimer();

    expect(service.isTimerRunning()).toBeTruthy();
  }));

  it('should have a stopped timer', inject([SessionTimerService], (service: SessionTimerService) => {
    service.startTimer();
    service.stopTimer();

    expect(service.isTimerRunning()).toBeFalsy();
  }));

  it('should have a running timer after being refreshed', inject([SessionTimerService],
    (service: SessionTimerService) => {
    service.startTimer();
    service.refreshTimer();

    expect(service.isTimerRunning()).toBeTruthy();
  }));

  it('should not have a running timer after being refreshed', inject([SessionTimerService],
    (service: SessionTimerService) => {
    service.refreshTimer();

    expect(service.isTimerRunning()).toBeFalsy();
  }));
});
