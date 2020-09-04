import { PermissionsComponent } from './../shared/permissions/permissions.component';
import { NgModule } from '@angular/core';
import { InstituteRoutingGuard } from './../guard/institute.guard';
import { PurchaseLicenseGuard, LicenseGuard } from '../guard/license.guard';
import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { LicenseComponent } from '../license/license.component';
import { LicenseCheckoutComponent } from '../license/license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './../license/license-review/license-review.component';
import { PurchaseLicenseComponent } from '../license/purchase-license/purchase-license.component';
import { ClassComponent } from '../shared/class/class.component';
import { InstituteStudentsComponent } from '../shared/institute-students/institute-students.component';

const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: PermissionsComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/classes', component: ClassComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/license', component: LicenseComponent, canActivate: [LicenseGuard] },
      { path: ':name/license/purchase', component: PurchaseLicenseComponent, canActivate: [PurchaseLicenseGuard]},
      { path: ':name/license/review', component: LicenseReviewComponent, canActivate: [PurchaseLicenseGuard]},
      { path: ':name/license/checkout', component: LicenseCheckoutComponent, canActivate: [PurchaseLicenseGuard] },
      { path: ':name/students', component: InstituteStudentsComponent}
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
    LicenseGuard,
    PurchaseLicenseGuard,
    InstituteRoutingGuard
  ]
})
export class SchoolWorkspaceRoutingModule {}

export const schoolWorkspaceRoutingComponents = [
  SchoolWorkspaceComponent,
  SchoolProfileComponent
];
