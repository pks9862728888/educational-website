import { InAppDataTransferService } from '../services/in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-college-workspace',
  templateUrl: './college-workspace.component.html',
  styleUrls: ['./college-workspace.component.css']
})
export class CollegeWorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
  mobileQuery: MediaQueryList;
  opened: boolean;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  routerEventsSubscription: Subscription;

  constructor( private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService ) {

    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
    this.activeLink = 'COLLEGE_PROFILE';
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('profile')) {
          this.activeLink = 'COLLEGE_PROFILE';
        } else if (val.url.includes('permissions')) {
          this.activeLink = 'COLLEGE_PERMISSIONS';
        } else if (val.url.includes('license')) {
          this.activeLink = 'LICENSE';
        }
      }
    });
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
  }

  // For navigating to teacher-workspace view
  navigate(link: string) {
    if (link !== this.activeLink) {
      this.activeLink = link;

      if (this.activeLink === 'HOME') {
        this.router.navigate(['/home']);
      } else if (this.activeLink === 'EXIT') {
        sessionStorage.setItem('activeRoute', 'INSTITUTES');
        sessionStorage.removeItem('currentInstituteSlug');
        sessionStorage.removeItem('currentInstituteRole');
        this.router.navigate(['/teacher-workspace/institutes']);
      } else {
        const instituteSlug = sessionStorage.getItem('currentInstituteSlug');
        if (this.activeLink === 'COLLEGE_PROFILE') {
          this.router.navigate(['/college-workspace/' + instituteSlug + '/profile']);
        } else if (this.activeLink === 'COLLEGE_PERMISSIONS') {
          this.router.navigate(['/college-workspace/' + instituteSlug + '/permissions']);
        } else if (this.activeLink === 'COLLEGE_CLASSES') {
          this.router.navigate(['/college-workspace/' + instituteSlug + '/classes']);
        } else if (this.activeLink === 'LICENSE') {
          this.router.navigate(['/college-workspace/' + instituteSlug + '/license']);
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
    if(this.routerEventsSubscription) {
      this.routerEventsSubscription.unsubscribe();
    }
  }

}
