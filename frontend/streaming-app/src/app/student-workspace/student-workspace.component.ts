import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-workspace',
  templateUrl: './student-workspace.component.html',
  styleUrls: ['./student-workspace.component.css']
})
export class StudentWorkspaceComponent implements OnInit {

  constructor( private cookieService: CookieService,
               private router: Router ) {
    // If auth token is already saved then redirecting to appropriate workspace
    if (this.cookieService.get('auth-token-edu-website')) {
      // Rendering appropriate workspace
      if (localStorage.getItem('is_student') === JSON.stringify(true)) {
        this.router.navigate(['/student-workspace']);
      } else if (
        localStorage.getItem('is_teacher') === JSON.stringify(true) ||
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
  }

}
