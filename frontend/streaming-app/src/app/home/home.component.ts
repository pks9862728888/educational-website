import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  loggedIn = false;

  constructor() { }

  ngOnInit() {
  }

  login() {
    console.log('Button has been clicked');
    this.loggedIn = true;
  }

  logout() {
    console.log('Logout button clicked');
    this.loggedIn = false;
  }

}
