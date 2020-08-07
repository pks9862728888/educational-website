import { currentSubjectSlug, currentInstituteSlug, currentInstituteRole, currentInstituteType, paymentComplete, purchasedLicenseExists, currentClassSlug, hasClassPerm, hasSubjectPerm, INSTITUTE_TYPE_REVERSE } from './../../constants';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-subject-workspace',
  templateUrl: './subject-workspace.component.html',
  styleUrls: ['./subject-workspace.component.css']
})
export class SubjectWorkspaceComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentInstituteType: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  constructor(
    private router: Router,
    private media: MediaMatcher,
    private inAppDataTransferService: InAppDataTransferService) {

    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'SUBJECT_OVERVIEW';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('overview')) {
          this.activeLink = 'SUBJECT_OVERVIEW';
        } else if (val.url.includes('permissions')) {
          this.activeLink = 'SUBJECT_PERMISSIONS';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    this.baseUrl = '/subject-workspace/' + this.currentSubjectSlug.slice(0, -10);
    this.currentInstituteType = sessionStorage.getItem(currentInstituteType);
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
  }

  navigateToAppropriateInstituteWorkspace(path: string) {
    if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['Coaching']) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + path]);
    } else if (this.currentInstituteType === INSTITUTE_TYPE_REVERSE['College']) {
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
      } else if (link === 'CLASS_SUBJECTS') {
        this.router.navigate(['/class-workspace/' + sessionStorage.getItem(currentClassSlug).slice(0, -10) + '/subjects']);
      } else if (link === 'CURRENT_INSTITUTE') {
        this.navigateToAppropriateInstituteWorkspace('/profile');
      } else if (link === 'INSTITUTES') {
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        if (link === 'SUBJECT_OVERVIEW') {
          this.router.navigate([this.baseUrl + '/overview']);
        } else if (link === 'SUBJECT_PERMISSIONS') {
          this.router.navigate([this.baseUrl + '/permissions']);
        }
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
