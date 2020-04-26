import { Component, OnInit, OnDestroy } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from './auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'streaming-app';

  // Status button to show login and signup button controls
  showLoginSignupButton: boolean;
  showLogoutButton: boolean;

  // Subscription to logged status
  private loggedinStatusSubscription: Subscription;

  constructor( private cookieService: CookieService,
               private authService: AuthService ) {}

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
  }

  // Unsubscribing from the subscriptions
  ngOnDestroy() {
    this.loggedinStatusSubscription.unsubscribe();
  }
}
