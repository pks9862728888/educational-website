import { MatSnackBar } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';
import { SnackbarComponent } from '../teacher-workspace/teacher-institute/teacher-institute.component';
import { MatDialog } from '@angular/material/dialog';
import { UiDialogComponent } from '../shared/ui-dialog/ui-dialog.component';
import { Observable, Subject } from 'rxjs';
import { UiActionControlsComponent } from '../shared/ui-action-controls/ui-action-controls.component';

@Injectable({
  providedIn: 'root'
})
export class UiService {

  private dialogData = new Subject<any>();
  dialogData$ = this.dialogData.asObservable();

  private actionControlDialogData = new Subject<string>();
  actionControlDialogData$ = this.actionControlDialogData.asObservable();

  constructor(
    private _snackBar: MatSnackBar,
    public dialog: MatDialog
    ) { }

  openDialog(title: string, falseStringDisplay: string, trueStringDisplay: string) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title: title,
        trueStringDisplay: trueStringDisplay,
        falseStringDisplay: falseStringDisplay
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.dialogData.next(result);
      } else {
        this.dialogData.next();
      }
    });
  }

  openReorderEditDeleteDialog() {
    const dialogRef = this.dialog.open(UiActionControlsComponent);
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.actionControlDialogData.next(result);
      } else {
        this.actionControlDialogData.next();
      }
    });
  }

  showSnackBar(message: string, duration: number) {
    this._snackBar.openFromComponent(SnackbarComponent, {
      data: message,
      duration: duration
    });
  }
}
