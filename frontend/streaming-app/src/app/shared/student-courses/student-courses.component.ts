import { currentInstituteSlug, currentSubjectSlug, currentClassSlug } from './../../../constants';
import { Router } from '@angular/router';
import { UiService } from './../../services/ui.service';
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

  viewOrder: StudentCourseListViewOrder[] = [];
  courses: [{string: StudentCourseDetails}];
  favouriteCourses: [{string: StudentCourseDetails}];
  classNames = {};

  constructor(
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private uiService: UiService,
    private router: Router
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.openedPanelStep = 0;
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

  getIndex(array, subject_id: number) {
    for (let i in array) {
      if (array[i].subject_id === subject_id) {
        return i;
      }
    }
    return -1;
  }

  bookmark(course: StudentCourseDetails) {
    this.instituteApiService.bookmarkInstituteCourse(
      course.subject_id.toString()
    ).subscribe(
      () => {
        if (course.BOOKMARKED) {
          course.BOOKMARKED = !course.BOOKMARKED;
          const index = this.getIndex(this.favouriteCourses, course.subject_id)
          this.favouriteCourses['BOOKMARKED'].splice(
            index, 1);

          if (this.courses[course.institute_slug]) {
            this.courses[course.institute_slug].push(course);
          } else {
            this.courses[course.institute_slug] = [
              course
            ];
          }
          this.uiService.showSnackBar(
            'Course removed from favourites!', 2000
          );
        } else {
          course.BOOKMARKED = !course.BOOKMARKED;
          const index = this.getIndex(this.courses, course.subject_id)
          this.courses[course.institute_slug].splice(index, 1);

          if (this.favouriteCourses[course.institute_slug]) {
            this.favouriteCourses['BOOKMARKED'].push(course);
          } else {
            this.favouriteCourses['BOOKMARKED'] = [
              course
            ];
          }
          this.uiService.showSnackBar(
            'Course added to favourites!', 2000
          );
        }
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              2500
            );
          } else {
            this.uiService.showSnackBar(
              'Error occured :(',
              2000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error occured :(',
            2000
          );
        }
      }
    );
  }

  openCourse(course: StudentCourseDetails) {
    sessionStorage.setItem(currentInstituteSlug, course.institute_slug);
    sessionStorage.setItem(currentSubjectSlug, course.subject_slug);
    sessionStorage.setItem(currentClassSlug, course.class_slug);
    const name = course.subject_slug.slice(0, -9);
    this.router.navigate(['preview-course-workspace/' + name + '/preview']);
  }

  setOpenedPanelStep(step: number) {
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
    }
  }

  formatDescription(text: string) {
    if (text && text.length > 106) {
      return text.slice(0, 106) + '...';
    } else {
      return text;
    }
  }

  getCourseList(institute: StudentCourseListViewOrder) {
    if (institute.institute_slug === 'BOOKMARKED') {
      return this.favouriteCourses[institute.institute_slug];
    } else {
      return this.courses[institute.institute_slug];
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
    if (institueSlug === 'BOOKMARKED') {
      if (this.favouriteCourses[institueSlug].length === 0) {
        return true;
      } else {
        return false;
      }
    } else {
      if (this.courses[institueSlug].length === 0) {
        return true;
      } else {
        return false;
      }
    }
  }
}
