import { InterModuleDataTransferService } from './../inter-module-data-transfer.service';
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

  // For breadcrumb
  activeLink: string;
  secondaryActiveLink: string;
  instituteActiveLinkSubscription: Subscription;

  constructor( private cookieService: CookieService,
               private router: Router,
               private media: MediaMatcher,
               private interModuleDataTransferService: InterModuleDataTransferService ) {

    this.mobileQuery = media.matchMedia('(max-width: 600px)');

    // If auth token is already saved then redirecting to appropriate workspace
    if (this.cookieService.get('auth-token-edu-website')) {
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

    // Setting active link
    this.activeLink = 'INSTITUTES';
  }

  ngOnInit(): void {
    // For keeping the sidenav opened in desktop view in the beginning
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    } else {
      this.opened = true;
    }

    this.instituteActiveLinkSubscription = this.interModuleDataTransferService.activeBreadcrumbLinkData$.subscribe(
      (data: string) => {
        this.secondaryActiveLink = data;
      }
    );
  }

  // For breadcrumb
  navigateClicked(link) {
    if (link !== this.activeLink) {
      this.activeLink = link;

      if (this.activeLink === 'HOME') {
        this.router.navigate(['\home']);
      }
    }
  }

  // For navbar
  hideNavbarInMobile(link: string) {
    if (this.mobileQuery.matches === true) {
      this.opened = false;
    }

    this.navigateClicked(link);
  }

  emitEvent(navigate: string) {
    if (navigate === 'INSTITUTES') {
      this.interModuleDataTransferService.showInstituteListView(true);
      this.secondaryActiveLink = '';
    }
  }

  ngOnDestroy(): void {
    this.instituteActiveLinkSubscription.unsubscribe();
  }

}
