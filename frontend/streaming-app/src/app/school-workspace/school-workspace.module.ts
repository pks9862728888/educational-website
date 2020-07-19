import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolMaterialWorkspaceModule } from './material.school.workspace.module';
import { AppRoutingModule } from '../app-routing.module';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, DateAdapter, MAT_DATE_FORMATS } from '@angular/material/core';
import { ApiService } from '../api.service';
import { APP_DATE_FORMATS, AppDateAdapter } from '../format-datepicker';
import { InAppDataTransferService } from '../in-app-data-transfer.service';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { SchoolPermissionsComponent } from './school-permissions/school-permissions.component';
import { SchoolClassesComponent } from './school-classes/school-classes.component';



@NgModule({
  declarations: [
    SchoolWorkspaceComponent,
    SchoolProfileComponent,
    SchoolPermissionsComponent,
    SchoolClassesComponent,
  ],
  imports: [
    RouterModule,
    CommonModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    SchoolMaterialWorkspaceModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
    ApiService,
    InAppDataTransferService,
    {provide: DateAdapter, useClass: AppDateAdapter},
    {provide: MAT_DATE_FORMATS, useValue: APP_DATE_FORMATS}
  ]
})
export class SchoolWorkspaceModule { }
