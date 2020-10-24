import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { characterLengthLessThanEqualTo, fillInTheBlankFormValidator } from 'src/app/custom.validator';
import { FillInTheBlankAnswer, SubjectTypedTestQuestions } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-fill-in-the-blank-form',
  templateUrl: './fill-in-the-blank-form.component.html',
  styleUrls: ['./fill-in-the-blank-form.component.css']
})
export class FillInTheBlankFormComponent implements OnInit {

  @Input() currentSubjectSlug: string;
  @Input() question: SubjectTypedTestQuestions;

  fillInTheBlankForm: FormGroup;
  submitIndicator: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private institueApiService: InstituteApiService,
    private uiService: UiService
  ) { }

  ngOnInit(): void {
    this.fillInTheBlankForm = this.formBuilder.group({
      correct_answer: [null, [characterLengthLessThanEqualTo(300)]],
      manual_checking: [null, [Validators.required]],
      enable_strict_checking: [null, [Validators.required]],
      ignore_grammar: [null, [Validators.required]],
      ignore_special_characters: [null, Validators.required]
    }, { validator: [fillInTheBlankFormValidator, ] });
    this.resetFillInTheBlankForm();
  }

  resetFillInTheBlankForm() {
    this.fillInTheBlankForm.reset();
    this.fillInTheBlankForm.enable();
    if (this.question.fill_in_the_blank_answer) {
      this.fillInTheBlankForm.patchValue({
        correct_answer: this.question.fill_in_the_blank_answer.correct_answer,
        manual_checking: this.question.fill_in_the_blank_answer.manual_checking,
        enable_strict_checking: this.question.fill_in_the_blank_answer.enable_strict_checking,
        ignore_grammar: this.question.fill_in_the_blank_answer.ignore_grammar,
        ignore_special_characters: this.question.fill_in_the_blank_answer.ignore_special_characters
      });
    } else {
      this.fillInTheBlankForm.patchValue({
        correct_answer: '',
        manual_checking: true,
        enable_strict_checking: true,
        ignore_grammar: false,
        ignore_special_characters: false
      });
    }
  }

  answerStrictlyChanged() {
    if (this.fillInTheBlankForm.value.enable_strict_checking) {
      this.fillInTheBlankForm.patchValue({
        ignore_grammar: false,
        ignore_special_characters: false
      });
    }
  }

  submitFillInTheBlankAnswer() {
    this.submitIndicator = true;
    this.fillInTheBlankForm.disable();
    this.institueApiService.addUpdateFillInTheBlankAnswerCheck(
      this.currentSubjectSlug,
      this.question.question_id.toString(),
      this.fillInTheBlankForm.value
    ).subscribe(
      (result: FillInTheBlankAnswer) => {
        this.submitIndicator = false;
        this.question.fill_in_the_blank_answer = result;
        this.resetFillInTheBlankForm();
        this.question.showAddAnswerForm = false;
        this.uiService.showSnackBar('Fill in the blank checking rule updated!', 2000);
      },
      errors => {
        this.submitIndicator = false;
        this.fillInTheBlankForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unable to update fill in the blank checking rule at the moment!', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unable to update fill in the blank checking rule at the moment!', 3000);
        }
      }
    );
  }

}
