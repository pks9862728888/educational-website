import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-school-classes',
  templateUrl: './school-classes.component.html',
  styleUrls: ['./school-classes.component.css']
})
export class SchoolClassesComponent implements OnInit {

  mobileQuery: MediaQueryList;

  // For storing classes
  classStep: number;
  classList = [1, 2];

  constructor( private media: MediaMatcher) {
    this.mobileQuery = this.media.matchMedia('(max-width: 768px)');
  }

  ngOnInit(): void {}

  // For handling expansion panel
  setClassStep(step: number) {
    this.classStep = step;
  }

  isClassesListEmpty() {
    return false;
  }

}
