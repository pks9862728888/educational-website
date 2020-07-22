import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-student-workspace',
  templateUrl: './student-workspace.component.html',
  styleUrls: ['./student-workspace.component.css']
})
export class StudentWorkspaceComponent implements OnInit {

  constructor( private router: Router ) {}

  ngOnInit(): void {
  }

}
