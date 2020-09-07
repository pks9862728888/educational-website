import { InstituteApiService } from './../../services/institute-api.service';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { StudentAllCoursesList, StudentCourseListViewOrder, StudentCourseDetails } from '../../models/student.model';

@Component({
  selector: 'app-student-courses',
  templateUrl: './student-courses.component.html',
  styleUrls: ['./student-courses.component.css']
})
export class StudentCoursesComponent implements OnInit {

  mq: MediaQueryList;
  openedPanelStep: number;
  showLoadingIndicator: boolean;
  showReload: boolean;
  text = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis iure explicabo maiores nesciunt facilis consectetur rem distinctio unde laborum nostrum eligendi dolore animi fuga hic, eveniet, consequatur deleniti, porro voluptatem.';

  viewOrder: StudentCourseListViewOrder[] = [];
  courses: [{string: StudentCourseDetails}];
  favouriteCourses: [{string: StudentCourseDetails}];
  classNames = {};

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.getCourses()
  }

  getCourses() {
    this.showLoadingIndicator = true;
    this.showReload = false;
    this.instituteApiService.getAllStudentCourses().subscribe(
      (result: StudentAllCoursesList) => {
        this.showLoadingIndicator = false;
        this.viewOrder = result.view_order;
        this.courses = result.courses;
        this.favouriteCourses = result.favourite_courses;
        this.classNames = result.class_names;
        if (this.favouriteCourses.length > 0) {
          this.openedPanelStep = 0;
        }
        console.log(result);
        console.log(this.viewOrder);
        console.log(this.courses);
        console.log(this.favouriteCourses);
        console.log(this.classNames);
      },
      errors => {
        this.showLoadingIndicator = false;
        this.showReload = true;
      }
    );
  }

  bookmark(course: StudentCourseDetails) {

  }

  setOpenedPanelStep(step: number) {
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
    }
  }

  formatDescription(text: string) {
    if (this.text.length > 106) {
      return this.text.slice(0, 106) + '...';
    } else {
      return this.text;
    }
  }

  isMyCourseEmpty() {
    if (this.viewOrder.length === 0) {
      return true;
    } else {
      return false;
    }
  }

  isInstituteCourseListEmpty(institueSlug: string) {
    if (this.courses[institueSlug].length === 0) {
      return true;
    } else {
      return false;
    }
  }
}
