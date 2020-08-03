import { DialogData } from './../../models/dialog.model';
import { Component, OnInit, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-ui-dialog',
  templateUrl: './ui-dialog.component.html',
  styleUrls: ['./ui-dialog.component.css']
})
export class UiDialogComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  ngOnInit(): void {}

}
