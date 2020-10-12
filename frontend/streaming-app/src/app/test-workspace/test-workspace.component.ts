import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd } from '@angular/router';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { currentInstituteSlug,
         currentInstituteType,
         INSTITUTE_TYPE_REVERSE,
         QUESTION_MODE,
         testMinDetails,
         webAppName } from 'src/constants';
import { TestMinDetailsResponse } from '../models/test.model';
import { InstituteApiService } from '../services/institute-api.service';

@Component({
  selector: 'app-test-workspace',
  templateUrl: './test-workspace.component.html',
  styleUrls: ['./test-workspace.component.css']
})
export class TestWorkspaceComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  webAppName = webAppName;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentTestSlug: string;
  currentInstituteType: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;

  QUESTION_MODE = QUESTION_MODE;
  testMinDetails: TestMinDetailsResponse;

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private media: MediaMatcher,
    private instituteApiService: InstituteApiService,
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'DASHBOARD';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('dashboard')) {
          this.activeLink = 'DASHBOARD';
        } else if (val.url.includes('create-question-paper/file-mode')) {
          this.activeLink = 'CREATE-QUESTION-PAPER/FILE-MODE';
        } else if (val.url.includes('create-question-paper/image-mode')) {
          this.activeLink = 'CREATE-QUESTION-PAPER/IMAGE-MODE';
        } else if (val.url.includes('create-question-paper/typed-mode')) {
          this.activeLink = 'CREATE-QUESTION-PAPER/TYPED-MODE';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = activatedRoute.snapshot.params.subjectSlug;
    this.currentTestSlug = activatedRoute.snapshot.params.testSlug;
    this.baseUrl = '/test-workspace/' + this.currentSubjectSlug + '/' + this.currentTestSlug;
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mq.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }
    this.loadTestMinDetails();
  }

  loadTestMinDetails() {
    this.loadingIndicator = true;
    this.loadingError = null;
    this.reloadIndicator = false;
    this.instituteApiService.getMinTestDetails(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug
    ).subscribe(
      (result: TestMinDetailsResponse) => {
        this.loadingIndicator = false;
        this.testMinDetails = result;
        sessionStorage.setItem(testMinDetails, JSON.stringify(this.testMinDetails));
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

  navigateToAppropriateInstituteWorkspace(path: string) {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.School) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.Coaching) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE.College) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + path]);
    }
  }

  navigate(link: string) {
    if (this.mq.matches === true) {
      this.opened = false;
    }
    if (link !== this.activeLink) {
      if (link === 'HOME') {
        this.router.navigate(['/home']);
      } else if (link === 'CURRENT_SUBJECT') {
        this.router.navigate(['/subject-workspace/' + this.currentSubjectSlug + '/create-course']);
      } else if (link === 'CURRENT_INSTITUTE') {
        this.navigateToAppropriateInstituteWorkspace('/profile');
      } else if (link === 'INSTITUTES') {
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        this.router.navigate([this.baseUrl + '/' + link.toLowerCase()]);
      }
    }
  }

  tempBreadCrumbNameExists() {
    if (this.tempBreadcrumbLinkName) {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
  }
}
