import { MatSnackBar } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { UiDialogComponent } from '../shared/ui-dialog/ui-dialog.component';
import { Subject } from 'rxjs';
import { UiActionControlsComponent } from '../shared/ui-action-controls/ui-action-controls.component';
import { SnackbarComponent } from '../shared/snackbar/snackbar.component';
import { ConfirmStudentsDetailsComponent } from '../shared/student-institutes/confirm-students-details/confirm-students-details.component';
import { UiEditDeleteAddAddControlsComponent } from '../shared/ui-edit-delete-add-add-controls/ui-edit-delete-add-add-controls.component';

@Injectable({
  providedIn: 'root'
})
export class UiService {

  private dialogData = new Subject<any>();
  dialogData$ = this.dialogData.asObservable();

  private editDeleteDialogData = new Subject<any>();
  editDeleteDialogData$ = this.editDeleteDialogData.asObservable();

  private openEditDeleteAddAddDialogData = new Subject<string>();
  openEditDeleteAddAddDialogData$ = this.openEditDeleteAddAddDialogData.asObservable();

  private studentDetailsDialogData = new Subject<boolean>();
  studentDetailsDialogData$ = this.studentDetailsDialogData.asObservable();

  constructor(
    private snackBar: MatSnackBar,
    public dialog: MatDialog
    ) { }

  openDialog(title: string, falseStringDisplay: string, trueStringDisplay: string) {
    const dialogRef = this.dialog.open(UiDialogComponent, {
      data: {
        title, trueStringDisplay, falseStringDisplay
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

  openEditDeleteDialog(firstButtonText: string, secondButtonText: string) {
    const dialogRef = this.dialog.open(UiActionControlsComponent, {
      data: {
        firstButtonText, secondButtonText
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.editDeleteDialogData.next(result);
      } else {
        this.editDeleteDialogData.next();
      }
    });
  }

  openEditDeleteAddAddDialog(
    firstButtonText: string,
    secondButtonText: string,
    thirdButtonText: string,
    fourthButtonText: string
    ) {
    const dialogRef = this.dialog.open(UiEditDeleteAddAddControlsComponent, {
      data: {
        firstButtonText, secondButtonText, thirdButtonText, fourthButtonText
      }
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.openEditDeleteAddAddDialogData.next(result);
      } else {
        this.openEditDeleteAddAddDialogData.next();
      }
    });
  }

  openStudentDetailsConfirmDialog(instituteSlug: string) {
    // Dialog to confirm student's details while joining institute
    const dialogRef = this.dialog.open(ConfirmStudentsDetailsComponent, {
      data: {instituteSlug}
    });
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.studentDetailsDialogData.next(result);
      } else {
        this.studentDetailsDialogData.next();
      }
    });
  }

  showSnackBar(message: string, duration: number) {
    this.snackBar.openFromComponent(SnackbarComponent, {
      data: message,
      duration
    });
  }
}
