import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { InstituteSubjectLectureMaterial } from '../../models/subject.model';
import { courseContent } from '../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';

@Component({
  selector: 'app-view-pdf',
  templateUrl: './view-pdf.component.html',
  styleUrls: ['./view-pdf.component.css']
})
export class ViewPdfComponent implements OnInit {

  content: InstituteSubjectLectureMaterial;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;
  filename: string;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(courseContent));
  }

  ngOnInit(): void {
    const ext = this.content.data.file.split('.');
    this.filename = this.content.name.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1];
  }

  back() {
      this.closeViewEvent.emit();
  }
}
