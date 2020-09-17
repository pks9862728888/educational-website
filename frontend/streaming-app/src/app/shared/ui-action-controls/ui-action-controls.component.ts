import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { EditDeleteDialogData } from '../../models/dialog.model';

@Component({
  selector: 'app-ui-action-controls',
  templateUrl: './ui-action-controls.component.html',
  styleUrls: ['./ui-action-controls.component.css']
})
export class UiActionControlsComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: EditDeleteDialogData) { }

  ngOnInit(): void {
  }

}
