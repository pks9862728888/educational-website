import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ui-error-text',
  templateUrl: './ui-error-text.component.html',
  styleUrls: ['./ui-error-text.component.css']
})
export class UiErrorTextComponent {

  @Input() errorText: string;
  @Output() closeErrorTextEvent = new EventEmitter<void>();

  constructor() { }

  hideErrorText() {
    this.closeErrorTextEvent.emit();
  }
}
