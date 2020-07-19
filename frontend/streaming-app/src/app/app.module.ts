import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { AppRoutingModule, routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MaterialModule } from './material.module';
import { AuthService } from './auth.service';
import { HttpClientModule } from '@angular/common/http';

import { TeacherWorkspaceModule } from './teacher-workspace/teacher-workspace.module';
import { StudentWorkspaceModule } from './student-workspace/student-workspace.module';
import { StaffWorkspaceModule } from './staff-workspace/staff-workspace.module';
import { SchoolWorkspaceModule } from './school-workspace/school-workspace.module';
import { CollegeWorkspaceModule } from './college-workspace/college-workspace.module';
import { HelpModule } from './help/help.module';
import { FeaturesModule } from './features/features.module';
import { PricingModule } from './pricing/pricing.module';
import { AboutModule } from './about/about.module';
import { HomeModule } from './home/home.module';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    MaterialModule,
    HttpClientModule,
    TeacherWorkspaceModule,
    StudentWorkspaceModule,
    StaffWorkspaceModule,
    SchoolWorkspaceModule,
    CollegeWorkspaceModule,
    HomeModule,
    FeaturesModule,
    PricingModule,
    AboutModule,
    HelpModule,
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
