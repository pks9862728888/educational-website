import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-teacher-college',
  templateUrl: './teacher-college.component.html',
  styleUrls: ['./teacher-college.component.css']
})
export class TeacherCollegeComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // For handling filters
  appliedFilter = 'NONE';

  // For handling expansion panel
  step: number;
  stepJoined: number;

  // For handling star rating
  rating = 4;

  constructor(private media: MediaMatcher) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

  // For controlling expansion panel functioning
  setStep(index: number) {
    this.step = index;
  }

  setStepJoined(index: number) {
    this.stepJoined = index;
  }

  // For checking filter
  checkFilter(filterName: string) {
    if (this.appliedFilter === filterName) {
      return true;
    } else {
      return false;
    }
  }

  applyFilter(filterName: string) {
    this.appliedFilter = filterName;
  }

}
