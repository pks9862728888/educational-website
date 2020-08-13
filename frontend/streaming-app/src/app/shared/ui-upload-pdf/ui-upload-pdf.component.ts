import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { formatDate } from '../../format-datepicker';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-ui-upload-pdf',
  templateUrl: './ui-upload-pdf.component.html',
  styleUrls: ['./ui-upload-pdf.component.css']
})
export class UiUploadPdfComponent implements OnInit {

  mq: MediaQueryList;
  uploadPdfForm: FormGroup;
  showIndicator: boolean;
  @Input() showTargetDate: boolean;
  @Output() formData = new EventEmitter<any>();
  @Output() fileError = new EventEmitter<string>();
  @Input() formEvent: Observable<String>;
  private formEventSubscription: Subscription;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.uploadPdfForm = this.formBuilder.group({
      title: [null, [Validators.required, Validators.maxLength(30)]],
      file: [null, [Validators.required]],
      target_date: [null]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.uploadPdfForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.uploadPdfForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.uploadPdfForm.reset();
          this.uploadPdfForm.enable();
        }
      }
    );
  }

  upload() {
    const file: File = (<HTMLInputElement>document.getElementById('pdf-file')).files[0];
    console.log(file);
    console.log(formatDate(this.uploadPdfForm.value.target_date));

    if (!file.type.includes('application/pdf') || !file.name.endsWith('.pdf') || file.name.includes('.exe') || file.name.includes('.sh')) {
      this.fileError.emit('Only .pdf file formats are supported.');
      this.uploadPdfForm.patchValue({
        file: null
      });
    } else {
      this.formData.emit(file.size / 1000000 + ' Mb');
    }
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
  }
}
