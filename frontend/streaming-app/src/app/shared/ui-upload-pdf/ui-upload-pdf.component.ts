import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { formatDate } from '../../format-datepicker';
import { Observable, Subscription } from 'rxjs';
import { getFileSize } from '../utilityFunctions';
import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from 'src/constants';

@Component({
  selector: 'app-ui-upload-pdf',
  templateUrl: './ui-upload-pdf.component.html',
  styleUrls: ['./ui-upload-pdf.component.css']
})
export class UiUploadPdfComponent implements OnInit {

  mq: MediaQueryList;
  uploadForm: FormGroup;
  showIndicator: boolean;
  progress = 0;
  @Input() showTargetDate: boolean;
  @Output() formData = new EventEmitter<any>();
  @Output() fileError = new EventEmitter<string>();
  @Input() formEvent: Observable<String>;
  private formEventSubscription: Subscription;
  @Input() uploadProgressEvent: Observable<{loaded: number, total: number}>;
  private progressEventSubscription: Subscription;
  totalFileSize: number;
  loadedFileSize: number;

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.uploadForm = this.formBuilder.group({
      title: [null, [Validators.required, Validators.maxLength(30)]],
      file: [null, [Validators.required]],
      target_date: [null]
    });
    this.formEventSubscription = this.formEvent.subscribe(
      (data: string) => {
        if (data === 'ENABLE') {
          this.showIndicator = false;
          this.uploadForm.enable();
        } else if (data === 'DISABLE') {
          this.showIndicator = true;
          this.uploadForm.disable();
        } else if (data === 'RESET') {
          this.showIndicator = false;
          this.uploadForm.reset();
          this.uploadForm.enable();
        }
      }
    );
    this.progressEventSubscription = this.uploadProgressEvent.subscribe(
      (result: {loaded: number, total: number}) => {
        this.progress = Math.round(100 * result.loaded / result.total);
        this.loadedFileSize = result.loaded;
        this.totalFileSize = result.total;
      }
    );
  }

  upload() {
    const file: File = (<HTMLInputElement>document.getElementById('pdf-file')).files[0];

    if (!file.type.includes('application/pdf') || !file.name.endsWith('.pdf') || file.name.includes('.exe') || file.name.includes('.sh')) {
      this.fileError.emit('Only .pdf file formats are supported.');
      this.uploadForm.patchValue({
        file: null
      });
    } else {
      let data = {};
      data['title'] = this.uploadForm.value.title;
      data['file'] = file;
      if (this.uploadForm.value.target_date) {
        data['target_date'] = formatDate(this.uploadForm.value.target_date);
      }
      data['size'] = file.size / 1000000000;
      data['content_type'] = STUDY_MATERIAL_CONTENT_TYPE_REVERSE['PDF'];
      this.formData.emit(data);
    }
  }

  getFileSize_(size: number) {
    return getFileSize(size);
  }

  ngOnDestroy() {
    if (this.formEventSubscription) {
      this.formEventSubscription.unsubscribe();
    }
    if (this.progressEventSubscription) {
      this.progressEventSubscription.unsubscribe();
    }
  }
}
