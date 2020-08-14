import { Component, OnInit, Input } from '@angular/core';
import { StudyMaterialDetails } from '../../models/subject.model';
import { actionContent } from '../../../constants';

@Component({
  selector: 'app-view-pdf',
  templateUrl: './view-pdf.component.html',
  styleUrls: ['./view-pdf.component.css']
})
export class ViewPdfComponent implements OnInit {

  content: StudyMaterialDetails;

  constructor() {
    this.content = JSON.parse(sessionStorage.getItem(actionContent));
  }

  ngOnInit(): void {
  }

}
