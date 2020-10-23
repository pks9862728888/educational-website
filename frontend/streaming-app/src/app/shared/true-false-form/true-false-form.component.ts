import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-true-false-form',
  templateUrl: './true-false-form.component.html',
  styleUrls: ['./true-false-form.component.css']
})
export class TrueFalseFormComponent implements OnInit {

  @Input() id: string;
  @Input() correctAnswer: boolean;
  @Output() correctAnswerChoice = new EventEmitter<boolean>();
  trueFalseForm: FormGroup;

  trueId: string;
  falseId: string;

  constructor(
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.trueFalseForm = this.formBuilder.group({
      correct_answer: [null, [Validators.required]]
    });
    this.trueFalseForm.patchValue({
      correct_answer: this.correctAnswer
    });

    this.trueId = 'true' + this.id.replace(' ', '').substring(0, Math.max(10, this.id.length));
    this.falseId = 'false' + this.id.replace(' ', '').substring(0, Math.max(10, this.id.length));
  }

  optionChanged() {
    this.correctAnswerChoice.emit(this.trueFalseForm.value.correct_answer);
  }
}
