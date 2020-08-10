import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-ui-add-external-link',
  templateUrl: './ui-add-external-link.component.html',
  styleUrls: ['./ui-add-external-link.component.css']
})
export class UiAddExternalLinkComponent implements OnInit {

  mq: MediaQueryList;
  addExternalLinkForm: FormGroup;
  @Output() formFieldError = new EventEmitter<string>();
  @Output() formData = new EventEmitter<any>();

  constructor(
    private media: MediaMatcher,
    private formBuilder: FormBuilder
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.addExternalLinkForm = this.formBuilder.group({
      title: [null, [Validators.required, Validators.maxLength(30)]],
      link: [null, [Validators.required, Validators.maxLength(100)]]
    });
  }

  upload() {
    this.addExternalLinkForm.patchValue({
      title: this.addExternalLinkForm.value.title.trim(),
      link: this.addExternalLinkForm.value.link.trim()
    })
    if (!this.addExternalLinkForm.value.title) {
      this.formFieldError.emit('Title can not be blank.');
    } else if (!this.addExternalLinkForm.value.link) {
      this.formFieldError.emit('Link can not be blank.');
    }
  }

}
