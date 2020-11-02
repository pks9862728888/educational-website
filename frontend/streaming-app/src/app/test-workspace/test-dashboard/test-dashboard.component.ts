import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-test-dashboard',
  templateUrl: './test-dashboard.component.html',
  styleUrls: ['./test-dashboard.component.css']
})
export class TestDashboardComponent implements OnInit {

  mq: MediaQueryList;
  selectedControl = 'TEST_DETAILS';

  constructor(
    private mediaMatcher: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = this.mediaMatcher.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
