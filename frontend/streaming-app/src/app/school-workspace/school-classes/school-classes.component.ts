import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-school-classes',
  templateUrl: './school-classes.component.html',
  styleUrls: ['./school-classes.component.css']
})
export class SchoolClassesComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    localStorage.setItem('activeRoute', 'SCHOOL_CLASSES');
  }

}
