import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
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
import { CollegeMaterialWorkspaceModule } from './material.college.workspace.module';
import { CollegeProfileComponent } from './college-profile/college-profile.component';
import { CollegePermissionsComponent } from './college-permissions/college-permissions.component';
import { CollegeWorkspaceComponent } from './college-workspace.component';


@NgModule({
  declarations: [
    CollegeWorkspaceComponent,
    CollegeProfileComponent,
    CollegePermissionsComponent,
  ],
  imports: [
    RouterModule,
    CommonModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    CollegeMaterialWorkspaceModule,
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
export class CollegeWorkspaceModule { }
