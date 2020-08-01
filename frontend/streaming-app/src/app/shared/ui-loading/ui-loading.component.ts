import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-ui-loading',
  templateUrl: './ui-loading.component.html',
  styleUrls: ['./ui-loading.component.css']
})
export class UiLoadingComponent implements OnInit {

  diameter = 70;
  @Input() actionText: string;

  constructor() { }

  ngOnInit(): void {
  }

}
