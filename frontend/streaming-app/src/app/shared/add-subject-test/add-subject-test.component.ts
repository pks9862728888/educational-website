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
         SUBJECT_ADD_TEST_PLACE} from 'src/constants';
import { getSubjectTestAnswerMode, getSubjectTestQuestionMode, getSubjectTestType } from '../utilityFunctions';

@Component({
  selector: 'app-add-subject-test',
  templateUrl: './add-subject-test.component.html',
  styleUrls: ['./add-subject-test.component.css']
})
export class AddSubjectTestComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  addTestForm: FormGroup;
  currentDate: Date;
  maxDate: Date;
  @Input() shouldSetDateTime: boolean;
  @Input() viewKey: string;
  @Input() lectureId: string;
  @Output() closeAddTestEvent = new EventEmitter<void>();
  @Output() testCreatedData = new EventEmitter<any>();

  HOUR_CHOICES = [];
  MINUTE_CHOICES = [];

  GRADED_TYPES = GRADED_TYPES;
  QUESTION_MODE = QUESTION_MODE;
  ANSWER_MODE = ANSWER_MODE;
  QUESTIONS_CATEGORY = QUESTIONS_CATEGORY;
  GRADED_TYPE_FORM_FIELD_OPTIONS = GRADED_TYPE_FORM_FIELD_OPTIONS;
  QUESTION_MODE_FORM_FIELD_OPTIONS = QUESTION_MODE_FORM_FIELD_OPTIONS;
  ANSWER_MODE_FORM_FIELD_OPTIONS = ANSWER_MODE_FORM_FIELD_OPTIONS;
  QUESTIONS_CATEGORY_FORM_FIELD_OPTIONS = QUESTIONS_CATEGORY_FORM_FIELD_OPTIONS;
  MONTH_FORM_FIELD_OPTIONS = MONTH_FORM_FIELD_OPTIONS;
  getSubjectTestType = getSubjectTestType;
  getTestSchedule = getTestSchedule;
  getSubjectTestQuestionMode = getSubjectTestQuestionMode;
  getSubjectTestAnswerMode = getSubjectTestAnswerMode;

  showFormView = true;
  showSubmitIndicator = false;
  formError: string;

  constructor(
    private formBuilder: FormBuilder,
    private media: MediaMatcher,
    private uiService: UiService,
    private instituteApiService: InstituteApiService
  ) {
    this.currentDate = new Date();
    this.maxDate = new Date(this.currentDate.getFullYear() + 1,
                            this.currentDate.getMonth(),
                            this.currentDate.getDay());
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
  }

  ngOnInit(): void {
    for (let i = 0; i < 24; i++) {
      this.HOUR_CHOICES.push({value: i, viewValue: i});
    }
    for (let i = 0; i < 61; i++) {
      this.MINUTE_CHOICES.push({value: i, viewValue: i});
    }
    this.addTestForm = this.formBuilder.group({
      name: [null, [Validators.required, Validators.maxLength(30)]],
      type: [null, [Validators.required]],
      total_marks: [null, [Validators.required, postiveIntegerValidator]],
      total_duration: [null, [Validators.required, postiveIntegerValidator]],
      date: [null],
      hour: [null],
      minute: [null],
      instruction: ['Answer all the questions', [Validators.maxLength(200)]],
      no_of_optional_section_answer: [null, [Validators.required, isNumberValidator]],
      question_mode: [QUESTION_MODE.TYPED, [Validators.required]],
      answer_mode: [ANSWER_MODE.TYPED, [Validators.required]],
      question_category: [QUESTIONS_CATEGORY.AUTOCHECK_TYPE, [Validators.required]],
      no_of_attempts: [null, [Validators.required, postiveIntegerValidator]],
      publish_result_automatically: [true, [Validators.required]],
      enable_peer_check: [false, [Validators.required]],
      allow_question_preview_10_min_before: [true, [Validators.required]],
      allow_test_after_scheduled_date_and_time: [false, [Validators.required]],
      shuffle_questions: [true, [Validators.required]]
    });
    if (this.shouldSetDateTime) {
      this.addTestForm.get('date').setValidators([Validators.required]);
      this.addTestForm.get('hour').setValidators([Validators.required]);
      this.addTestForm.get('minute').setValidators([Validators.required]);
      this.addTestForm.updateValueAndValidity();
    }
    this.initializeForm();
  }

  initializeForm() {
    this.addTestForm.reset();
    this.addTestForm.patchValue({
      type: GRADED_TYPES.GRADED,
      instruction: 'Answer all the questions',
      no_of_optional_section_answer: 0,
      question_mode: QUESTION_MODE.TYPED,
      answer_mode: ANSWER_MODE.TYPED,
      question_category: QUESTIONS_CATEGORY.AUTOCHECK_TYPE,
      no_of_attempts: 1,
      publish_result_automatically: true,
      enable_peer_check: false,
      allow_question_preview_10_min_before: false,
      allow_test_after_scheduled_date_and_time: false,
      shuffle_questions: true
    });
    if (this.shouldSetDateTime) {
      this.addTestForm.patchValue({
        date: new Date()
      });
    }
    this.addTestForm.enable();
  }

  gradedTypeChanged() {
    const gradedType = this.addTestForm.value.type;
    if (gradedType === GRADED_TYPES.GRADED) {
      this.addTestForm.patchValue({
        no_of_attempts: 1
      });
    }
  }

  questionModeChanged() {
    const questionMode = this.addTestForm.value.question_mode;
    if (questionMode === QUESTION_MODE.FILE) {
      this.addTestForm.patchValue({
        answer_mode: ANSWER_MODE.FILE,
        question_category: QUESTIONS_CATEGORY.FILE_UPLOAD_TYPE,
        no_of_optional_section_answer: 0
      });
    } else if (questionMode === QUESTION_MODE.TYPED || questionMode === QUESTION_MODE.IMAGE) {
      this.addTestForm.patchValue({
        answer_mode: ANSWER_MODE.TYPED
      });
      if (this.addTestForm.value.question_category === QUESTIONS_CATEGORY.FILE_UPLOAD_TYPE) {
        this.addTestForm.patchValue({
          question_category: QUESTIONS_CATEGORY.ALL_TYPES
        });
      }
    }
  }

  answerModeChanged() {
    const answerMode = this.addTestForm.value.answer_mode;
    const questionMode = this.addTestForm.value.question_mode;

    if (answerMode === ANSWER_MODE.FILE && (questionMode === QUESTION_MODE.TYPED || questionMode === QUESTION_MODE.IMAGE)) {
      this.addTestForm.patchValue({
        answer_mode: ANSWER_MODE.TYPED
      });
      this.uiService.showSnackBar(
        'Answer mode should be TYPED if Question mode is TYPED or IMAGE!',
        3000
      );
    } else if (answerMode === ANSWER_MODE.TYPED && (questionMode === QUESTION_MODE.FILE)) {
      this.addTestForm.patchValue({
        answer_mode: ANSWER_MODE.FILE
      });
      this.uiService.showSnackBar(
        'Answer mode should be FILE if Question mode is FILE!',
        3000
      );
    }
  }

  questionCategoryChanged() {
    const questionMode = this.addTestForm.value.question_mode;
    const questionCategory = this.addTestForm.value.question_category;
    const peerCheck = this.addTestForm.value.enable_peer_check;

    if (questionCategory !== QUESTIONS_CATEGORY.FILE_UPLOAD_TYPE && questionMode === QUESTION_MODE.FILE) {
      this.addTestForm.patchValue({
        question_category: QUESTIONS_CATEGORY.FILE_UPLOAD_TYPE
      });
      this.uiService.showSnackBar(
        'Question category should be FILE UPLOAD TYPE if Question mode is FILE!',
        3000
      );
    } else if (questionCategory === QUESTIONS_CATEGORY.FILE_UPLOAD_TYPE &&
               (questionMode === QUESTION_MODE.TYPED || questionMode === QUESTION_MODE.IMAGE)) {
      this.addTestForm.patchValue({
        question_category: QUESTIONS_CATEGORY.ALL_TYPES
      });
      this.uiService.showSnackBar(
        'Question category should not be FILE UPLOAD TYPE if Question mode is TYPED or IMAGE!',
        3000
      );
    }

    if (this.addTestForm.value.question_category === QUESTIONS_CATEGORY.AUTOCHECK_TYPE && peerCheck) {
      this.addTestForm.patchValue({
        enable_peer_check: false
      });
    }
  }

  questionPreviewChanged() {
    const questionPreview = this.addTestForm.value.allow_question_preview_10_min_before;
    if (!this.addTestForm.value.date || !this.addTestForm.value.hour || !this.addTestForm.value.minute) {
      this.addTestForm.patchValue({
        allow_question_preview_10_min_before: false
      });
      this.uiService.showSnackBar(
        'Please set date and time of test first.',
        3000
      );
    }
  }

  allowTestAfterScheduledDateTimeChanged() {
    const allowTestAfterScheduledDateTime = this.addTestForm.value.allow_test_after_scheduled_date_and_time;
    if (!this.addTestForm.value.date || !this.addTestForm.value.hour || !this.addTestForm.value.minute) {
      this.addTestForm.patchValue({
        allow_test_after_scheduled_date_and_time: false
      });
      this.uiService.showSnackBar(
        'Please set date and time of test first.',
        3000
      );
    }
  }

  resetTime() {
    this.addTestForm.patchValue({
      hour: null,
      minute: null,
      allow_question_preview_10_min_before: false,
      allow_test_after_scheduled_date_and_time: false
    });
  }

  resetDate() {
    let dateNow = new Date();
    if (!this.shouldSetDateTime) {
      dateNow = null;
    }
    this.addTestForm.patchValue({
      date: dateNow
    });
    if (!dateNow) {
      this.addTestForm.patchValue({
        allow_question_preview_10_min_before: false,
        allow_test_after_scheduled_date_and_time: false
      });
    }
  }

  next(stepper: MatStepper) {
    this.addTestForm.patchValue({
      name: this.addTestForm.value.name.trim()
    });
    const sheduledDateAndTime = getUnixTimeStamp(this.addTestForm.value.date, this.addTestForm.value.hour, this.addTestForm.value.minute);
    const unixTimeNow = + new Date();
    if (unixTimeNow >= sheduledDateAndTime) {
      this.uiService.showSnackBar(
        'Error! Test date and time can not be in the past.',
        3000
      );
    } else if (!this.addTestForm.invalid) {
      this.showFormView = false;
      stepper.next();
    }
  }

  submit(stepper: MatStepper) {
    const data = {...this.addTestForm.value};
    const sheduledDateAndTime = getUnixTimeStamp(this.addTestForm.value.date,
                                                 this.addTestForm.value.hour,
                                                 this.addTestForm.value.minute);
    data.test_schedule = sheduledDateAndTime;
    delete data.date;
    delete data.hour;
    delete data.minute;

    if (this.viewKey) {
      data.view_key = this.viewKey;
      data.test_place = SUBJECT_ADD_TEST_PLACE.VIEW;
    } else if (this.lectureId) {
      data.lecture_id = this.lectureId;
      data.test_place = SUBJECT_ADD_TEST_PLACE.LECTURE;
    } else {
      data.test_place = SUBJECT_ADD_TEST_PLACE.GLOBAL;
    }
    console.log(data);
    this.closeFormError();
    this.showSubmitIndicator = true;
    this.instituteApiService.addSubjectTest(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      data
    ).subscribe(
      result => {
        this.showSubmitIndicator = false;
        this.testCreatedData.emit(result);
        this.uiService.showSnackBar(
          'Test created successfully!',
          2000
        );
      },
      errors => {
        this.showSubmitIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.formError = errors.error.error;
            this.showFormView = true;
            stepper.previous();
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to add test at the moment. Try again',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error! Unable to add test at the moment. Try again',
            3000
          );
        }
      }
    );
  }

  editForm(stepper: MatStepper) {
    this.showFormView = false;
    stepper.previous();
  }

  closeAddTest() {
    this.initializeForm();
    this.showFormView = true;
    this.closeAddTestEvent.emit();
  }

  closeFormError() {
    this.formError = null;
  }
}
