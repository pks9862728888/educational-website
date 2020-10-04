import { MediaMatcher } from '@angular/cdk/layout';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatStepper } from '@angular/material/stepper';
import { isNumberValidator, postiveIntegerValidator } from 'src/app/custom.validator';
import { getTestSchedule, getUnixTimeStamp } from 'src/app/format-datepicker';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { ANSWER_MODE,
         ANSWER_MODE_FORM_FIELD_OPTIONS,
         currentInstituteSlug,
         currentSubjectSlug,
         GRADED_TYPES,
         GRADED_TYPE_FORM_FIELD_OPTIONS,
         MONTH_FORM_FIELD_OPTIONS,
         QUESTIONS_CATEGORY,
         QUESTIONS_CATEGORY_FORM_FIELD_OPTIONS,
         QUESTION_MODE,
         QUESTION_MODE_FORM_FIELD_OPTIONS,
         SUBJECT_ADD_TEST_PLACE,
         TEST_SCHEDULE_TYPES} from 'src/constants';
import { getSubjectTestAnswerMode, getSubjectTestQuestionMode, getSubjectTestType } from '../utilityFunctions';

@Component({
  selector: 'app-add-subject-test',
  templateUrl: './add-subject-test.component.html',
  styleUrls: ['./add-subject-test.component.css']
})
export class AddSubjectTestComponent implements OnInit {

  @Input() viewKey: string;
  @Input() lectureId: string;
  @Output() closeAddTestEvent = new EventEmitter<void>();
  @Output() testCreatedData = new EventEmitter<any>();

  TEST_SCHEDULE_TYPES = TEST_SCHEDULE_TYPES;
  testScheduleType: string;

  constructor() {}

  ngOnInit(): void {}

  setTestScheduleType(type: string) {
    this.testScheduleType = type;
  }

  testCreated(data) {
    this.testCreatedData.emit(data);
  }

  closeAddTest() {
    this.testScheduleType = null;
    this.closeAddTestEvent.emit();
  }

  changeTestScheduleType() {
    this.testScheduleType = null;
  }
}
