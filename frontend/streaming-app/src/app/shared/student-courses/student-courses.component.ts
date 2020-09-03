import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-student-courses',
  templateUrl: './student-courses.component.html',
  styleUrls: ['./student-courses.component.css']
})
export class StudentCoursesComponent implements OnInit {

  mq: MediaQueryList;
  openedPanelStep: number;
  count = 0;
  text = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis iure explicabo maiores nesciunt facilis consectetur rem distinctio unde laborum nostrum eligendi dolore animi fuga hic, eveniet, consequatur deleniti, porro voluptatem.';

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
  }

  ngOnInit(): void {
    this.openedPanelStep = 0;
  }

  setOpenedPanelStep(step: number) {
    if (this.openedPanelStep === step) {
      this.openedPanelStep = null;
    } else {
      this.openedPanelStep = step;
    }
  }

  formatDescription(text: string) {
    if (this.text.length > 106) {
      return this.text.slice(0, 106) + '...';
    } else {
      return this.text;
    }
  }

}
