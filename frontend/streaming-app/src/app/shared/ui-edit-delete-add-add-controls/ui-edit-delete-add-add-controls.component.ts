import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { EditDeleteAddAddDialogData } from '../../models/dialog.model';

@Component({
  selector: 'app-ui-edit-delete-add-add-controls',
  templateUrl: './ui-edit-delete-add-add-controls.component.html',
  styleUrls: ['./ui-edit-delete-add-add-controls.component.css']
})
export class UiEditDeleteAddAddControlsComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: EditDeleteAddAddDialogData) { }

  ngOnInit(): void {
  }

}
