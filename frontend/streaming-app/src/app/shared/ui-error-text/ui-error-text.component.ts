import { MediaMatcher } from '@angular/cdk/layout';
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-error-text',
  templateUrl: './ui-error-text.component.html',
  styleUrls: ['./ui-error-text.component.css']
})
export class UiErrorTextComponent {

  mq: MediaQueryList;
  @Input() errorText: string;
  @Output() closeErrorTextEvent = new EventEmitter<void>();

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  hideErrorText() {
    this.closeErrorTextEvent.emit();
  }
}
