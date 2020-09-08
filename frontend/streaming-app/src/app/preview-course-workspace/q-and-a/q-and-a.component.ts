import { Subscription } from 'rxjs';
import { currentInstituteSlug, currentSubjectSlug, userId, is_teacher } from './../../../constants';
import { UiService } from './../../services/ui.service';
import { InstituteApiService } from './../../services/institute-api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { StudyMaterialPreviewDetails, CourseContentQuestion, CourseContentAnswers } from './../../models/subject.model';
import { Component, OnInit, Input } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';
import { getTimeElapsed } from 'src/app/shared/utilityFunctions';

@Component({
  selector: 'app-q-and-a',
  templateUrl: './q-and-a.component.html',
  styleUrls: ['./q-and-a.component.css']
})
export class QAndAComponent implements OnInit {

  mq: MediaQueryList;
  currentInstituteSlug: string;
  currentSubjectSlug: string;
  getTimeElapsed = getTimeElapsed;
  hideAnswerAnonymouslyOption: boolean;
  @Input() content: StudyMaterialPreviewDetails;
  colors = [
    'rgba(191, 207, 46, 0.5)',
    'rgba(139, 195, 74, 0.5)',
    'rgba(0, 150, 136, 0.5)',
    'rgba(156, 39, 176, 0.5)',
    'rgba(102, 187, 106, 0.5)',
  ];
  loadingQuestionsIndicator: boolean;
  reloadQuestionsIndicator: boolean;
  loadingQuestionsError: string;
  showSpecificQuestionView = false;
  answerForm: FormGroup;
  submitAnswerError: string;
  submitAnswerIndicator: boolean;
  showAskQuestionForm = false;
  askQuestionForm: FormGroup;
  submitQuestionIndicator: boolean;
  submitQuestionError: string;
  loadingAnswersIndicator: boolean;
  reloadLoadAnswerIndicator: boolean;
  loadAnswerError: string;
  deleteAnswerSubscription: Subscription;

