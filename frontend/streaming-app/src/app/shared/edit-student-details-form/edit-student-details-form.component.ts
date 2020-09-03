import { InstituteApiService } from './../../services/institute-api.service';
import { currentInstituteSlug, GENDER_FORM_FIELD_OPTIONS } from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { InstituteStudentMinDetails } from '../../models/student.model';
import { formatDate } from '../../format-datepicker';

@Component({
  selector: 'app-edit-student-details-form',
  templateUrl: './edit-student-details-form.component.html',
  styleUrls: ['./edit-student-details-form.component.css']
})
export class EditStudentDetailsFormComponent implements OnInit {

  mq: MediaQueryList;
  maxDate: Date;
  genderOptions = GENDER_FORM_FIELD_OPTIONS;
  error: string;
  editForm: FormGroup;
  @Output() hideEditFormEvent = new EventEmitter<void>();
  @Output() editedStudentDetails = new EventEmitter<InstituteStudentMinDetails>();
  @Input() student: InstituteStudentMinDetails;
  showSubmitIndicator: boolean;
  currentInstituteSlug: string;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.maxDate = new Date();
  }

  ngOnInit(): void {
    this.editForm = this.formBuilder.group({
      first_name: [null, [Validators.maxLength(30)]],
      last_name: [null, [Validators.maxLength(30)]],
      gender: [''],
      date_of_birth: [''],
      registration_no: [null, [Validators.maxLength(15)]],
      enrollment_no: [null, [Validators.maxLength(15)]]
    });
    this.resetEditForm();
  }

  resetEditForm() {
    this.editForm.patchValue({
      first_name: this.student.first_name,
      last_name: this.student.last_name,
      registration_no: this.student.registration_no,
      enrollment_no: this.student.enrollment_no,
      gender: this.student.gender,
      date_of_birth: this.student.date_of_birth
    });
  }

  submit() {
    let data = this.editForm.value;
    if (!data.first_name) {
      data['first_name'] = '';
    }
    if (!data.last_name) {
      data['last_name'] = '';
    }
    if (!data.registration_no) {
      data['registration_no'] = '';
    }
    if (!data.enrollment_no) {
      data['enrollment_no'] = '';
    }
    if (data.date_of_birth) {
      // Formatting date of birth in YYYY-MM-DD
      data.date_of_birth = formatDate(data.date_of_birth);
    }
    data['id'] = this.student.id;
    this.error = null;
    this.showSubmitIndicator = true;
    this.editForm.disable();
    this.instituteApiService.editInstituteStudentDetails(
      this.currentInstituteSlug,
      data
    ).subscribe(
      (result: InstituteStudentMinDetails) => {
        this.showSubmitIndicator = false;
        this.editedStudentDetails.emit(result);
      },
      errors => {
        this.showSubmitIndicator = false;
        this.editForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.error = errors.error.error;
          } else {
            this.error = 'Unable to update student details at the moment.';
          }
        } else {
          this.error = 'Unable to update student details at the moment.';
        }
      }
    )
  }

  hideEditForm() {
    this.hideEditFormEvent.emit();
  }

  closeEditError() {
    this.error = null;
  }
}
