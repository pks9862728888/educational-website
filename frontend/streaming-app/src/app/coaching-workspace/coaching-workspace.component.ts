import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { InstituteLicenseExists } from '../models/license.model';
import { currentInstituteSlug, webAppName } from 'src/constants';

@Component({
  selector: 'app-coaching-workspace',
  templateUrl: './coaching-workspace.component.html',
  styleUrls: ['./coaching-workspace.component.css']
})
export class CoachingWorkspaceComponent implements OnInit, OnDestroy {

  mq: MediaQueryList;
  webAppName = webAppName;
  currentInstituteSlug: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;
  licenseExistsStatistics: InstituteLicenseExists;
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
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.activeLink = 'COACHING_PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if (val.url.includes('profile')) {
          this.activeLink = 'COACHING_PROFILE';
        } else if (val.url.includes('permissions')) {
          this.activeLink = 'COACHING_PERMISSIONS';
        } else if (val.url.includes('license')) {
          this.activeLink = 'LICENSE';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.baseUrl = '/coaching-workspace/' + this.currentInstituteSlug;
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
      } else if (link === 'EXIT') {
        sessionStorage.setItem('activeRoute', 'INSTITUTES');
        sessionStorage.removeItem('currentInstituteSlug');
        sessionStorage.removeItem('currentInstituteRole');
        sessionStorage.removeItem('currentInstituteType');
        sessionStorage.removeItem('selectedLicenseId');
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        if (link === 'COACHING_PROFILE') {
          this.router.navigate([this.baseUrl + '/profile']);
        } else if (link === 'COACHING_PERMISSIONS') {
          this.router.navigate([this.baseUrl + '/permissions']);
        } else if (link === 'COACHING_CLASSES') {
          this.router.navigate([this.baseUrl + '/classes']);
        } else if (link === 'LICENSE') {
          this.router.navigate([this.baseUrl + '/license']);
        }
      }
    }
  }

  // For navbar
  performAction(link: string) {
    // Hiding navbar if it is mobile
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

  ngOnDestroy(): void {
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
    if (this.purchasedLicenseSubscription) {
      this.purchasedLicenseSubscription.unsubscribe();
    }
  }

}
