import { Component, OnInit, DoCheck } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-workspace',
  templateUrl: './workspace.component.html',
  styleUrls: ['./workspace.component.css']
})
export class WorkspaceComponent implements OnInit {

  constructor(private router: Router,
              private route: ActivatedRoute) {}

  ngOnInit(): void {
    // Rendering appropriate workspace
    if (localStorage.getItem('is_student') === JSON.stringify(true)) {
      this.router.navigate(['/workspace/student-workspace']);
    } else if (localStorage.getItem('is_teacher') === JSON.stringify(true)) {
      this.router.navigate(['/workspace/teacher-workspace']);
    } else if (localStorage.getItem('is_staff') === JSON.stringify(true)) {
      this.router.navigate(['/workspace/staff-workspace']);
    } else {
      // Get the type of user and then again navigate to appropriate workspace
    }
  }

}
