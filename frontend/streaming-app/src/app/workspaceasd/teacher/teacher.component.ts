import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-teacher',
  templateUrl: './teacher.component.html',
  styleUrls: ['./teacher.component.css']
})
export class TeacherComponent implements OnInit {

  // For breadcrumb
  homeLinkActive = false;
  workspaceLinkActive = true;

  constructor( private router: Router ) { }

  ngOnInit(): void {
    this.workspaceLinkActive = true;
  }

  // For breadcrumb
  workspaceClicked() {
    this.workspaceLinkActive = true;
    this.homeLinkActive = false;
    this.router.navigate(['/workspace/teacher-workspace']);
  }

  // For expansion panel
}
