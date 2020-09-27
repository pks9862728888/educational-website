import { courseContent} from './../../../constants';
import { MediaMatcher } from '@angular/cdk/layout';
import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { InstituteSubjectLectureMaterial } from '../../models/subject.model';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-view-image',
  templateUrl: './view-image.component.html',
  styleUrls: ['./view-image.component.css']
})
export class ViewImageComponent implements OnInit {

  content: InstituteSubjectLectureMaterial;
  @Output() closeViewEvent = new EventEmitter();
  mq: MediaQueryList;

  constructor(
    private media: MediaMatcher
  ) {
    this.mq = this.media.matchMedia('(max-width: 600px)');
    this.content = JSON.parse(sessionStorage.getItem(courseContent));
  }

  ngOnInit(): void {}

  back() {
    this.closeViewEvent.emit();
  }

  download() {
    const ext = this.content.data.file.split('.');
    saveAs(
      this.content.data.file, this.content.name.toLowerCase().replace(' ', '_') + '.' + ext[ext.length - 1]);
  }
}
