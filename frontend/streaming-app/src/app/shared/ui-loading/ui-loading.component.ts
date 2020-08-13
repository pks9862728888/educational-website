import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-ui-loading',
  templateUrl: './ui-loading.component.html',
  styleUrls: ['./ui-loading.component.css']
})
export class UiLoadingComponent implements OnInit {

  mq: MediaQueryList;
  diameter: number;
  @Input() actionText: string;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    if (this.mq.matches) {
      this.diameter = 50;
    } else {
      this.diameter = 70;
    }
  }

}
