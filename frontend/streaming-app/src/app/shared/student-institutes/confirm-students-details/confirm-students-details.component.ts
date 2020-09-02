import { formatDate } from 'src/app/format-datepicker';
import { GENDER_FORM_FIELD_OPTIONS } from './../../../../constants';
import { InstituteApiService } from './../../../services/institute-api.service';
import { Component, OnInit, Inject } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { StudentConfirmProfileDataInterface } from '../../../models/institute.model';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';


@Component({
  selector: 'app-confirm-students-details',
  templateUrl: './confirm-students-details.component.html',
  styleUrls: ['./confirm-students-details.component.css']
})
export class ConfirmStudentsDetailsComponent implements OnInit {

  showLoadingIndicator: boolean;
  showReloadIndicator: boolean;
  errorText: string;
  editForm: FormGroup;
  profileDetails: StudentConfirmProfileDataInterface;
  genderOptions = GENDER_FORM_FIELD_OPTIONS;
  maxDate: Date;
  showSubmitIndicator: boolean;
  submitError: string;

  constructor(
    private instituteApiService: InstituteApiService,
    private formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data: {
      instituteSlug: string;
    }
  ) {
    this.maxDate = new Date();
  }

  ngOnInit(): void {
    this.loadProfileData();
  }

  loadProfileData() {
    this.showLoadingIndicator = true;
    this.showReloadIndicator = false;
    this.errorText = null;
    this.instituteApiService.loadStudentConfirmProfileDetails(
      this.data.instituteSlug
    ).subscribe(
      (result: StudentConfirmProfileDataInterface) => {
        this.profileDetails = result;
        this.editForm = this.formBuilder.group({
          first_name: [null, [Validators.maxLength(30)]],
          last_name: [null, [Validators.maxLength(30)]],
          gender: [''],
          date_of_birth: [null]
        });
        this.resetEditForm();
        this.showLoadingIndicator = false;
      },
      errors => {
        this.showLoadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.errorText = errors.error.error;
          } else {
            this.showReloadIndicator = true;
          }
        } else {
          this.showReloadIndicator = true;
        }
      }
    )
  }

  resetEditForm() {
    this.editForm.patchValue({
      first_name: this.profileDetails.first_name,
      last_name: this.profileDetails.last_name,
      gender: this.profileDetails.gender,
      date_of_birth: this.profileDetails.date_of_birth
    });
  }

  submit() {
    this.submitError = null;
    this.showSubmitIndicator = true;
    this.editForm.patchValue({
      first_name: this.editForm.value.first_name.trim(),
      last_name: this.editForm.value.last_name.trim(),
      gender: this.editForm.value.gender.trim(),
    });
    let data = this.editForm.value
    if (!data.first_name) {
      data.first_name = '';
    }
    if (!data.last_name) {
      data.last_name = '';
    }
    if (!data.date_of_birth) {
      data.date_of_birth = formatDate(data.date_of_birth);
    }
    this.instituteApiService.studentJoinInstitute(
      this.data.instituteSlug,
      data
    ).subscribe(
      () => {
        this.showSubmitIndicator = false;
        document.getElementById('close').click();
      },
      errors => {
        this.showSubmitIndicator = false;
        if (errors.error) {
          if(errors.error.error) {
            this.submitError = errors.error.error;
          } else {
            this.submitError = 'Error! Unable to join institute.';
          }
        } else {
          this.submitError = 'Error! Unable to join institute.';
        }
      }
    )
  }

  closeSubmitError() {
    this.submitError = null;
  }
}
