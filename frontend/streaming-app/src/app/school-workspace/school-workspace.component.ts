import { currentInstituteSlug, currentInstituteRole, INSTITUTE_ROLE_REVERSE, webAppName, is_student, is_teacher } from './../../constants';
import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { InstituteLicenseExists } from '../models/license.model';


@Component({
  selector: 'app-school-workspace',
  templateUrl: './school-workspace.component.html',
  styleUrls: ['./school-workspace.component.css']
})
export class SchoolWorkspaceComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  title = webAppName;
  userType: string;
  currentInstituteSlug: string;
  currentInstituteRole: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;
  licenseExistsStatistics: InstituteLicenseExists = {
    purchased_common_license: false
  };
  purchasedLicenseSubscription: Subscription;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;

  constructor(
    private router: Router,
    private media: MediaMatcher,
    private inAppDataTransferService: InAppDataTransferService,
    private instituteApiService: InstituteApiService
    ) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('profile')) {
          this.activeLink = 'PROFILE';
        } else if (val.url.includes('permissions')) {
          this.activeLink = 'PERMISSIONS';
        } else if (val.url.includes('classes')) {
          this.activeLink = 'CLASSES';
        } else if (val.url.includes('license')) {
          this.activeLink = 'LICENSE';
        } else if (val.url.includes('students')) {
          this.activeLink = 'STUDENTS';
        } else if (val.url.includes('student-courses')) {
          this.activeLink = 'STUDENT-COURSES';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteRole = sessionStorage.getItem(currentInstituteRole);
    if (sessionStorage.getItem(is_student) === 'true') {
      this.userType = 'STUDENT';
    } else if (sessionStorage.getItem(is_teacher) === 'true') {
      this.userType = 'TEACHER';
    }
    this.baseUrl = '/school-workspace/' + this.currentInstituteSlug;
    this.purchasedLicenseSubscription = this.inAppDataTransferService.teacherLmsCmsView$.subscribe(
      () => {
        this.licenseExistsStatistics.purchased_common_license = true;
      }
    );
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mq.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }
    this.showTempNamesSubscription = this.inAppDataTransferService.activeBreadcrumbLinkData$.subscribe(
      (linkName: string) => {
        this.tempBreadcrumbLinkName = linkName;
      }
    );
    this.loadLicenseStatistics();
  }

  loadLicenseStatistics() {
    this.loadingIndicator = true;
    this.loadingError = null;
    this.reloadIndicator = false;
    this.instituteApiService.getLicenseExistsStatistics(
      sessionStorage.getItem(currentInstituteSlug)
      ).subscribe(
      (result: InstituteLicenseExists) => {
        this.loadingIndicator = false;
        this.licenseExistsStatistics = result;
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

  // For navigating to teacher-workspace view
  navigate(link: string) {
    if (link !== this.activeLink) {
      if (link === 'HOME') {
        this.router.navigate(['/home']);
      } else if (link === 'EXIT' || link === 'INSTITUTES') {
        if (this.userType === 'TEACHER') {
          sessionStorage.removeItem('paymentComplete');
          this.router.navigate(['/teacher-workspace/institutes']);
        } else if (this.userType === 'STUDENT') {
          this.router.navigate(['/student-workspace/institutes']);
        }
      } else {
        this.router.navigate([this.baseUrl + '/' + link.toLowerCase()]);
      }
    }
  }

  // For navbar
  performAction(link: string) {
    if (this.mq.matches === true) {
      this.opened = false;
    }
    this.navigate(link);
  }

  tempBreadCrumbNameExists() {
    if (this.tempBreadcrumbLinkName) {
      return true;
    } else {
      return false;
    }
  }

  userIsAdmin() {
    if (this.currentInstituteRole == INSTITUTE_ROLE_REVERSE['Admin']) {
      return true;
    } else {
      return false;
    }
  }

  userIsStudent() {
    if (this.userType === 'STUDENT') {
      return true;
    } else {
      return false;
    }
  }

  userIsTeacher() {
    if (this.userType === 'TEACHER') {
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
    if (this.purchasedLicenseSubscription) {
      this.purchasedLicenseSubscription.unsubscribe();
    }
  }

}
