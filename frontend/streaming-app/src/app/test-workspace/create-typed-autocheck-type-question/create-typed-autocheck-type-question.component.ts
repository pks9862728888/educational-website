import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MediaMatcher } from '@angular/cdk/layout';
import { HttpEventType } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatChipInputEvent } from '@angular/material/chips';
import { MatDialog } from '@angular/material/dialog';
import { addQuestionFormValidator,
         characterLengthLessThanEqualTo,
         postiveIntegerValidator } from 'src/app/custom.validator';
import { getDateFromUnixTimeStamp } from 'src/app/format-datepicker';
import { QuestionAnswerOptions, SubjectTypedTestQuestions,
         TestConceptLabelInterface,
         TestMinDetailsResponseForTypedTestQuestionCreation,
         TestQuestionSetInterface,
         TypedQuestionsSectionInterface} from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { UiDialogComponent } from 'src/app/shared/ui-dialog/ui-dialog.component';
import { getFileSize } from 'src/app/shared/utilityFunctions';
import { AUTOCHECK_TYPE_QUESTIONS, AUTOCHECK_TYPE_QUESTION_FORM_FIELD_OPTIONS,
         QUESTION_SECTION_VIEW_TYPE,
         QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS } from 'src/constants';

@Component({
  selector: 'app-create-typed-autocheck-type-question',
  templateUrl: './create-typed-autocheck-type-question.component.html',
  styleUrls: ['./create-typed-autocheck-type-question.component.css']
})
export class CreateTypedAutocheckTypeQuestionComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  currentTestSlug: string;
  currentInstituteRole: string;

  questionSetForm: FormGroup;
  editQuestionSetForm: FormGroup;
  addQuestionForm: FormGroup;
  editQuestionForm: FormGroup;
  addQuestionSectionForm: FormGroup;
  editQuestionSectionForm: FormGroup;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;

  submitIndicatorAddQuestionSet: boolean;
  loadingSetQuestionsIndicator: boolean;
  loadingSetQuestionErrorText: string;
  reloadSetQuestions: boolean;

  addQuestionSectionIndicator: boolean;

  addConceptLabelIndicator: boolean;
  deleteConceptLabelIndicator: boolean;

  addQuestionIndicator: boolean;
  editQuestionIndicator: boolean;

  progress = 0;
  loadedFileSize = 0;
  totalFileSize = 0;

  showAddQuestionSetForm = false;
  previewQuestionPaper = false;
  showAddQuestionForm = false;
  showConceptLabelInfo = false;
  showQuestionSetInfo = false;

  QUESTION_SECTION_VIEW_TYPE = QUESTION_SECTION_VIEW_TYPE;
  getDateFromUnixTimeStamp = getDateFromUnixTimeStamp;
  getFileSize = getFileSize;
  QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS = QUESTION_SECTION_VIEW_TYPE_FORM_FIELD_OPTIONS;
  AUTOCHECK_TYPE_QUESTION_FORM_FIELD_OPTIONS = AUTOCHECK_TYPE_QUESTION_FORM_FIELD_OPTIONS;
  AUTOCHECK_TYPE_QUESTIONS = AUTOCHECK_TYPE_QUESTIONS;

  readonly separatorKeysCodes: number[] = [ENTER, COMMA];

  testDetails: TestMinDetailsResponseForTypedTestQuestionCreation;
  selectedSet: TestQuestionSetInterface;
  setQuestions: TypedQuestionsSectionInterface[];
  filename: string;

  selectedSectionIdx: number;
  selectedSectionData: TypedQuestionsSectionInterface;

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
      set_name: [null, [Validators.required, characterLengthLessThanEqualTo(20)]]
    });

    this.addQuestionSectionForm = this.formBuilder.group({
      name: [null],
      section_mandatory: [null, [Validators.required]],
      view: [null, [Validators.required]],
      answer_all_questions: [null, [Validators.required]],
      no_of_question_to_attempt: [null, [Validators.required]]
    }, { validator: [addQuestionFormValidator, ] });

    this.editQuestionSectionForm = this.formBuilder.group({
      name: [null],
      section_mandatory: [null, [Validators.required]],
      view: [null, [Validators.required]],
      answer_all_questions: [null, [Validators.required]],
      no_of_question_to_attempt: [null, [Validators.required]]
    }, { validator: [addQuestionFormValidator, ] });

    this.addQuestionForm = this.formBuilder.group({
      question: [null, [Validators.required]],
      marks: [null, [Validators.required, postiveIntegerValidator]],
      concept_label: [null],
      type: [null, [Validators.required]],
      has_picture: [null, [Validators.required]]
    });

    this.editQuestionForm = this.formBuilder.group({
      text: [null, [characterLengthLessThanEqualTo(2000)]],
      marks: [null, [Validators.required, postiveIntegerValidator]],
      concept_label: [null]
    });

    this.editQuestionSetForm = this.formBuilder.group({
      set_name: [null, [Validators.required, characterLengthLessThanEqualTo(20)]]
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
      (result: TestMinDetailsResponseForTypedTestQuestionCreation) => {
        this.loadingIndicator = false;
        this.testDetails = result;
        if (result.test_sets.length > 0) {
          this.selectedSet = result.test_sets[0];
        }
        this.setQuestions = result.first_set_questions;
        if (this.setQuestions && this.setQuestions.length > 0) {
          this.selectedSectionIdx = 0;
          this.selectedSectionData = this.setQuestions[0];
        }
        console.log(result);
        console.log(this.setQuestions);
        console.log(this.selectedSet);
        console.log(this.selectedSectionData);
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
          this.selectedSectionData = null;
          this.setQuestions = [];
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
        this.deleteQuestionSet(this.selectedSet.id);
      }
    });
  }

  deleteQuestionSet(selectedSetId: number) {
    this.selectedSet.delete = true;
    this.instituteApiService.deleteQuestionSet(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString()
    ).subscribe(
      () => {
        const index = +this.findIndexInArray(this.testDetails.test_sets, selectedSetId);
        if (this.selectedSet.id === selectedSetId) {
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
            this.uiService.showSnackBar('Error! Unable to delete question set.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete question set.', 3000);
        }
      }
    );
  }

  getQuestionSetQuestions(questionSet: TestQuestionSetInterface, retry = false) {
    this.showAddQuestionSetForm = false;
    this.selectedSet.showAddSectionForm = false;

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
        (result: TypedQuestionsSectionInterface[]) => {
          this.loadingSetQuestionsIndicator = false;
          this.setQuestions = result;
          console.log(result);
          if (this.setQuestions.length > 0) {
            this.selectSectionIdx(0);
          }
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

  showAddQuestionSectionForm() {
    this.resetAddQuestionSectionForm();
    this.addQuestionSectionForm.enable();
    this.addQuestionSectionIndicator = false;
    this.selectedSet.showAddSectionForm = true;
  }

  hideAddQuestionSectionForm() {
    this.selectedSet.showAddSectionForm = false;
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
    const data = {...this.addQuestionSectionForm.value };
    data.no_of_question_to_attempt = +data.no_of_question_to_attempt;
    if (data.answer_all_questions) {
      data.no_of_question_to_attempt = null;
    }
    if (data.view === QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION) {
      data.name = '';
      data.no_of_question_to_attempt = 1;
      data.answer_all_questions = true;
    }
    console.log(data);
    this.addQuestionSectionIndicator = true;
    this.addQuestionSectionForm.disable();
    this.instituteApiService.addTestQuestionSection(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString(),
      data
    ).subscribe(
      (result: TypedQuestionsSectionInterface) => {
        this.hideAddQuestionSectionForm();
        this.addQuestionSectionIndicator = false;
        console.log(result);
        if (!this.setQuestions) {
          this.setQuestions = [];
        }
        this.setQuestions.push(result);
        for (const idx in this.setQuestions) {
          if (this.setQuestions[idx].section_id === result.section_id) {
            this.selectSectionIdx(+idx);
          }
        }
        console.log(this.setQuestions);
        console.log(this.selectedSectionData);
        this.uiService.showSnackBar('Question group added successfully!', 2000);
      },
      errors => {
        this.addQuestionSectionIndicator = false;
        this.addQuestionSectionForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 2000);
          } else {
            this.uiService.showSnackBar('Error! Unable to add question group at this moment.', 2000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to add question group at this moment.', 2000);
        }
      }
    );
  }

  addConceptLabelEvent(event: MatChipInputEvent): void {
    const input = event.input;
    let value = event.value;

    if (value) {
      value = value.trim();
    }

    if  (value.length > 30) {
      this.uiService.showSnackBar('Concept labels should not exceed 30 characters.', 3000);
    } else {

      if (!value) {
        input.value = '';
      } else {
        this.addConceptLabelIndicator = true;
        this.instituteApiService.addTestConceptLabel(
          this.currentInstituteSlug,
          this.currentSubjectSlug,
          this.currentTestSlug,
          { name: value}
        ).subscribe(
          (result: TestConceptLabelInterface) => {
            this.addConceptLabelIndicator = false;

            // Add question label
            this.testDetails.labels.push(result);

            // Reset the input value
            if (input) {
              input.value = '';
            }

            this.uiService.showSnackBar('Concept label added successfully!', 2000);
          },
          errors => {
            this.addConceptLabelIndicator = false;
            if (errors.error) {
              if (errors.error.error) {
                this.uiService.showSnackBar(errors.error.error, 2000);
              } else {
                this.uiService.showSnackBar('Error! Unable to add concept label at this moment.', 2000);
              }
            } else {
              this.uiService.showSnackBar('Error! Unable to add concept label at this moment.', 2000);
            }
          }
        );
      }
    }
  }

  removeConceptLabelConfirm(label) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        // tslint:disable-next-line: max-line-length
        title: 'Deleting concept label will remove this label from all other questions of ALL THE QUESTION SETS of this test. Do you want to delete label "' + label.name + '"?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.removeConceptLabel(label);
      }
    });
  }

  removeConceptLabel(label: TestConceptLabelInterface) {
    this.deleteConceptLabelIndicator = true;
    this.instituteApiService.deleteConceptLabel(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      label.id.toString()
    ).subscribe(
      () => {
        this.deleteConceptLabelIndicator = false;
        const index = this.testDetails.labels.indexOf(label);

        if (index >= 0) {
          this.testDetails.labels.splice(index, 1);
        }

        // Remove concept label from the questions of current selected question set
        this.setQuestions.map(
          s => {
            s.questions.map(q => {
              if (q.concept_label_id === label.id) {
                delete q.concept_label_id;
              }
            });
          }
        );

        this.uiService.showSnackBar('Concept label deleted successfully', 3000);
      },
      errors => {
        this.deleteConceptLabelIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete concept label at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete concept label at the moment.', 3000);
        }
      }
    );
  }

  toggleAddQuestionInSection() {
    this.resetAddQuestionForm();
    this.addQuestionIndicator = false;
    this.showAddQuestionForm = !this.showAddQuestionForm;
  }

  resetAddQuestionForm() {
    this.addQuestionForm.reset();
    this.addQuestionForm.enable();
    this.addQuestionForm.patchValue({
      has_picture: false
    });
  }

  addQuestion(selectedSectionData: TypedQuestionsSectionInterface) {
      this.addQuestionIndicator = true;
      this.addQuestionForm.disable();

      this.instituteApiService.addTypedTestQuestion(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.currentTestSlug,
        this.selectedSet.id.toString(),
        selectedSectionData.section_id.toString(),
        this.addQuestionForm.value
      ).subscribe(
        (result: SubjectTypedTestQuestions) => {
            this.addQuestionIndicator = false;
            this.toggleAddQuestionInSection();

            if (selectedSectionData.section_id === this.selectedSectionData.section_id) {
              this.selectedSectionData.questions.push(result);
            } else {
              const idx = this.findIndexInArray(this.setQuestions, selectedSectionData.section_id, 'section_id');
              if (idx >= 0) {
                this.setQuestions[idx].questions.push(result);
              }
            }
            this.uiService.showSnackBar('Question added successfully!', 2000);
            console.log(this.setQuestions);
        },
        errors => {
          this.addQuestionIndicator = false;
          this.addQuestionForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(errors.error.error, 3000);
            } else {
              this.uiService.showSnackBar('Error! Unable to add question at the moment.', 3000);
            }
          } else {
            this.uiService.showSnackBar('Error! Unable to add question at the moment.', 3000);
          }
        }
      );
  }

  confirmDeleteQuestion(selectedSectionData: TypedQuestionsSectionInterface, question: SubjectTypedTestQuestions) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Delete question?', trueStringDisplay: 'Yes', falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteQuestion(selectedSectionData, question);
      }
    });
  }

  deleteQuestion(selectedSectionData: TypedQuestionsSectionInterface, question: SubjectTypedTestQuestions) {
    const questionIdx = this.findIndexInArray(selectedSectionData.questions, question.question_id, 'question_id');
    if (questionIdx >= 0) {
      this.selectedSectionData.questions[questionIdx].delete = true;
    }
    this.instituteApiService.deleteImageTestQuestion(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString(),
      question.question_id.toString()
    ).subscribe(
      () => {
        if (selectedSectionData.section_id === this.selectedSectionData.section_id) {
          this.selectedSectionData.questions.splice(+questionIdx, 1);
        } else {
          const sectionIdx = this.findIndexInArray(this.setQuestions, selectedSectionData.section_id, 'section_id');
          if (sectionIdx >= 0) {
            this.setQuestions[sectionIdx].questions.splice(+questionIdx, 1);
          }
        }
        this.uiService.showSnackBar('Question deleted successfully!', 2000);
      },
      errors => {
        this.selectedSectionData.questions[questionIdx].delete = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 2000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete question at the moment.', 2000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete question at the moment.', 2000);
        }
      }
    );
  }

  showEditQuestionFormInSection(question: SubjectTypedTestQuestions) {
    this.resetEditQuestionForm(question);
    this.setQuestions.map(s => {
      s.questions.map(
        q => {
          if (q.question_id !== question.question_id) {
            q.edit = false;
          } else {
            q.edit = true;
          }
        }
      );
    });
  }

  closeEditQuestionFormInSection(question: SubjectTypedTestQuestions) {
    this.selectedSectionData.questions.map(q => {
      if (q.question_id === question.question_id) {
        q.edit = false;
      }
    });
  }

  resetEditQuestionForm(question) {
    this.editQuestionForm.reset();
    this.editQuestionForm.enable();
    this.editQuestionForm.patchValue({
      text: question.text,
      marks: question.marks,
      concept_label: question.concept_label_id
    });
  }

  editQuestion(question: SubjectTypedTestQuestions) {
    this.editQuestionIndicator = true;
    this.editQuestionForm.disable();
    const data = {...this.editQuestionForm.value};
    if (!data.text) {
      delete data.text;
    }
    if (!data.concept_label) {
      delete data.concept_label;
    }
    this.instituteApiService.editImageTestQuestion(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      this.selectedSet.id.toString(),
      question.question_id.toString(),
      data
    ).subscribe(
      (result: SubjectTypedTestQuestions) => {
        this.editQuestionIndicator = false;
        this.selectedSectionData.questions.map(q => {
          if (q.question_id === result.question_id) {
            q.marks = result.marks;
            q.concept_label_id = result.concept_label_id;
            q.question = result.question;
          }
        });
        this.closeEditQuestionFormInSection(result);
        this.uiService.showSnackBar('Question edit successful!', 3000);
      },
      errors => {
        this.editQuestionIndicator = false;
        this.editQuestionForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to edit question at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to edit question at the moment.', 3000);
        }
      }
    );
  }

  selectSectionIdx(index: number) {
    this.selectedSectionIdx = index;
    this.showAddQuestionForm = false;
    this.selectedSectionData = this.setQuestions[index];
  }

  editQuestionSetName() {
    this.resetQuestionSetEditForm();
    this.selectedSet.edit = true;
    this.selectedSet.editingIndicator = false;
    this.editQuestionSetForm.enable();
  }

  resetQuestionSetEditForm() {
    this.editQuestionSetForm.reset();
    this.editQuestionSetForm.patchValue({
      set_name: this.selectedSet.set_name
    });
    this.editQuestionSetForm.enable();
  }

  closeQuestionSetEditForm() {
    this.selectedSet.edit = false;
  }

  editQuestionSet(selectedSetId: number) {
    this.selectedSet.editingIndicator = true;
    this.editQuestionSetForm.disable();
    this.instituteApiService.editQuestionSet(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      selectedSetId.toString(),
      this.editQuestionSetForm.value
    ).subscribe(
      (result: {id: number; set_name: string}) => {
        this.selectedSet.editingIndicator = false;
        this.selectedSet.edit = false;
        if (this.selectedSet.id === result.id) {
          this.selectedSet.set_name = result.set_name;
        } else {
          this.testDetails.test_sets.map(s => {
            if (s.id === result.id) {
              s.set_name = result.set_name;
            }
          });
        }
        this.uiService.showSnackBar(
          'Updated question set successfully!',
          2000
        );
      },
      errors => {
        this.selectedSet.editingIndicator = false;
        this.editQuestionSetForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to edit question set.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to edit question set.', 3000);
        }
      }
    );
  }

  showEditQuestionSectionForm() {
    this.resetEditQuestionSectionForm();
    this.selectedSectionData.edit = true;
    this.selectedSectionData.editingIndicator = false;
  }

  resetEditQuestionSectionForm() {
    this.editQuestionSectionForm.reset();
    this.editQuestionSectionForm.enable();
    let noOfQuestionToAttempt = this.selectedSectionData.no_of_question_to_attempt;
    if (!noOfQuestionToAttempt) {
      noOfQuestionToAttempt = 0;
    }
    this.editQuestionSectionForm.patchValue({
      name: this.selectedSectionData.name,
      view: this.selectedSectionData.view,
      section_mandatory: this.selectedSectionData.section_mandatory,
      no_of_question_to_attempt: noOfQuestionToAttempt,
      answer_all_questions: this.selectedSectionData.answer_all_questions
    });
  }

  closeEditQuestionSectionForm() {
    this.selectedSectionData.edit = false;
  }

  editQuestionSection(selectedSectionId: number) {
    const data = {...this.editQuestionSectionForm.value };
    data.no_of_question_to_attempt = +data.no_of_question_to_attempt;
    if (data.answer_all_questions) {
      data.no_of_question_to_attempt = null;
    }
    if (data.view === QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION) {
      data.name = '';
      data.no_of_question_to_attempt = 1;
      data.answer_all_questions = true;
    }
    this.selectedSectionData.editingIndicator = true;
    this.editQuestionSectionForm.disable();
    this.instituteApiService.editTestQuestionSection(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      selectedSectionId.toString(),
      data
    ).subscribe(
      (result: TypedQuestionsSectionInterface) => {
        this.closeEditQuestionSectionForm();
        this.selectedSectionData.editingIndicator = false;
        if (this.selectedSectionData.section_id === result.section_id) {
          this.selectedSectionData.name = result.name;
          this.selectedSectionData.answer_all_questions = result.answer_all_questions;
          this.selectedSectionData.no_of_question_to_attempt = result.no_of_question_to_attempt;
          this.selectedSectionData.view = result.view;
          this.selectedSectionData.section_mandatory = result.section_mandatory;
        } else {
          this.setQuestions.map(s => {
            if (s.section_id === result.section_id) {
              this.selectedSectionData.name = result.name;
              this.selectedSectionData.answer_all_questions = result.answer_all_questions;
              this.selectedSectionData.no_of_question_to_attempt = result.no_of_question_to_attempt;
              this.selectedSectionData.view = result.view;
              this.selectedSectionData.section_mandatory = result.section_mandatory;
            }
          });
        }
        this.uiService.showSnackBar('Question group edited successfully!', 2000);
      },
      errors => {
        this.selectedSectionData.editingIndicator = false;
        this.editQuestionSectionForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 2000);
          } else {
            this.uiService.showSnackBar('Error! Unable to edit question group at this moment.', 2000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to edit question group at this moment.', 2000);
        }
      }
    );
  }

  confirmRemoveConceptLabelFromQuestion(question: SubjectTypedTestQuestions) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Are you sure you want to remove this concept label from question?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.removeConceptLabelFromQuestion(question);
      }
    });
  }

  removeConceptLabelFromQuestion(question: SubjectTypedTestQuestions) {
    this.selectedSectionData.questions.map(q => {
      if (q.question_id === question.question_id) {
        q.removingLabelIndicator = true;
      }
    });
    this.instituteApiService.removeQuestionConceptLabel(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      question.question_id.toString()
    ).subscribe(
      () => {
        this.setQuestions.map(s => {
          s.questions.map(q => {
            if (q.question_id === question.question_id) {
              q.removingLabelIndicator = false;
              delete q.concept_label_id;
            }
          });
        });
        this.uiService.showSnackBar('Concept label removed.', 2000);
      },
      errors => {
        this.setQuestions.map(s => {
          s.questions.map(q => {
            if (q.question_id === question.question_id) {
              q.removingLabelIndicator = false;
              delete q.concept_label_id;
            }
          });
        });
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to remove concept label at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to remove concept label at the moment.', 3000);
        }
      }
    );
  }

  confirmDeleteQuestionSection(questionSectionId: number) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Are you sure you want to remove this question group?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteQuestionSection(questionSectionId);
      }
    });
  }

  deleteQuestionSection(questionSectionId: number) {
    this.selectedSectionData.deletingIndicator = true;
    this.instituteApiService.deleteQuestionSection(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.currentTestSlug,
      questionSectionId.toString()
    ).subscribe(
      () => {
        let index = -1;
        for (const idx in this.setQuestions) {
          if (this.setQuestions[idx].section_id === questionSectionId) {
            index = +idx;
          }
        }
        if (index > -1) {
          if (this.setQuestions.length > index + 1) {
            this.selectSectionIdx(index + 1);
          } else if (this.setQuestions.length > 1) {
            this.selectSectionIdx(index - 1);
          }
          this.setQuestions.splice(index, 1);
        }
        this.uiService.showSnackBar('Question section deleted.', 2000);
      },
      errors => {
        this.setQuestions.map(s => {
          if (s.section_id === questionSectionId) {
            s.deletingIndicator = false;
          }
        });
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete question group at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete question group at the moment.', 3000);
        }
      }
    );
  }

  trueFalseAnswerChanged(questionId: number, answer: boolean) {
    console.log(answer);
    this.instituteApiService.addUpdateTrueFalseCorrectAnswer(
      this.currentSubjectSlug,
      questionId.toString(),
      {correct_answer: answer}
    ).subscribe(
      (result: {correct_answer: boolean}) => {
        this.setQuestions.map(s => {
          s.questions.map(q => {
            if (q.question_id === questionId) {
              q.correct_answer = result.correct_answer;
            }
          });
        });
        console.log(result);
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Updating True / False correct answer failure.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Updating True / False correct answer failure.', 3000);
        }
      }
    );
  }

  addUpdateCorrectNumericAnswerToQuestion(question: SubjectTypedTestQuestions, correctAnswer: number) {
    question.showAddAnswerIndicator = true;
    this.instituteApiService.addUpdateNumericCorrectAnswer(
      this.currentSubjectSlug,
      question.question_id.toString(),
      {correct_answer: correctAnswer}
    ).subscribe(
      (result: {correct_answer: number}) => {
        question.correct_answer = result.correct_answer;
        question.showAddAnswerIndicator = false;
        question.showAddAnswerForm = false;
        this.uiService.showSnackBar('Numeric answer added!', 2000);
      },
      errors => {
        question.showAddAnswerIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to add numeric answer at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to add numeric answer at the moment.', 3000);
        }
      }
    );
  }

  editMcqOption(question: SubjectTypedTestQuestions, seletedOption: QuestionAnswerOptions) {
    question.selectedOptionToEdit = seletedOption;
    question.showAddAnswerForm = true;
  }

  confirmDeleteMcqOption(question: SubjectTypedTestQuestions, selectedOption: QuestionAnswerOptions) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Do you want to delete option: "' + selectedOption.option + '"?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteMcqOption(question, selectedOption);
      }
    });
  }

  deleteMcqOption(question: SubjectTypedTestQuestions, selectedOption: QuestionAnswerOptions) {
    selectedOption.deletingIndicator = true;
    this.instituteApiService.deleteMcqOption(
      this.currentSubjectSlug,
      question.question_id.toString(),
      selectedOption.option_id.toString()
    ).subscribe(
      () => {
        let index = -1;
        for (const idx in question.options) {
          if (question.options[idx].option_id === selectedOption.option_id) {
            index = +idx;
            break;
          }
        }
        if (index > -1) {
          question.options.splice(index, 1);
        }
        if (question.selectedOptionToEdit && question.selectedOptionToEdit.option_id === selectedOption.option_id) {
          question.showAddAnswerForm = false;
          question.showAddAnswerIndicator = false;
          question.selectedOptionToEdit = null;
        }
      },
      errors => {
        selectedOption.deletingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete option at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete option at the moment.', 3000);
        }
      }
    );
  }

  editMultipleChoiceOption(question: SubjectTypedTestQuestions, seletedOption: QuestionAnswerOptions) {
    question.selectedOptionToEdit = seletedOption;
    question.showAddAnswerForm = true;
  }

  confirmDeleteMultipleChoiceOption(question: SubjectTypedTestQuestions, selectedOption: QuestionAnswerOptions) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: 'Do you want to delete option: "' + selectedOption.option + '"?',
        trueStringDisplay: 'Yes',
        falseStringDisplay: 'No'
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteMultipleChoiceOption(question, selectedOption);
      }
    });
  }

  deleteMultipleChoiceOption(question: SubjectTypedTestQuestions, selectedOption: QuestionAnswerOptions) {
    selectedOption.deletingIndicator = true;
    this.instituteApiService.deleteMultipleChoiceOption(
      this.currentSubjectSlug,
      question.question_id.toString(),
      selectedOption.option_id.toString()
    ).subscribe(
      () => {
        let index = -1;
        for (const idx in question.options) {
          if (question.options[idx].option_id === selectedOption.option_id) {
            index = +idx;
            break;
          }
        }
        if (index > -1) {
          question.options.splice(index, 1);
        }
        if (question.selectedOptionToEdit && question.selectedOptionToEdit.option_id === selectedOption.option_id) {
          question.showAddAnswerForm = false;
          question.showAddAnswerIndicator = false;
          question.selectedOptionToEdit = null;
        }
      },
      errors => {
        selectedOption.deletingIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to delete option at the moment.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to delete option at the moment.', 3000);
        }
      }
    );
  }

  getConceptLabelName(conceptLabelId: number) {
    return this.testDetails.labels.map(label => {
      if (label.id === conceptLabelId) {
        return label.name;
      }
    });
  }

  findTotalMarksOfSelectedQuestionSet() {
    if (this.setQuestions) {
      return this.setQuestions.map(s => s.questions.map(q => +q.marks).reduce((a, b) => a + b, 0)).reduce((a, b) => a + b, 0);
    } else {
      return 0;
    }
  }

  findTotalMarksOfSelectedQuestionGroup() {
    if (this.selectedSectionData) {
      return this.selectedSectionData.questions.map(q => +q.marks).reduce((a, b) => a + b, 0);
    } else {
      return 0;
    }
  }

  canAddQuestionInSection() {
    if (this.selectedSectionData.view === QUESTION_SECTION_VIEW_TYPE.SINGLE_QUESTION) {
      if (this.selectedSectionData.questions.length > 0) {
        return false;
      }
    }
    return true;
  }

  findIndexInArray(array, key: number, searchField = 'id') {
    for (const idx in array) {
      if (array[idx][searchField] === key) {
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
