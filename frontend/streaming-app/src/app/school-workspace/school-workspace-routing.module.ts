import { StudentInstituteCoursesComponent } from './../shared/student-institute-courses/student-institute-courses.component';
import { PermissionsComponent } from './../shared/permissions/permissions.component';
import { NgModule } from '@angular/core';
import { InstituteRoutingGuard } from './../guard/institute.guard';
import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { LicenseComponent } from '../license/license.component';
import { CommonLicenseCheckoutComponent } from '../license/common-license-checkout/common-license-checkout.component';
import { CommonLicenseReviewComponent } from '../license/common-license-review/common-license-review.component';
import { PurchaseCommonLicenseComponent } from '../license/purchase-common-license/purchase-common-license.component';
import { ClassComponent } from '../shared/class/class.component';
import { InstituteStudentsComponent } from '../shared/institute-students/institute-students.component';
import { ChooseProductTypeComponent } from '../license/choose-product-type/choose-product-type.component';
import { PurchaseStorageComponent } from '../license/purchase-storage/purchase-storage.component';
import { PurchaseLiveClassLicenseComponent } from '../license/purchase-live-class-license/purchase-live-class-license.component';
import { PurchaseDigitalAdaptiveExamLicenseComponent } from '../license/purchase-digital-adaptive-exam-license/purchase-digital-adaptive-exam-license.component';

const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: PermissionsComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/classes', component: ClassComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/license', component: LicenseComponent },
      { path: ':name/license/choose-product-type', component: ChooseProductTypeComponent },
      { path: ':name/license/purchase-common-license', component: PurchaseCommonLicenseComponent},
      { path: ':name/license/purchase-storage-license', component: PurchaseStorageComponent},
      { path: ':name/license/purchase-digital-adaptive-exam-license', component: PurchaseDigitalAdaptiveExamLicenseComponent},
      { path: ':name/license/purchase-live-class-license', component: PurchaseLiveClassLicenseComponent},
      { path: ':name/license/review', component: CommonLicenseReviewComponent},
      { path: ':name/license/checkout', component: CommonLicenseCheckoutComponent },
      { path: ':name/students', component: InstituteStudentsComponent},
      { path: ':name/student-courses', component: StudentInstituteCoursesComponent}
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
    InstituteRoutingGuard
  ]
})
export class SchoolWorkspaceRoutingModule {}

export const schoolWorkspaceRoutingComponents = [
  SchoolWorkspaceComponent,
  SchoolProfileComponent
];
