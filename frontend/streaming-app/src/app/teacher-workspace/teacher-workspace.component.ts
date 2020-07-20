import { authTokenName } from './../../constants';
import { InAppDataTransferService } from '../in-app-data-transfer.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
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
  activeLink: string;
  showTempNamesSubscription: Subscription;
  tempBreadcrumbLinkName: string;
  subscribed = true;

  constructor( private cookieService: CookieService,
               private router: Router,
               private media: MediaMatcher,
               private inAppDataTransferService: InAppDataTransferService ) {

    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');

    // Initializing sidenav active route in case page is reloaded
    const active_route = localStorage.getItem('activeRoute');
    if (active_route && (active_route === 'PROFILE' || active_route === 'INSTITUTES' || active_route === 'CHATROOMS')) {
      this.activeLink = active_route;
    } else {
      localStorage.setItem('activeRoute', 'PROFILE');
      this.activeLink = 'PROFILE';
    }

    // Disallowing student and staff to view this workspace
    if (this.cookieService.get(authTokenName)) {
      // Rendering appropriate workspace
      if (localStorage.getItem('is_student') === JSON.stringify(true) ||
                 localStorage.getItem('is_staff') === JSON.stringify(true)) {
        this.router.navigate(['/**']);
      } else {
        // Get the type of user and then again navigate to appropriate workspace
      }
    } else {
      this.subscribed = false;
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
      } else {
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
    if (this.subscribed) {
      this.showTempNamesSubscription.unsubscribe();
    }
  }

}
