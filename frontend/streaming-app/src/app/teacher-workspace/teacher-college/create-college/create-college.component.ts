import { COUNTRY_FORM_FIELD_OPTIONS, LANGUAGE_FORM_FIELD_OPTIONS, INSTITUTE_CATEGORY_FORM_FIELD_OPTIONS } from './../../../../constants';
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { STATE_FORM_FIELD_OPTIONS } from 'src/constants';

@Component({
  selector: 'app-create-college',
  templateUrl: './create-college.component.html',
  styleUrls: ['./create-college.component.css']
})
export class CreateCollegeComponent implements OnInit {

  // Form field options
  states = STATE_FORM_FIELD_OPTIONS;
  countries = COUNTRY_FORM_FIELD_OPTIONS;
  languages = LANGUAGE_FORM_FIELD_OPTIONS;
  instituteCategories = INSTITUTE_CATEGORY_FORM_FIELD_OPTIONS;

  // To control whether create institute is created or not
  @Output() instituteCreated = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

  // If create institute is cancelled
  cancelClicked() {
    this.instituteCreated.emit('false');
  }

}
