import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { StudyMaterialPreviewDetails } from './../../models/subject.model';
import { Component, OnInit, Input } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-q-and-a',
  templateUrl: './q-and-a.component.html',
  styleUrls: ['./q-and-a.component.css']
})
export class QAndAComponent implements OnInit {

  mq: MediaQueryList;
  @Input() content: StudyMaterialPreviewDetails;
  text = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur distinctio velit ea facilis? Vitae officia saepe veniam. Fuga consectetur magnam impedit, dicta voluptatibus dolorum laudantium voluptas! Neque culpa saepe doloribus?';
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

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.answerForm = this.formBuilder.group({
      answer: [null, [Validators.required]]
    });
    this.askQuestionForm = this.formBuilder.group({
      question: [null, [Validators.required]],
      description: [null, ]
    });
  }

  loadQuestions() {

  }

  loadAnswers() {

  }

  answerClicked() {
    this.answerForm.patchValue({
      answer: this.answerForm.value.answer.trim()
    });
    if (!this.answerForm.invalid) {
      console.log(this.answerForm.value);
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
      console.log(this.askQuestionForm.value);
    }
  }

  questionClicked() {
    this.showSpecificQuestionView = true;
  }

  showAllQuestionView() {
    this.answerForm.reset();
    this.showSpecificQuestionView = false;
    this.loadingAnswersIndicator = false;
    this.reloadLoadAnswerIndicator = false;
    this.loadAnswerError = null;
  }

  getBackgroundColor() {
    // const idx = Math.floor(Math.random() * this.colors.length);
    // return this.colors[idx];
    return this.colors[0];
  }

  formatText(text: string) {
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
  }

  closeSubmitAnswerErrorText() {
    this.submitAnswerError = null;
  }

  closeSubmitQuestionError() {
    this.submitQuestionError = null;
  }

}
