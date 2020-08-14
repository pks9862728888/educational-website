import { actionContent } from './../../../constants';
import { Component, OnInit, Input } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';

@Component({
  selector: 'app-view-video',
  templateUrl: './view-video.component.html',
  styleUrls: ['./view-video.component.css']
})
export class ViewVideoComponent implements OnInit {

  content: StudyMaterialDetails;

  constructor() {
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
  }

  ngOnInit(): void {
  }

}
