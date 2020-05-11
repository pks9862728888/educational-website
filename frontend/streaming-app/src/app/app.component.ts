import { Component, OnInit, OnDestroy } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from './auth.service';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
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
  title = 'streaming-app';

  // Duration for showing snackbar
  durationInSeconds = 4;

  // Status button to show login and signup button controls
  showLoginSignupButton: boolean;
  showLogoutButton: boolean;

  // Subscription to logged status and user type
  private loggedinStatusSubscription: Subscription;

  constructor( private cookieService: CookieService,
               private authService: AuthService,
               private router: Router,
               private snackBar: MatSnackBar ) {}

  ngOnInit() {
    // Subscribing to know user logged in status
    this.loggedinStatusSubscription = this.authService.userLoggedInSignalSource$.subscribe(
      status => {
        if (status === true ) {
          this.showLogoutButton = true;
          this.showLoginSignupButton = false;
        } else {
          this.showLogoutButton = false;
          this.showLoginSignupButton = true;
        }
      }
    );

    // Checking whether user is logged in and broadcasting the logged in status
    if (this.cookieService.get('auth-token-edu-website')) {
      this.authService.sendLoggedinStatusSignal(true);
    } else {
      this.authService.sendLoggedinStatusSignal(false);
    }
  }

  // Clears token and saved info from local storage & then emits logged in signal as false
  logout() {
    this.cookieService.deleteAll();
    localStorage.clear();
    this.authService.sendLoggedinStatusSignal(false);
    this.snackBar.openFromComponent(SnackbarLoggedOutComponent, {
      duration: this.durationInSeconds * 1000,
    });
    this.router.navigate(['/home']);
  }

  getWorkSpaceRoute() {
    // Rendering appropriate workspace
    if (localStorage.getItem('is_student') === JSON.stringify(true)) {
      return ['/student-workspace'];
    } else if (localStorage.getItem('is_teacher') === JSON.stringify(true)) {
      return ['/teacher-workspace'];
    } else if (localStorage.getItem('is_staff') === JSON.stringify(true)) {
      return ['/staff-workspace'];
    } else {
      // Get the type of user and then again navigate to appropriate workspace
    }
  }

  // Unsubscribing from the subscriptions
  ngOnDestroy() {
    this.loggedinStatusSubscription.unsubscribe();
  }
}
