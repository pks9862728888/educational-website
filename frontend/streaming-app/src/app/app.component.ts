import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'streaming-app';

  showLoginSignupButton: boolean;
  showLogoutButton: boolean;

  constructor( private cookieService: CookieService ) {}

  ngOnInit() {
    if (this.cookieService.get('auth-token-edu-website')) {
      this.showLoginSignupButton = false;
      this.showLogoutButton = true;
    } else {
      this.showLoginSignupButton = true;
      this.showLogoutButton = false;
    }
  }

  // On clicking logout clears token and saved info from local storage
  logout() {
    this.cookieService.deleteAll();
    localStorage.clear();
  }
}
