import { authTokenName } from './../../constants';
import { InAppDataTransferService } from '../in-app-data-transfer.service';
import { Component, OnInit, OnDestroy, Renderer2, ElementRef, ViewChild } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { MediaMatcher } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-teacher-workspace',
  templateUrl: './teacher-workspace.component.html',
  styleUrls: ['./teacher-workspace.component.css']
})
export class TeacherWorkspaceComponent implements OnInit, OnDestroy {

  // For showing sidenav toolbar
  mobileQuery: MediaQueryList;
  opened: boolean;
  showInstituteViewSidenav: boolean;
  instituteSidenavViewSubscription: Subscription;
  activeLink: string;
  navbarActiveLinkSubscription: Subscription;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;

  constructor( private cookieService: CookieService,
               private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService,
               private renderer: Renderer2,
               private element: ElementRef ) {

    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');

    // Initializing sidenav active route in case page is reloaded
    const active_route = localStorage.getItem('activeRoute');
    if (active_route) {
      this.activeLink = active_route;
      if (this.activeLink !== 'PROFILE' && this.activeLink !== 'INSTITUTES' && this.activeLink !== 'CHATROOMS') {
        this.showInstituteViewSidenav = true;
      } else {
        this.showInstituteViewSidenav = false;
      }
    } else {
      localStorage.setItem('activeRoute', 'INSTITUTES');
      this.inAppDataTransferService.showInstituteSidenavView(false);
      this.activeLink = 'INSTITUTES';
    }

    // If auth token is already saved then redirecting to appropriate workspace
    if (this.cookieService.get(authTokenName)) {
      // Rendering appropriate workspace
      if (localStorage.getItem('is_teacher') === JSON.stringify(true)) {
        this.router.navigate(['/teacher-workspace']);
      } else if (localStorage.getItem('is_student') === JSON.stringify(true) ||
                 localStorage.getItem('is_staff') === JSON.stringify(true)) {
        this.router.navigate(['/**']);
      } else {
        // Get the type of user and then again navigate to appropriate workspace
      }
    } else {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }

    this.instituteSidenavViewSubscription = this.inAppDataTransferService.setInstituteSidenavView$.subscribe(
      (status: boolean) => {
        this.showInstituteViewSidenav = status;
        const active_link = localStorage.getItem('activeRoute');
        if (active_link === 'INSTITUTE_PROFILE') {
          this.activeLink = active_link;
        } else if (active_link === 'INSTITUTES') {
          // this.activeLink = active_link;       It wills how expression checked after checked error
        }
      }
    );

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
      } else if (link === 'INSTITUTE_PROFILE') {
        const instituteSlug = localStorage.getItem('currentInstituteSlug');
        this.router.navigate(['/teacher-workspace/institutes/preview/' + instituteSlug]);
      } else if (link === 'INSTITUTE_PERMISSIONS') {
        const instituteSlug = localStorage.getItem('currentInstituteSlug');
        this.router.navigate(['/teacher-workspace/institutes/' + instituteSlug + '/permissions']);
      } else if (link === 'INSTITUTE_CLASSES') {
        const instituteSlug = localStorage.getItem('currentInstituteSlug');
        this.router.navigate(['/teacher-workspace/institutes/' + instituteSlug + '/classes']);
      } else {
        if (this.activeLink === 'INSTITUTES') {
          this.showInstituteViewSidenav = false;
        }
        this.router.navigate(['/teacher-workspace/' + link.toLowerCase()]);
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

  emitShowInstituteListViewEvent() {
    this.tempBreadcrumbLinkName = '';
    this.inAppDataTransferService.showInstituteListView(true);
  }

  tempBreadCrumbNameExists() {
    if (this.tempBreadcrumbLinkName) {
      return true;
    } else {
      return false;
    }
  }

  ngOnDestroy(): void {
    this.instituteSidenavViewSubscription.unsubscribe();
  }

}