  questions: CourseContentQuestion[] = [];
  answers: CourseContentAnswers[] = [];
  selectedQuestion: CourseContentQuestion;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.currentInstituteSlug = sessionStorage.getItem(currentInstituteSlug);
    this.currentSubjectSlug = sessionStorage.getItem(currentSubjectSlug);
    if (sessionStorage.getItem(is_teacher) === 'true') {
      this.hideAnswerAnonymouslyOption = true;
    } else {
      this.hideAnswerAnonymouslyOption = false;
    }
  }

  ngOnInit(): void {
    this.answerForm = this.formBuilder.group({
      answer: [null, [Validators.required]],
      anonymous: [false, ]
    });
    this.askQuestionForm = this.formBuilder.group({
      question: [null, [Validators.required]],
      description: [null, ],
      anonymous: [false, ]
    });
    this.loadQuestions();
  }

  loadQuestions() {
    this.loadingQuestionsIndicator = true;
    this.loadingQuestionsError = null;
    this.reloadQuestionsIndicator = false;
    this.instituteApiService.loadAllInstituteSubjectCourseContentQuestions(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.content.id.toString()
    ).subscribe(
      (result: CourseContentQuestion[]) => {
        this.loadingQuestionsIndicator = false;
        this.questions = result;
        console.log(this.questions);
      },
      errors => {
        this.loadingQuestionsIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadingQuestionsError = errors.error.error;
          } else {
            this.reloadQuestionsIndicator = true;
          }
        } else {
          this.reloadQuestionsIndicator = true;
        }
      }
    )
  }

  questionClicked(question: CourseContentQuestion) {
    this.selectedQuestion = question;
    this.showSpecificQuestionView = true;
    this.loadAnswers();
  }

  loadAnswers() {
    this.loadingAnswersIndicator = true;
    this.reloadLoadAnswerIndicator = false;
    this.loadAnswerError = null;
    this.instituteApiService.loadAnswerOfInstituteCourseQuestion(
      this.currentInstituteSlug,
      this.currentSubjectSlug,
      this.selectedQuestion.id.toString()
    ).subscribe(
      (result: CourseContentAnswers[]) => {
        this.loadingAnswersIndicator = false;
        this.answers = result;
        console.log(this.answers);
      },
      errors => {
        this.loadingAnswersIndicator = false;
        if (errors.error) {
          if (errors.error.error) {
            this.loadAnswerError = errors.error.error;
          } else {
            this.reloadLoadAnswerIndicator = true;
          }
        } else {
          this.reloadLoadAnswerIndicator = true;
        }
      }
    )
  }

  answerClicked() {
    this.answerForm.patchValue({
      answer: this.answerForm.value.answer.trim()
    });
    if (!this.answerForm.invalid) {
      let data = this.answerForm.value;
      data['rgb_color'] = this.getBackgroundColor();
      if (!data['anonymous']) {
        data['anonymous'] = false;
      }
      this.answerForm.disable();
      this.submitAnswerIndicator = true;
      this.submitQuestionError = null;
      console.log(data);
      this.instituteApiService.answerQuestionOfInstituteCourseContent(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.selectedQuestion.id.toString(),
        data
      ).subscribe(
        (result: CourseContentAnswers) => {
          this.submitAnswerIndicator = false;
          this.answerForm.enable();
          this.answerForm.reset();
          this.answerForm.patchValue({
            anonymous: false
          });
          this.answers.unshift(result);
          const getQuestionId = this.getIndex(this.questions, this.selectedQuestion.id);
          this.questions[getQuestionId]['answer_count'] += 1;
          this.uiService.showSnackBar(
            'Answer added successfully!',
            2000
          );
        },
        errors => {
          this.submitAnswerIndicator = false;
          this.answerForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.submitAnswerError = errors.error.error;
            } else {
              this.submitQuestionError = 'Unknown error occured :(';
            }
          } else {
            this.submitQuestionError = 'Unknown error occured :(';
          }
        }
      )
    }
  }

  toggleAskQuestion() {
    if (this.showAskQuestionForm) {
      this.askQuestionForm.reset();
    }
    this.showAskQuestionForm = !this.showAskQuestionForm;
  }

  askQuestion() {
    this.askQuestionForm.patchValue({
      question: this.askQuestionForm.value.question.trim()
    });
    if (!this.askQuestionForm.invalid) {
      let data = this.askQuestionForm.value;
      data['rgb_color'] = this.getBackgroundColor();
      if (!data.description) {
        data['description'] = '';
      } else {
        data['description'] = data['description'].trim();
      }
      this.submitQuestionIndicator = true;
      this.submitQuestionError = null;
      this.askQuestionForm.disable();
      this.instituteApiService.askQuestionInCourseContent(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.content.id.toString(),
        data
      ).subscribe(
        (result: CourseContentQuestion) => {
          this.submitQuestionIndicator = false;
          this.questions.unshift(result);
          this.askQuestionForm.reset();
          this.askQuestionForm.enable();
          this.askQuestionForm.patchValue({
            anonymous: false
          });
          this.showAskQuestionForm = false;
          this.uiService.showSnackBar(
            'Question added successfully!',
            2000
          );
          console.log(result);
        },
        errors => {
          this.submitQuestionIndicator = false;
          this.askQuestionForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.submitQuestionError = errors.error.error;
            } else {
              this.uiService.showSnackBar(
                'Error occured while asking question :(',
                2000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error occured while asking question :(',
              2000
            );
          }
        }
      )
    }
  }

  deleteAnswerConfirm(answer: CourseContentAnswers) {
    this.deleteAnswerSubscription = this.uiService.dialogData$.subscribe(
      result => {
        if (result === true) {
         this.deleteAnswer(answer);
        }
        this.deleteAnswerSubscription.unsubscribe();
      }
    )
    this.uiService.openDialog(
      'Confirm delete answer?',
      'No',
      'Yes'
    );
  }

  deleteAnswer(answer: CourseContentAnswers) {
    this.instituteApiService.deleteInstituteCourseContentAnswer(
      this.currentSubjectSlug,
      answer.id.toString()
    ).subscribe(
      () => {
        const answerIndex = this.getIndex(this.answers, answer.id);
        if (answerIndex >= 0) {
          this.answers.splice(+answerIndex, 1);
        }
        this.uiService.showSnackBar(
          'Answer deleted successfully!',
          2500
        );
        const questionIndex = this.getIndex(this.questions, this.selectedQuestion.id);
        if (questionIndex >= 0) {
          this.questions[questionIndex]['answer_count'] -= 1;
        }
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              2500
            );
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to delete answer.',
              2500
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error! Unable to delete answer.',
            2500
          );
        }
      }
    )
  }

  pinUnpinAnswer(answerId: number, pinned: boolean) {
    let data = {};
    if (pinned) {
      data['unpin'] = true;
    } else {
      data['pin'] = true;
    }
    this.instituteApiService.pinUnpinInstituteCourseContentAnswer(
      answerId.toString(),
      data
    ).subscribe(
      (result: {status: string} ) => {
        let statusText = '';
        const answerIndex = this.getIndex(this.answers, answerId);
        if (answerIndex > -1) {
          if (result.status === 'PINNED') {
            this.answers[answerIndex]['pin'] = true;
            statusText = 'Answer Pinned!';
          } else {
            this.answers[answerIndex]['pin'] = false;
            statusText = 'Answer Unpinned!';
          }
          this.uiService.showSnackBar(
            statusText,
            2000
          );
        }
      },
      errors => {
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(
              errors.error.error,
              2500
            );
          } else {
            this.uiService.showSnackBar(
              'Error! Could not pin answer.',
              2000
            );
          }
        } else {
          this.uiService.showSnackBar(
            'Error! Could not pin answer.',
            2500
          );
        }
      }
    );
  }

  showAllQuestionView() {
    this.answerForm.reset();
    this.showSpecificQuestionView = false;
    this.loadingAnswersIndicator = false;
    this.reloadLoadAnswerIndicator = false;
    this.loadAnswerError = null;
    this.selectedQuestion = null;
    this.answers = [];
  }

  getIndex(list, id: number) {
    for (let idx in list) {
      if (list[idx].id === id) {
        return idx;
      }
    }
    return -1;
  }

  upvoteQuestion(id: number, userId: number, upvoted: boolean) {
    if (!this.userIsSelf(userId)) {
      let data = {}
      if (upvoted) {
        data['downvote'] = true;
      } else {
        data['upvote'] = true;
      }
      this.instituteApiService.upvoteDownvoteInstituteCourseContentQuestion(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        id.toString(),
        data
      ).subscribe(
        result => {
          const questionIndex = this.getIndex(this.questions, id);
          let actionString = '';
          if (questionIndex >= 0) {
            if (result && result['upvoted']) {
              this.questions[questionIndex]['upvoted'] = true;
              this.questions[questionIndex]['upvotes'] += 1;
              actionString = 'Question upvoted!';
            } else {
              this.questions[questionIndex]['upvoted'] = false;
              this.questions[questionIndex]['upvotes'] -= 1;
              actionString = 'Removed question upvote!';
            }
            this.uiService.showSnackBar(actionString, 2000);
          }
        },
        errors => {
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                2000
              );
            } else {
              this.uiService.showSnackBar(
                'Request failed.',
                2000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Request failed.',
              2000
            );
          }
        }
      );
    }
  }

  upvoteAnswer(id: number, userId: number, upvoted: boolean) {
    if (!this.userIsSelf(userId)) {
      let data = {}
      if (upvoted) {
        data['downvote'] = true;
      } else {
        data['upvote'] = true;
      }
      this.instituteApiService.upvoteDownvoteInstituteCourseContentAnswer(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        id.toString(),
        data
      ).subscribe(
        result => {
          const answerIndex = this.getIndex(this.answers, id);
          let actionString = '';
          if (answerIndex >= 0) {
            if (result && result['upvoted']) {
              this.answers[answerIndex]['upvoted'] = true;
              this.answers[answerIndex]['upvotes'] += 1;
              actionString = 'Answer upvoted!';
            } else {
              this.answers[answerIndex]['upvoted'] = false;
              this.answers[answerIndex]['upvotes'] -= 1;
              actionString = 'Removed answer upvote!';
            }
            this.uiService.showSnackBar(actionString, 2000);
          }
        },
        errors => {
          if (errors.error) {
            if (errors.error.error) {
              this.uiService.showSnackBar(
                errors.error.error,
                2000
              );
            } else {
              this.uiService.showSnackBar(
                'Request failed.',
                2000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Request failed.',
              2000
            );
          }
        }
      )
    }
  }

  getBackgroundColor() {
    const idx = Math.floor(Math.random() * this.colors.length);
    return this.colors[idx];
  }

  formatText(text: string) {
    if (text) {
      const lenText = text.length;
      let offset = 0;
      if (this.mq.matches) {
        offset = Math.max(0, lenText - 38);
      } else {
        offset = Math.max(0, lenText - 146);
      }
      if (offset === 0) {
        return text;
      } else {
        return text.substr(0, lenText - offset) + '...';
      }
    } else {
      return '';
    }
  }

  questionExists() {
    if (this.questions.length > 0) {
      return true;
    } else {
      return false;
    }
  }

  getNameInitials(name: string) {
    const name_array = name.split(' ');
    return name_array[0].charAt(0) + name_array[name_array.length - 1].charAt(0);
  }

  getQuestionCount() {
    return this.questions.length;
  }

  getAnswerCount() {
    return this.answers.length;
  }

  userIsSelf(userId_: number) {
    if (userId_ && userId_.toString() === sessionStorage.getItem(userId)) {
      return true;
    } else {
      return false;
    }
  }

  userIsQuestionAsker() {
    if (this.selectedQuestion.user_id && this.selectedQuestion.user_id.toString() === sessionStorage.getItem(userId)) {
      return true;
    } else {
      console.log(false);
      return false;
    }
  }

  closeSubmitAnswerErrorText() {
    this.submitAnswerError = null;
  }

  closeSubmitQuestionError() {
    this.submitQuestionError = null;
  }
}
