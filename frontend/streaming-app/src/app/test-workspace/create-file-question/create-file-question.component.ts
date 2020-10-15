import { MediaMatcher } from '@angular/cdk/layout';
import { HttpEventType } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { islengthWithin20Validator } from 'src/app/custom.validator';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { FileQuestionsInterface,
         TestMinDetailsResponseForFileTestQuestionCreation,
         TestQuestionSetInterface } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { UiDialogComponent } from 'src/app/shared/ui-dialog/ui-dialog.component';
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
  uploadError: string;
  progress = 0;
  loadedFileSize = 0;
  totalFileSize = 0;

  showAddQuestionSetForm = false;
  previewQuestionPaper = false;

  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;
  getFileSize = getFileSize;

  testDetails: TestMinDetailsResponseForFileTestQuestionCreation;
  selectedSet: TestQuestionSetInterface;
  setQuestions: FileQuestionsInterface;
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
      (result: TestMinDetailsResponseForFileTestQuestionCreation) => {
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
        (result: TestQuestionSetInterface) => {
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

  deleteQuestionSet(selectedSet: TestQuestionSetInterface) {
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

  getQuestionSetQuestions(questionSet: TestQuestionSetInterface, retry = false) {
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
        (result: FileQuestionsInterface) => {
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
      this.loadedFileSize = 0;
      this.totalFileSize = file.size;
      this.uploadQuestionPaperIndicator = true;
      this.uploadQuestionPaperForm.disable();
      this.uploadError = null;

      this.instituteApiService.uploadFileQuestionPaper(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.currentTestSlug,
        this.selectedSet.id.toString(),
        { file }
      ).subscribe(
        (result: {type: number; loaded: number; total: number; file: string; id: number; body: any; }) => {
          if (result.type === HttpEventType.UploadProgress) {
            this.progress = Math.round(100 * result.loaded / result.total);
            this.loadedFileSize = result.loaded;
            this.totalFileSize = result.total;
          } else if (result.type === HttpEventType.Response) {
            this.setQuestions = result.body;
            this.uploadQuestionPaperIndicator = false;
            this.uploadQuestionPaperForm.reset();
            this.uploadQuestionPaperForm.enable();
            this.uiService.showSnackBar(
              'Question paper uploaded successfully.',
              3000
            );
          }
        },
        errors => {
          this.uploadQuestionPaperIndicator = false;
          this.uploadQuestionPaperForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.uploadError = errors.error.error;
            } else {
              this.uiService.showSnackBar(
                'Error! Unable to upload at the moment.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to upload at the moment.',
              3000
            );
          }
        }
      );
    }
  }

  confirmDeleteQuestionPaper() {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Are you sure you want to delete question paper?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteQuestionPaper();
      }
    });
  }

  findIndexInArray(array, id) {
    for (const idx in array) {
      if (array[idx].id === id) {
        return idx;
      }
    }
    return -1;
  }

  deleteQuestionPaper() {
    this.setQuestions.delete = true;
    this.instituteApiService.deleteTestFileUploadQuestionPaper(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString()
    ).subscribe(
      () => {
        this.setQuestions = null;
        this.uiService.showSnackBar(
          'Question paper file delete successful!',
          3000
        );
        this.selectedSet.active = false;
        this.selectedSet.verified = false;
        this.selectedSet.mark_as_final = false;
        const index = +this.findIndexInArray(this.testDetails.test_sets, this.selectedSet.id);
        this.testDetails.test_sets.splice(index, 1, this.selectedSet);
      },
      errors => {
        this.setQuestions.delete = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              3000
            );
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to delete question paper at the moment. Try again',
              3000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error! Unable to delete question paper at the moment. Try again.',
            3000
          );
        }
      }
    );
  }

  showQuestionPaper() {
    this.filename = this.selectedSet.set_name.replace(' ', '').toLowerCase() + '.pdf';
    this.previewQuestionPaper = true;
  }

  closeQuestionPaperPreview() {
    this.previewQuestionPaper = false;
  }

  closeUploadError() {
    this.uploadError = null;
  }
}
