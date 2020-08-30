import { MediaMatcher } from '@angular/cdk/layout';
import { environment } from './../../../environments/environment';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, Output, EventEmitter } from '@angular/core';

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

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.error = 'sdfsdfs';
  }

  ngOnInit(): void {
    this.editForm = this.formBuilder.group({
      first_name: [null, [Validators.maxLength(30)]],
      last_name: [null, [Validators.maxLength(30)]],
      registration_no: [null, [Validators.maxLength(15)]],
      enrollment_no: [null, [Validators.maxLength(15)]]
    });
  }

  resetEditForm() {
    this.editForm.patchValue({
      first_name: '',
      last_name: '',
      registration_no: '',
      enrollment_no: ''
    })
  }

  submit() {
    console.log(this.editForm.value);
  }

  hideEditForm() {
    this.hideEditFormEvent.emit();
  }

  closeEditError() {
    this.error = null;
  }

}
