import { Component, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-teacher-profile',
  templateUrl: './teacher-profile.component.html',
  styleUrls: ['./teacher-profile.component.css']
})
export class TeacherProfileComponent implements OnInit {

  // For detecting whether device is mobile
  mobileQuery: MediaQueryList;

  constructor( private media: MediaMatcher ) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
  }

}
