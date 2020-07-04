import { FormGroup, FormBuilder, Validators } from '@angular/forms';
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

  // Form
  instituteForm: FormGroup;

  constructor( private formBuilder: FormBuilder ) { }

  ngOnInit(): void {
    this.instituteForm = this.formBuilder.group({
      name: [null, [Validators.required, ]],
      country: ['IN', [Validators.required, ]],
    });
  }

  // If create institute is cancelled
  cancelClicked() {
    this.instituteCreated.emit('false');
  }

}
