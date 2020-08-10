import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-course-guidelines',
  templateUrl: './course-guidelines.component.html',
  styleUrls: ['./course-guidelines.component.css']
})
export class CourseGuidelinesComponent implements OnInit {

  mq: MediaQueryList;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }
}
