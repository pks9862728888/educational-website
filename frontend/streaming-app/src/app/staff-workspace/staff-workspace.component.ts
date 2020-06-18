import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-staff-workspace',
  templateUrl: './staff-workspace.component.html',
  styleUrls: ['./staff-workspace.component.css']
})
export class StaffWorkspaceComponent implements OnInit {

  constructor( private cookieService: CookieService,
               private router: Router) {
    // If auth token is already saved then redirecting to appropriate workspace
    if (this.cookieService.get('auth-token-edu-website')) {
      // Rendering appropriate workspace
      if (localStorage.getItem('is_staff') === JSON.stringify(true)) {
        this.router.navigate(['/staff-workspace']);
      } else if (
        localStorage.getItem('is_student') === JSON.stringify(true) ||
        localStorage.getItem('is_teacher') === JSON.stringify(true)) {
        this.router.navigate(['/**']);
      } else {
        // Get the type of user and then again navigate to appropriate workspace
      }
    } else {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit(): void {
  }

}
