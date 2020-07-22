import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-staff-workspace',
  templateUrl: './staff-workspace.component.html',
  styleUrls: ['./staff-workspace.component.css']
})
export class StaffWorkspaceComponent implements OnInit {

  constructor(private router: Router) {}

  ngOnInit(): void {
  }

}
