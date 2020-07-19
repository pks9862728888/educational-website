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

import { CoachingWorkspaceComponent } from './coaching-workspace.component';
import { CoachingProfileComponent } from './coaching-profile/coaching-profile.component';
import { CoachingPermissionsComponent } from './coaching-permissions/coaching-permissions.component';
import { CoachingMaterialWorkspaceModule } from './material.coaching.workspace.module';



@NgModule({
  declarations: [
    CoachingWorkspaceComponent,
    CoachingProfileComponent,
    CoachingPermissionsComponent,
  ],
  imports: [
    RouterModule,
    CommonModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    CoachingMaterialWorkspaceModule,
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
export class CoachingWorkspaceModule { }
