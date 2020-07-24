import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { COUNTRY_FORM_FIELD_OPTIONS, LANGUAGE_FORM_FIELD_OPTIONS, INSTITUTE_CATEGORY_FORM_FIELD_OPTIONS, INSTITUTE_TYPE_FORM_FIELD_OPTIONS } from './../../../../constants';
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { STATE_FORM_FIELD_OPTIONS } from 'src/constants';
import { InstituteApiService } from 'src/app/institute-api.service';

interface CreatedInstituteResponse {
  created: boolean;
  url: string;
}

@Component({
  selector: 'app-create-institute',
  templateUrl: './create-institute.component.html',
  styleUrls: ['./create-institute.component.css']
})
export class CreateInstituteComponent implements OnInit {

  // Form field options
  states = STATE_FORM_FIELD_OPTIONS;
  countries = COUNTRY_FORM_FIELD_OPTIONS;
  languages = LANGUAGE_FORM_FIELD_OPTIONS;
  instituteCategories = INSTITUTE_CATEGORY_FORM_FIELD_OPTIONS;
  instituteTypes = INSTITUTE_TYPE_FORM_FIELD_OPTIONS;

  // To control whether create institute is created or not
  @Output() instituteCreated = new EventEmitter();

  // Form
  instituteForm: FormGroup;
  phoneNumberError: string;
  urlError: string;
  nameError: string;
  errorOccurred: boolean;

  constructor( private formBuilder: FormBuilder,
               private instituteApiService: InstituteApiService ) { }

  ngOnInit(): void {
    this.instituteForm = this.formBuilder.group({
      name: ['', [
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(150)
      ]],
      country: ['IN', [Validators.required, ]],
      institute_category: ['E', [Validators.required, ]],
      type: ['', [Validators.required, ]],
      institute_profile: this.formBuilder.group ({
        motto: ['', [Validators.maxLength(256), ]],
        email: ['', [Validators.email, ]],
        phone: ['', ],
        website_url: ['', ],
        state: ['', ],
        pin: ['', [Validators.maxLength(10), ]],
        address: ['', [Validators.maxLength(50), ]],
        recognition: ['', [Validators.maxLength(30), ]],
        primary_language: ['EN', [Validators.required, ]],
        secondary_language: ['', ],
        tertiary_language: ['', ]
      })
    });
  }

  // If create institute is cancelled
  cancelClicked() {
    this.instituteCreated.emit({
      status: false,
    });
  }

  // Reset the form
  resetClicked() {
    this.instituteForm.reset({
      institute_category: 'E',
      type: null,
      country: 'IN',
      institute_profile: {
        primary_language: 'EN'
      }
    });
  }

  resetErrorResponses() {
    this.errorOccurred = false;
    this.nameError = null;
    this.urlError = null;
    this.phoneNumberError = null;
  }

  // Submit the data
  instituteFormSubmit() {
    this.resetErrorResponses();
    this.instituteApiService.createInstitute(this.instituteForm.value).subscribe(
      (result: CreatedInstituteResponse) => {
        this.instituteCreated.emit({
          status: true,
          url: result.url,
          type: this.instituteForm.value.type
        });
      },
      errors => {
        this.errorOccurred = true;

        if (errors.error) {
          if (errors.error.created === 'false') {
            this.nameError = errors.error.message;
          } else if (errors.error.institute_profile) {
            if (errors.error.institute_profile.phone) {
              this.phoneNumberError = errors.error.institute_profile.phone[0];
            }
            if (errors.error.institute_profile.website_url) {
              this.urlError = errors.error.institute_profile.website_url[0];
            }
          }
        }
      }
    );
  }
}
