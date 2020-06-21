import { NgModule } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDividerModule } from '@angular/material/divider';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatBottomSheetModule } from '@angular/material/bottom-sheet';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCheckboxModule } from '@angular/material/checkbox';


@NgModule({
    imports: [
        MatSidenavModule,
        MatListModule,
        MatIconModule,
        MatToolbarModule,
        MatDividerModule,
        MatTabsModule,
        MatCardModule,
        MatGridListModule,
        MatButtonModule,
        MatInputModule,
        MatFormFieldModule,
        MatRadioModule,
        MatSelectModule,
        MatDatepickerModule,
        MatBottomSheetModule,
        MatSnackBarModule,
        MatDialogModule,
        MatProgressBarModule,
        MatCheckboxModule
    ],
    exports: [
        MatSidenavModule,
        MatListModule,
        MatIconModule,
        MatToolbarModule,
        MatDividerModule,
        MatTabsModule,
        MatCardModule,
        MatGridListModule,
        MatButtonModule,
        MatInputModule,
        MatFormFieldModule,
        MatRadioModule,
        MatSelectModule,
        MatDatepickerModule,
        MatBottomSheetModule,
        MatSnackBarModule,
        MatDialogModule,
        MatProgressBarModule,
        MatCheckboxModule
    ]
})
export class TeacherMaterialWorkspaceModule { }
