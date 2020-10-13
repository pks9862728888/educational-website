import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TestMinDetailsResponseForQuestionCreation } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';

@Component({
  selector: 'app-create-file-question',
  templateUrl: './create-file-question.component.html',
  styleUrls: ['./create-file-question.component.css']
})
export class CreateFileQuestionComponent implements OnInit {

  currentSubjectSlug: string;
  currentTestSlug: string;
  questionSetForm: FormGroup;

  loadingIndicator: boolean;
  loadingError: string;
  reloadIndicator: boolean;
  submitIndicatorAddQuestionSet: boolean;

  showAddQuestionSetForm = false;

  testDetails: TestMinDetailsResponseForQuestionCreation;

  constructor(
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) {
    this.currentSubjectSlug = window.location.pathname.split('/')[2];
    this.currentTestSlug = window.location.pathname.split('/')[3];
  }

  ngOnInit(): void {
    this.getTestDetails();
    this.questionSetForm = this.formBuilder.group({
      set_name: [null, Validators.required]
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
  }

}
