import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-ui-action-controls',
  templateUrl: './ui-action-controls.component.html',
  styleUrls: ['./ui-action-controls.component.css']
})
export class UiActionControlsComponent implements OnInit {

  reorder = 'REORDER';
  edit = 'EDIT';
  delete = 'DELETE';

  constructor() { }

  ngOnInit(): void {
  }

}
