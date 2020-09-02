import { InstituteApiService } from './../../services/institute-api.service';
import { currentInstituteSlug } from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { environment } from './../../../environments/environment';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { InstituteStudentMinDetails } from '../../models/student.model';

@Component({
  selector: 'app-edit-student-details-form',
  templateUrl: './edit-student-details-form.component.html',
  styleUrls: ['./edit-student-details-form.component.css']
})
export class EditStudentDetailsFormComponent implements OnInit {

  mq: MediaQueryList;
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
  }

  ngOnInit(): void {
    this.editForm = this.formBuilder.group({
      first_name: [null, [Validators.maxLength(30)]],
      last_name: [null, [Validators.maxLength(30)]],
      registration_no: [null, [Validators.maxLength(15)]],
      enrollment_no: [null, [Validators.maxLength(15)]]
    });
    this.editForm.patchValue({
      first_name: this.student.first_name,
      last_name: this.student.last_name,
      registration_no: this.student.registration_no,
      enrollment_no: this.student.enrollment_no
    });
  }

  resetEditForm() {
    this.editForm.patchValue({
      first_name: this.student.first_name,
      last_name: this.student.last_name,
      registration_no: this.student.registration_no,
      enrollment_no: this.student.enrollment_no
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
    data['id'] = this.student.id;
    console.log(data);
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
