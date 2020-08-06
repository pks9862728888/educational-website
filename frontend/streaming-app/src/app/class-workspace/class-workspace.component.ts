import { currentClassSlug, currentInstituteType, paymentComplete, purchasedLicenseExists, INSTITUTE_TYPE_REVERSE, hasClassPerm } from './../../constants';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Subscription } from 'rxjs';
import { MediaMatcher } from '@angular/cdk/layout';
import { currentInstituteSlug, currentInstituteRole, INSTITUTE_ROLE_REVERSE } from '../../constants';

@Component({
  selector: 'app-class-workspace',
  templateUrl: './class-workspace.component.html',
  styleUrls: ['./class-workspace.component.css']
})
export class ClassWorkspaceComponent implements OnInit, OnDestroy {
  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentInstituteRole: string;
  currentClassSlug: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  constructor( private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService) {
    this.mq = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'CLASS_PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('profile')) {
          this.activeLink = 'CLASS_PROFILE';
        } else if(val.url.includes('subjects')) {
          this.activeLink = 'CLASS_SUBJECTS';
        } else if(val.url.includes('permissions')) {
          this.activeLink = 'CLASS_PERMISSIONS';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentInstituteRole = sessionStorage.getItem(currentInstituteRole);
    this.currentClassSlug = sessionStorage.getItem(currentClassSlug);
    this.baseUrl = '/class-workspace/' + this.currentClassSlug.slice(0, -10);
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

  clearAllInstituteRelatedStorage() {
    sessionStorage.removeItem(currentInstituteSlug);
    sessionStorage.removeItem(currentInstituteRole);
    sessionStorage.removeItem(currentInstituteType);
    sessionStorage.removeItem(paymentComplete);
    sessionStorage.removeItem(purchasedLicenseExists);
    sessionStorage.removeItem(currentClassSlug);
    sessionStorage.removeItem(hasClassPerm);
  }

  navigateToAppropriateInstituteWorkspace(path: string) {
    if (sessionStorage.getItem(currentInstituteType) === INSTITUTE_TYPE_REVERSE['School']) {
      this.router.navigate(['/school-workspace/' + this.currentInstituteSlug + path]);
    } else if (sessionStorage.getItem(currentInstituteType) === INSTITUTE_TYPE_REVERSE['Coaching']) {
      this.router.navigate(['/coaching-workspace/' + this.currentInstituteSlug + path]);
    } else if (sessionStorage.getItem(currentInstituteType) === INSTITUTE_TYPE_REVERSE['College']) {
      this.router.navigate(['/college-workspace/' + this.currentInstituteSlug + path]);
    }
  }

  navigate(link: string) {
    if (this.mq.matches === true) {
      this.opened = false;
    }
    if (link !== this.activeLink) {
      if (link === 'HOME') {
        this.clearAllInstituteRelatedStorage();
        this.router.navigate(['/home']);
      } else if (link === 'EXIT_INSTITUTE') {
        this.clearAllInstituteRelatedStorage();
        this.router.navigate(['/teacher-workspace/institutes']);
      } else if (link === 'EXIT_CLASS' || link === 'INSTITUTE') {
        sessionStorage.removeItem(currentClassSlug);
        sessionStorage.removeItem(hasClassPerm);
        this.navigateToAppropriateInstituteWorkspace('/classes');
      } else {
        if (link === 'CLASS_PROFILE') {
          this.router.navigate([this.baseUrl + '/profile']);
        } else if (link === 'CLASS_PERMISSIONS') {
          this.router.navigate([this.baseUrl + '/permissions']);
        } else if (link === 'CLASS_SUBJECTS') {
          this.router.navigate([this.baseUrl + '/subjects']);
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
