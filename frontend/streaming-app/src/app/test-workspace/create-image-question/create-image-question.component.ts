import { MediaMatcher } from '@angular/cdk/layout';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { addQuestionFormValidator, islengthWithin20Validator } from 'src/app/custom.validator';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { SetFileQuestionsInterface,
         SetImageQuestionsInterface,
         TestMinDetailsResponseForImageTestQuestionCreation,
         TestQuestionSet } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { UiDialogComponent } from 'src/app/shared/ui-dialog/ui-dialog.component';
import { getFileSize } from 'src/app/shared/utilityFunctions';
import { QUESTION_SECTION_VIEW_TYPE, QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS } from 'src/constants';
import { MatChipInputEvent } from '@angular/material/chips';

@Component({
  selector: 'app-create-image-question',
  templateUrl: './create-image-question.component.html',
  styleUrls: ['./create-image-question.component.css']
})
export class CreateImageQuestionComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentTestSlug: string;
  currentInstituteRole: string;

  questionSetForm: FormGroup;
  uploadQuestionForm: FormGroup;
  addQuestionSectionForm: FormGroup;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;

  submitIndicatorAddQuestionSet: boolean;
  loadingSetQuestionsIndicator: boolean;
  loadingSetQuestionErrorText: string;
  reloadSetQuestions: boolean;

  addQuestionSectionIndicator: boolean;

  progress = 0;
  loadedFileSize = 0;
  totalFileSize = 0;

  showAddQuestionSetForm = false;
  showAddSectionForm = false;
  previewQuestionPaper = false;

  QUESTION_SECTION_VIEW_TYPE = QUESTION_SECTION_VIEW_TYPE;
  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;
  getFileSize = getFileSize;
  QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS = QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS;

  questionLabels = [
    {name: 'Label', id: 1}
  ];
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];

  testDetails: TestMinDetailsResponseForImageTestQuestionCreation;
  selectedSet: TestQuestionSet;
  setQuestions: SetFileQuestionsInterface;
  filename: string;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService,
    private dialog: MatDialog
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    const splittedPathName = window.location.pathname.split('/');
    this.currentInstituteSlug = splittedPathName[2];
    this.currentInstituteRole = splittedPathName[3].toUpperCase();
    this.currentSubjectSlug = splittedPathName[4];
    this.currentTestSlug = splittedPathName[5];
  }

  ngOnInit(): void {
    this.getTestDetails();
    this.questionSetForm = this.formBuilder.group({
      set_name: [null, [Validators.required, islengthWithin20Validator]]
    });
    this.addQuestionSectionForm = this.formBuilder.group({
      name: [null],
      section_mandatory: [null, [Validators.required]],
      view: [null, [Validators.required]],
      answer_all_questions: [null, [Validators.required]],
      no_of_question_to_attempt: [null, [Validators.required]]
    }, { validator: [addQuestionFormValidator, ] });
    this.uploadQuestionForm = this.formBuilder.group({
      file: [null, [Validators.required]]
    });
  }

  getTestDetails() {
    this.loadingIndicator = true;
    this.loadingError = null;
    this.reloadIndicator = false;
    this.instituteApiService.getTestMinDetailsForQuestionCreation(
      this.currentSubjectSlug,
      this.currentTestSlug
    ).subscribe(
      (result: TestMinDetailsResponseForImageTestQuestionCreation) => {
        this.loadingIndicator = false;
        this.testDetails = result;
        if (result.test_sets.length > 0) {
          this.selectedSet = result.test_sets[0];
        }
        this.setQuestions = result.first_set_questions;
        console.log(result);
      },
      errors => {
        this.loadingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingError = errors.error.error;
          } else {
            this.reloadIndicator = true;
          }
        } else {
          this.reloadIndicator = true;
        }
      }
    );
  }

  toggleAddQuestionSetForm() {
    this.questionSetForm.reset();
    this.questionSetForm.enable();
    this.showAddQuestionSetForm = !this.showAddQuestionSetForm;
  }

  addQuestionSet() {
    this.submitIndicatorAddQuestionSet = true;
    this.questionSetForm.disable();
    if (!this.questionSetForm.invalid) {
      this.instituteApiService.addTestQuestionSet(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.currentTestSlug,
        this.questionSetForm.value
      ).subscribe(
        (result: TestQuestionSet) => {
          this.submitIndicatorAddQuestionSet = false;
          this.testDetails.test_sets.push(result);
          this.selectedSet = result;
          console.log(result);
          this.toggleAddQuestionSetForm();
          this.uiService.showSnackBar(
            'Question set added successfully!',
            2000
          );
        },
        errors => {
          this.submitIndicatorAddQuestionSet = false;
          this.questionSetForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                3000
              );
            } else {
              this.uiService.showSnackBar(
                'Error! Unable to add question set at the moment.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to add question set at the moment.',
              3000
            );
          }
        }
      );
    }
  }

  confirmDeleteSet() {
    const dialogReference = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Are you sure you want to delete question set: ' + this.selectedSet.set_name + ' ?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogReference.afterClosed().subscribe(result => {
      if (result) {
        this.deleteQuestionSet(this.selectedSet);
      }
    });
  }

  deleteQuestionSet(selectedSet: TestQuestionSet) {
    this.selectedSet.delete = true;
    this.instituteApiService.deleteQuestionSet(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString()
    ).subscribe(
      () => {
        const index = +this.findIndexInArray(this.testDetails.test_sets, selectedSet.id);
        if (this.selectedSet.id === selectedSet.id) {
          this.selectedSet = null;
          this.setQuestions = null;
        }
        this.testDetails.test_sets.splice(index, 1);
        this.uiService.showSnackBar('Question set deleted successfully!', 2000);
      },
      errors => {
        this.selectedSet.delete = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete test set.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete test set.', 3000);
        }
      }
    );
  }

  getQuestionSetQuestions(questionSet: TestQuestionSet, retry = false) {
    this.showAddQuestionSetForm = false;

    if (retry || this.selectedSet && questionSet.id !== this.selectedSet.id) {
      this.selectedSet = questionSet;
      this.setQuestions = null;
      this.loadingSetQuestionsIndicator = true;
      this.loadingSetQuestionErrorText = null;
      this.reloadSetQuestions = false;
      this.instituteApiService.getTestSetQuestions(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.currentTestSlug,
        this.selectedSet.id.toString()
      ).subscribe(
        (result: SetImageQuestionsInterface) => {
          this.loadingSetQuestionsIndicator = false;
          this.setQuestions = result;
          console.log(result);
        },
        errors => {
          this.loadingSetQuestionsIndicator = false;
          if (errors.error) {
            if (errors.error.error) {
              this.loadingSetQuestionErrorText = errors.error.error;
            } else {
              this.reloadSetQuestions = true;
            }
          } else {
            this.reloadSetQuestions = true;
          }
        }
      );
    }
  }

  toggleAddQuestionSection() {
    this.resetAddQuestionSectionForm();
    this.addQuestionSectionForm.enable();
    this.addQuestionSectionIndicator = false;
    this.showAddSectionForm = !this.showAddSectionForm;
  }

  resetAddQuestionSectionForm() {
    this.addQuestionSectionForm.patchValue({
      name: '',
      no_of_question_to_attempt: 0,
      section_mandatory: true,
      answer_all_questions: true,
      view: QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION
    });
  }

  questionSectionViewChanged() {
    if (this.addQuestionSectionForm.value.view === QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION) {
      this.addQuestionSectionForm.patchValue({
        answer_all_questions: true,
      });
    }
  }

  addQuestionSection() {
    this.addQuestionSectionIndicator = true;
    const data = {...this.addQuestionSectionForm.value };
    if (data.answer_all_questions) {
      data.no_of_question_to_attempt = null;
    }
    if (data.view === QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION) {
      data.name = '';
    }
    console.log(data);
  }

  addQuestionLabelEvent(event: MatChipInputEvent): void {
    const input = event.input;
    const value = event.value;

    if  (value.length > 30) {
      this.uiService.showSnackBar('Concept labels should not exceed 30 characters.', 3000);
    } else {
      // Add our question label
      if ((value || '').trim()) {
        this.questionLabels.push({name: value.trim(), id: null});
      }

      // Reset the input value
      if (input) {
        input.value = '';
      }
    }
  }

  removeQuestionLabel(label) {
    console.log(label);
    const index = this.questionLabels.indexOf(label);

    if (index >= 0) {
      this.questionLabels.splice(index, 1);
    }
  }

  findIndexInArray(array, id: number) {
    for (const idx in array) {
      if (array[idx].id === id) {
        return idx;
      }
    }
    return -1;
  }

  showQuestionPaper() {
    this.filename = this.selectedSet.set_name.replace(' ', '').toLowerCase() + '.pdf';
    this.previewQuestionPaper = true;
  }

  closeQuestionPaperPreview() {
    this.previewQuestionPaper = false;
  }
}
