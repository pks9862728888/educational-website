import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { isNumberValidator } from 'src/app/custom.validator';

@Component({
  selector: 'app-numeric-question-add-correct-answer',
  templateUrl: './numeric-question-add-correct-answer.component.html',
  styleUrls: ['./numeric-question-add-correct-answer.component.css']
})
export class NumericQuestionAddCorrectAnswerComponent implements OnInit {

  @Input() correctAnswer: number;
  @Input() submittingIndicator: boolean;
  @Output() correctAnswerValue = new EventEmitter<number>();
  addCorrectAnswerForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder
  ) { }

  ngOnInit(): void {
    this.addCorrectAnswerForm = this.formBuilder.group({
      correct_answer: [null, [Validators.required, isNumberValidator]]
    });
    this.addCorrectAnswerForm.patchValue({
      correct_answer: this.correctAnswer
    });
  }

  addCorrectAnswer() {
    this.correctAnswerValue.emit(this.addCorrectAnswerForm.value.correct_answer);
  }
}
