import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-test-dashboard-details',
  templateUrl: './test-dashboard-details.component.html',
  styleUrls: ['./test-dashboard-details.component.css']
})
export class TestDashboardDetailsComponent implements OnInit {

  mq: MediaQueryList;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
