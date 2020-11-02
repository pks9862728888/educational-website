import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SubjectTestFullDetailsResponse } from 'src/app/models/subject.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { QUESTIONS_CATEGORY, QUESTION_MODE } from 'src/constants';

@Component({
  selector: 'app-test-dashboard',
  templateUrl: './test-dashboard.component.html',
  styleUrls: ['./test-dashboard.component.css']
})
export class TestDashboardComponent implements OnInit {

  mq: MediaQueryList;
  selectedControl = 'TEST_DETAILS';

  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentTestSlug: string;
  currentInstituteRole: string;

  loadingError: string;
  reloadIndicator: boolean;
  loadingIndicator: boolean;

  testFullDetails: SubjectTestFullDetailsResponse;

  constructor(
    private mediaMatcher: MediaMatcher,
    private instituteApiService: InstituteApiService,
    private uiService: UiService,
    private router: Router
  ) {
    this.mq = this.mediaMatcher.matchMedia('(max-width: 600px)');
    const splittedPathName = window.location.pathname.split('/');
    this.currentInstituteSlug = splittedPathName[2];
    this.currentInstituteRole = splittedPathName[3].toUpperCase();
    this.currentSubjectSlug = splittedPathName[4];
    this.currentTestSlug = splittedPathName[5];
  }

  ngOnInit(): void {
    this.getTestFullDetails();
  }

  getTestFullDetails() {
    this.loadingIndicator = true;
    this.reloadIndicator = false;
    this.loadingError = null;
    this.instituteApiService.getSubjectTestFullDetails(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug
    ).subscribe(
      (result: SubjectTestFullDetailsResponse) => {
        this.loadingIndicator = false;
        this.testFullDetails = result;
      },
      errors => {
        this.loadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingError = errors.error.error;
          } else {
            this.reloadIndicator = true;
          }
        } else {
          this.reloadIndicator = true;
        }
      }
    );
  }

  navigateToCreateQuestionPaperView() {
    const hostName = window.location.pathname;
    let path = hostName.slice(0, hostName.length - 'dashboard'.length) + 'create-question-paper/';
    if (this.testFullDetails.question_category === QUESTIONS_CATEGORY.AUTOCHECK_TYPE &&
      this.testFullDetails.question_mode === QUESTION_MODE.TYPED) {
      path += 'autocheck-question-typed-mode';
    } else if (this.testFullDetails.question_category === QUESTIONS_CATEGORY.ALL_TYPES &&
      this.testFullDetails.question_mode === QUESTION_MODE.TYPED) {
      path += 'all-question-typed-mode';
    } else if (this.testFullDetails.question_mode === QUESTION_MODE.FILE) {
      path += 'file-mode';
    } else if (this.testFullDetails.question_mode === QUESTION_MODE.IMAGE) {
      path += 'image-mode';
    }
    this.router.navigate([path]);
  }

}
