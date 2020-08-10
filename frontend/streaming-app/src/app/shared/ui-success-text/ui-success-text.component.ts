import { MediaMatcher } from '@angular/cdk/layout';
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-success-text',
  templateUrl: './ui-success-text.component.html',
  styleUrls: ['./ui-success-text.component.css']
})
export class UiSuccessTextComponent {

  mq: MediaQueryList;
  @Input() successText: string;
  @Output() closeSuccessTextEvent = new EventEmitter<void>();

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  hideSuccessText() {
    this.closeSuccessTextEvent.emit();
  }
}
