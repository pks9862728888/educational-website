import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { islengthWithin20Validator } from 'src/app/custom.validator';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { SetQuestionsInterface, TestMinDetailsResponseForQuestionCreation, TestQuestionSet } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { getFileSize } from 'src/app/shared/utilityFunctions';

@Component({
  selector: 'app-create-file-question',
  templateUrl: './create-file-question.component.html',
  styleUrls: ['./create-file-question.component.css']
})
export class CreateFileQuestionComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentTestSlug: string;
  currentInstituteRole: string;
  questionSetForm: FormGroup;
  uploadQuestionPaperForm: FormGroup;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;
  submitIndicatorAddQuestionSet: boolean;
  loadingSetQuestionsIndicator: boolean;
  loadingSetQuestionErrorText: string;
  reloadSetQuestions: boolean;
  uploadQuestionPaperIndicator: boolean;
  progress = 0;
  loadedFileSize = 0;
  totalFileSize = 0;

  showAddQuestionSetForm = false;

  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;
  getFileSize = getFileSize;

  testDetails: TestMinDetailsResponseForQuestionCreation;
  selectedSet: TestQuestionSet;
  setQuestions: SetQuestionsInterface;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
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
    this.uploadQuestionPaperForm = this.formBuilder.group({
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
      (result: TestMinDetailsResponseForQuestionCreation) => {
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

  getQuestionSetQuestions(questionSet: TestQuestionSet, retry=false) {
    this.showAddQuestionSetForm = false;

    if (retry || this.selectedSet && questionSet.id !== this.selectedSet.id) {
      this.selectedSet = questionSet;
      // Load Questions
    }
  }

  uploadQuestionPaper() {
    const file: File = (document.getElementById('pdf-file-upload') as HTMLInputElement).files[0];

    if (!file.type.includes('application/pdf') || !file.name.endsWith('.pdf') || file.name.includes('.exe') || file.name.includes('.sh')) {
      this.uploadQuestionPaperForm.patchValue({
        file: null
      });
      this.uiService.showSnackBar(
        'Only Pdf files with .pdf extensions can be uploaded.',
        3000
      );
    } else {
      this.uploadQuestionPaperIndicator = true;
      console.log(file);
      this.instituteApiService.uploadFileQuestionPaper(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.currentTestSlug,
        this.selectedSet.id.toString(),
        { file }
      ).subscribe(
        result => {
          // this.uploadQuestionPaperIndicator = false;
          console.log(result);
        },
        errors => {
          this.uploadQuestionPaperIndicator = false;
        }
      );
    }
  }
}
