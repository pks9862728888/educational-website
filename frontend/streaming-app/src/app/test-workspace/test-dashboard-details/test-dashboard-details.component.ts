import { MediaMatcher } from '@angular/cdk/layout';
import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { characterLengthLessThanEqualTo, isNumberValidator, postiveIntegerValidator } from 'src/app/custom.validator';
import { getOnlyDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { SubjectTestFullDetailsResponse } from 'src/app/models/subject.model';
import { GRADED_TYPES, QUESTIONS_CATEGORY, QUESTION_MODE, TEST_SCHEDULE_TYPES } from 'src/constants';

@Component({
  selector: 'app-test-dashboard-details',
  templateUrl: './test-dashboard-details.component.html',
  styleUrls: ['./test-dashboard-details.component.css']
})
export class TestDashboardDetailsComponent implements OnInit {

  mq: MediaQueryList;
  @Input() testFullDetails: SubjectTestFullDetailsResponse;

  editTestForm: FormGroup;
  editTest = true;
  editingIndicator = false;

  GRADED_TYPES = GRADED_TYPES;
  TEST_SCHEDULE_TYPES = TEST_SCHEDULE_TYPES;
  QUESTIONS_CATEGORY = QUESTIONS_CATEGORY;
  getOnlyDateFromUnixTimeStamp = getOnlyDateFromUnixTimeStamp;

  currentDate: Date;
  maxDate: Date;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentDate = new Date();
    this.maxDate = new Date(this.currentDate.getFullYear() + 1,
                            this.currentDate.getMonth(),
                            this.currentDate.getDay());
  }

  ngOnInit(): void {
    this.editTestForm = this.formBuilder.group({
      name: [null, [Validators.required, characterLengthLessThanEqualTo(30)]],
      total_marks: [null, [Validators.required, postiveIntegerValidator]],
      total_duration: [null, [Validators.required, postiveIntegerValidator]],
      instruction: [null, [characterLengthLessThanEqualTo(200)]],
      no_of_optional_section_answer: [null, [Validators.required, isNumberValidator]],
      no_of_attempts: [null, [Validators.required, postiveIntegerValidator]],
      publish_result_automatically: [null, [Validators.required]],
      enable_peer_check: [null, [Validators.required]],
      allow_question_preview_10_min_before: [null, [Validators.required]],
      shuffle_questions: [null, [Validators.required]]
    });
    if (this.testFullDetails.test_schedule_type === TEST_SCHEDULE_TYPES.SPECIFIC_DATE) {
      this.editTestForm.controls.date.setValidators([Validators.required]);
    } else if (this.testFullDetails.test_schedule_type === TEST_SCHEDULE_TYPES.SPECIFIC_DATE_AND_TIME) {
      this.editTestForm.controls.date.setValidators([Validators.required]);
      this.editTestForm.controls.hour.setValidators([Validators.required]);
      this.editTestForm.controls.hour.setValidators([Validators.required]);
    }
    this.resetEditForm();
  }

  resetEditForm() {
    this.editTestForm.reset();
    this.editTestForm.enable();
    this.editTestForm.patchValue({
      name: this.testFullDetails.name,
      total_marks: this.testFullDetails.total_marks,
      total_duration: this.testFullDetails.total_duration,
      instruction: this.testFullDetails.instruction,
      no_of_optional_section_answer: this.testFullDetails.no_of_optional_section_answer,
      no_of_attempts: this.testFullDetails.no_of_attempts,
      publish_result_automatically: this.testFullDetails.publish_result_automatically,
      enable_peer_check: this.testFullDetails.enable_peer_check,
      allow_question_preview_10_min_before: this.testFullDetails.allow_question_preview_10_min_before,
      shuffle_questions: this.testFullDetails.shuffle_questions
    });
  }

  showEditTestForm() {
    this.resetEditForm();
    this.editTest = true;
  }


  getFullDateFromTimeStamp(timestampSchedule: number) {
    return new Date(timestampSchedule);
  }

}
