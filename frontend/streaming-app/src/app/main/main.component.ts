import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  loggedIn = false;

  constructor(private cookieService: CookieService,
              private router: Router) { }

  ngOnInit() {
    // Checking whether token is present or not.
    const eduwebToken = this.cookieService.get('edu-web-token');
    if (eduwebToken) {
      this.loggedIn = true;
    } else {
      this.loggedIn = false;
    }
  }

  login() {
    console.log('Login Button has been clicked');
    this.router.navigate(['/authenticate']);
  }

  logout() {
    console.log('Logout button clicked');
    this.loggedIn = false;
  }

}
