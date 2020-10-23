import { HttpEventType } from '@angular/common/http';
import { Component, Input, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SubjectTypedTestQuestions } from 'src/app/models/test.model';
import { InstituteApiService } from 'src/app/services/institute-api.service';
import { UiService } from 'src/app/services/ui.service';
import { getFileSize } from '../utilityFunctions';

@Component({
  selector: 'app-add-typed-test-question-image',
  templateUrl: './add-typed-test-question-image.component.html',
  styleUrls: ['./add-typed-test-question-image.component.css']
})
export class AddTypedTestQuestionImageComponent implements OnInit {

  @Input() question: SubjectTypedTestQuestions;
  @Input() currentInstituteSlug: string;
  @Input() currentSubjectSlug: string;
  uploadError: string;
  uploadImageForm: FormGroup;
  uploadIndicator: boolean;
  progress: number;
  totalFileSize: number;
  loadedFileSize: number;

  getFileSize = getFileSize;

  constructor(
    private formBuilder: FormBuilder,
    private instituteApiService: InstituteApiService,
    private uiService: UiService
  ) { }

  ngOnInit(): void {
    this.uploadImageForm = this.formBuilder.group({
      file: [null, [Validators.required]]
    });
  }

  uploadImage() {
    const file: File = (document.getElementById(this.question.question_id.toString()) as HTMLInputElement).files[0];

    if (!file.type.includes('image/jpeg') && !file.type.includes('image/jpg') && !file.type.includes('image/png')) {
      this.uploadError = 'Only .jpeg, .jpg, and .png formats are supported.';
      this.uploadImageForm.patchValue({
        file: null
      });
    } else {
      this.loadedFileSize = 0;
      this.totalFileSize = file.size;
      this.uploadIndicator = true;
      this.uploadImageForm.disable();
      this.uploadError = null;

      this.instituteApiService.uploadImageInTypedTestQuestion(
        this.currentInstituteSlug,
        this.currentSubjectSlug,
        this.question.question_id.toString(),
        { file }
      ).subscribe(
        (result: {type: number; loaded: number; total: number; file: string; body: any; }) => {
          if (result.type === HttpEventType.UploadProgress) {
            this.progress = Math.round(100 * result.loaded / result.total);
            this.loadedFileSize = result.loaded;
            this.totalFileSize = result.total;
          } else if (result.type === HttpEventType.Response) {
            this.question.image = result.body.image;
            this.uploadIndicator = false;
            this.uploadImageForm.reset();
            this.uploadImageForm.enable();
            this.uiService.showSnackBar(
              'Image uploaded successfully.',
              3000
            );
          }
        },
        errors => {
          this.uploadIndicator = false;
          this.uploadImageForm.enable();
          if (errors.error) {
            if (errors.error.error) {
              this.uploadError = errors.error.error;
            } else {
              this.uiService.showSnackBar(
                'Error! Unable to upload image at the moment.',
                3000
              );
            }
          } else {
            this.uiService.showSnackBar(
              'Error! Unable to upload image at the moment.',
              3000
            );
          }
        }
      );
    }
  }
}
