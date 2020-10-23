import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { characterLengthLessThanEqualTo } from 'src/app/custom.validator';
import { QuestionAnswerOptions, SubjectTypedTestQuestions } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-mcq-form',
  templateUrl: './mcq-form.component.html',
  styleUrls: ['./mcq-form.component.css']
})
export class McqFormComponent implements OnInit {

  @Input() currentSubjectSlug: string;
  @Input() question: SubjectTypedTestQuestions;

  addOptionForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) { }

  ngOnInit(): void {
    this.addOptionForm = this.formBuilder.group({
      option: [null, [Validators.required, characterLengthLessThanEqualTo(300)]],
      correct_answer: [null, [Validators.required]]
    });

    if (this.question.selectedMcqOptionToEdit) {
      this.addOptionForm.patchValue({
        option: this.question.selectedMcqOptionToEdit.option,
        correct_answer: this.question.selectedMcqOptionToEdit.correct_answer
      });
    } else {
      this.addOptionForm.patchValue({
        correct_answer: false
      });
    }
  }

  submit() {
    this.question.showAddAnswerIndicator = true;
    this.addOptionForm.disable();
    const data = this.addOptionForm.value;
    data.option = data.option.trim();

    if (this.question.selectedMcqOptionToEdit) {
      data.option_id = this.question.selectedMcqOptionToEdit.option_id;
    }

    this.instituteApiService.addUpdateMcqOption(
      this.currentSubjectSlug,
      this.question.question_id.toString(),
      data
    ).subscribe(
      (result: QuestionAnswerOptions) => {
        if (!this.question.selectedMcqOptionToEdit) {
          this.question.options.push(result);
          this.uiService.showSnackBar('Option added!', 2000);
        } else {
          this.question.options.map(o => {
            if (o.option_id === result.option_id) {
              o.option = result.option;
              o.correct_answer = result.correct_answer;
            }
          });
          this.uiService.showSnackBar('Option updated!', 2000);
        }
        this.closeMcqForm();
      },
      errors => {
        this.question.showAddAnswerIndicator = false;
        this.addOptionForm.enable();
        if (errors.error) {
          if (errors.error.error) {
            this.uiService.showSnackBar(errors.error.error, 3000);
          } else {
            this.uiService.showSnackBar('Error! Unknown error occurred.', 3000);
          }
        } else {
          this.uiService.showSnackBar('Error! Unknown error occurred.', 3000);
        }
      }
    );
  }

  closeMcqForm() {
    this.question.selectedMcqOptionToEdit = null;
    this.question.showAddAnswerForm = false;
    this.question.showAddAnswerIndicator = false;
  }
}
