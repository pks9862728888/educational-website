import { MediaMatcher } from '@angular/cdk/layout';
import { Component, Input, OnInit } from '@angular/core';
import { SubjectTestFullDetailsResponse } from 'src/app/models/subject.model';

@Component({
  selector: 'app-test-dashboard-details',
  templateUrl: './test-dashboard-details.component.html',
  styleUrls: ['./test-dashboard-details.component.css']
})
export class TestDashboardDetailsComponent implements OnInit {

  mq: MediaQueryList;
  @Input() testFullDetails: SubjectTestFullDetailsResponse;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
