import { MediaMatcher } from '@angular/cdk/layout';
import { authTokenName, webAppName } from './../constants';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from './services/auth.service';
import { Subscription } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'snack-bar-component-logout-snack',
  template: `
    <div class="logged-out-successfully">
      Successfully logged out :)
    </div>
  `,
  styles: [`
    .logged-out-successfully {
      color: hotpink;
      text-align: center;
    }
  `],
})
export class SnackbarLoggedOutComponent { }

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  title = webAppName;
  hideNavbar: boolean;
  routerEventsSubscription: Subscription;

  // For tracking whether device is mobile
  mobileQuery: MediaQueryList;

  // Duration for showing snackbar
  durationInSeconds = 4;

  // Status button to show login and signup button controls
  showLoginSignUpButton: boolean;
  showLogoutButton: boolean;

  // Counts number of notifications
  newNotificationCount = 12;

  // Subscription to logged status and user type
  private loggedInStatusSubscription: Subscription;

  constructor( private media: MediaMatcher,
               private cookieService: CookieService,
               private authService: AuthService,
               private router: Router,
               private snackBar: MatSnackBar ) {
    this.mobileQuery = this.media.matchMedia('(max-width: 600px)');
    this.routerEventsSubscription = router.events.subscribe(val => {
      if (val instanceof NavigationEnd) {
        if(val.url.includes('preview-course-workspace')) {
          this.hideNavbar = true;
        } else {
          this.hideNavbar = false;
        }
      }
    });
  }

  ngOnInit() {
    // Subscribing to know user logged in status
    this.loggedInStatusSubscription = this.authService.userLoggedInSignalSource$.subscribe(
      (status: boolean) => {
        if (status === true ) {
          this.showLogoutButton = true;
          this.showLoginSignUpButton = false;
        } else {
          this.showLogoutButton = false;
          this.showLoginSignUpButton = true;
        }
      }
    );

    // Checking whether user is logged in and broadcasting the logged in status
    if (this.cookieService.get(authTokenName)) {
      this.authService.sendLoggedInStatusSignal(true);
    } else {
      this.authService.sendLoggedInStatusSignal(false);
    }
  }

  // Clears token and saved info from local storage & then emits logged in signal as false
  logout() {
    this.authService.logout();
    this.snackBar.openFromComponent(SnackbarLoggedOutComponent, {
      duration: this.durationInSeconds * 1000,
    });
    this.router.navigate(['/home']);
  }

  getWorkSpaceRoute() {
    if (sessionStorage.getItem('is_student') === JSON.stringify(true)) {
      return ['/student-workspace'];
    } else if (sessionStorage.getItem('is_teacher') === JSON.stringify(true)) {
      return ['/teacher-workspace'];
    } else if (sessionStorage.getItem('is_staff') === JSON.stringify(true)) {
      return ['/staff-workspace'];
    }
  }

  // Unsubscribing from the subscriptions
  ngOnDestroy() {
    if (this.loggedInStatusSubscription) {
      this.loggedInStatusSubscription.unsubscribe();
    }
  }
}
