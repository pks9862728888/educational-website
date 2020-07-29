import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-error-text',
  templateUrl: './error-text.component.html',
  styleUrls: ['./error-text.component.css']
})
export class ErrorTextComponent {

  @Input() errorText: string;
  @Output() closeErrorTextEvent = new EventEmitter<void>();

  constructor() { }

  hideErrorText() {
    this.closeErrorTextEvent.emit();
  }
}
