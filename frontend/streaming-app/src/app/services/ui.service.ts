import { MatSnackBar } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { UiDialogComponent } from '../shared/ui-dialog/ui-dialog.component';
import { Subject } from 'rxjs';
import { UiActionControlsComponent } from '../shared/ui-action-controls/ui-action-controls.component';
import { SnackbarComponent } from '../shared/snackbar/snackbar.component';
import { ConfirmNameComponent } from '../shared/student-institutes/confirm-name/confirm-name.component';

@Injectable({
  providedIn: 'root'
})
export class UiService {

  private dialogData = new Subject<any>();
  dialogData$ = this.dialogData.asObservable();

  private actionControlDialogData = new Subject<string>();
  actionControlDialogData$ = this.actionControlDialogData.asObservable();

  private nameDialogData = new Subject<{'first_name': string; 'last_name': string}>();
  nameDialogData$ = this.nameDialogData.asObservable();

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

  openNameDialog() {
    // Dialog to confirm student's name while joining institute
    const dialogRef = this.dialog.open(ConfirmNameComponent);
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.nameDialogData.next(result);
      } else {
        this.nameDialogData.next();
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
