import { Component, OnInit } from '@angular/core';
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
    if (localStorage.getItem('is_student')) {
      this.router.navigate(['/workspace/student-workspace']);
    } else if (localStorage.getItem('is_teacher')) {
      this.router.navigate(['/workspace/teacher-workspace']);
    } else if (localStorage.getItem('is_staff')) {
      this.router.navigate(['/workspace/staff-workspace']);
    }
  }

}
