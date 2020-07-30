import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';


@Component({
  selector: 'app-school-workspace',
  templateUrl: './school-workspace.component.html',
  styleUrls: ['./school-workspace.component.css']
})
export class SchoolWorkspaceComponent implements OnInit, OnDestroy {

  mobileQuery: MediaQueryList;
  currentInstituteSlug: string;
  baseUrl: string;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  constructor( private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService,
               private instituteApiService: InstituteApiService) {
    this.mobileQuery = this.media.matchMedia('(max-width: 768px)');
    this.activeLink = 'SCHOOL_PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('profile')) {
          this.activeLink = 'SCHOOL_PROFILE';
        } else if (val.url.includes('permissions')) {
          this.activeLink = 'SCHOOL_PERMISSIONS';
        } else if (val.url.includes('classes')) {
          this.activeLink = 'SCHOOL_CLASSES';
        } else if (val.url.includes('license')) {
          this.activeLink = 'LICENSE';
        }
      }
    });
    this.currentInstituteSlug = sessionStorage.getItem('currentInstituteSlug');
    this.baseUrl = '/school-workspace/' + this.currentInstituteSlug;
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }
    this.showTempNamesSubscription = this.inAppDataTransferService.activeBreadcrumbLinkData$.subscribe(
      (linkName: string) => {
        this.tempBreadcrumbLinkName = linkName;
      }
    );
    this.instituteApiService.getPaidUnexpiredLicenseDetails(sessionStorage.getItem('currentInstituteSlug')).subscribe(
      (result: {status: string}) => {
        sessionStorage.setItem('purchasedLicenseExists', result.status);
      }
    )
  }

  // For navigating to teacher-workspace view
  navigate(link: string) {
    if (link !== this.activeLink) {
      if (link === 'HOME') {
        this.router.navigate(['/home']);
      } else if (link === 'EXIT' || link === 'INSTITUTES') {
        sessionStorage.removeItem('currentInstituteSlug');
        sessionStorage.removeItem('currentInstituteRole');
        sessionStorage.removeItem('selectedLicenseId');
        sessionStorage.removeItem('currentInstituteType');
        sessionStorage.removeItem('paymentComplete');
        sessionStorage.removeItem('purchasedLicenseExists');
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        const instituteSlug = sessionStorage.getItem('currentInstituteSlug');
        if (link === 'SCHOOL_PROFILE') {
          this.router.navigate([this.baseUrl + '/profile']);
        } else if (link === 'SCHOOL_PERMISSIONS') {
          this.router.navigate([this.baseUrl + '/permissions']);
        } else if (link === 'SCHOOL_CLASSES') {
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
    if (this.mobileQuery.matches === true) {
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
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
  }

}
