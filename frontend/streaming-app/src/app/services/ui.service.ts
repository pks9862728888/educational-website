import { MatSnackBar } from '@angular/material/snack-bar';
import { Injectable } from '@angular/core';
import { SnackbarComponent } from '../teacher-workspace/teacher-institute/teacher-institute.component';

@Injectable({
  providedIn: 'root'
})
export class UiService {

  constructor(private _snackBar: MatSnackBar) { }

  showSnackBar(message: string, duration: number) {
    this._snackBar.openFromComponent(SnackbarComponent, {
      data: message,
      duration: duration
    });
  }
}
