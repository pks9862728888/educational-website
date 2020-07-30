import { InstituteApiService } from './../services/institute-api.service';
import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-coaching-workspace',
  templateUrl: './coaching-workspace.component.html',
  styleUrls: ['./coaching-workspace.component.css']
})
export class CoachingWorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
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
               private instituteApiService: InstituteApiService ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
    this.activeLink = 'COACHING_PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('profile')) {
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
      } else if (link === 'EXIT') {
        sessionStorage.setItem('activeRoute', 'INSTITUTES');
        sessionStorage.removeItem('currentInstituteSlug');
        sessionStorage.removeItem('currentInstituteRole');
        sessionStorage.removeItem('currentInstituteType');
        sessionStorage.removeItem('purchasedLicenseExists');
        sessionStorage.removeItem('selectedLicenseId');
        sessionStorage.removeItem('paymentComplete');
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
    if (this.showTempNamesSubscription) {
      this.showTempNamesSubscription.unsubscribe();
    }
    if (this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
  }

}
