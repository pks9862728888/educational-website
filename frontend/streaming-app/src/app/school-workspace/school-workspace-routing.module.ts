import { NgModule } from '@angular/core';
import { InstituteRoutingGuard } from './../guard/institute.guard';
import { PurchaseLicenseGuard, LicenseGuard } from '../guard/license.guard';
import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { SchoolPermissionsComponent } from './school-permissions/school-permissions.component';
import { SchoolClassesComponent } from './school-classes/school-classes.component';
import { LicenseComponent } from '../license/license.component';
import { LicenseCheckoutComponent } from '../license/license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './../license/license-review/license-review.component';
import { PurchaseLicenseComponent } from '../license/purchase-license/purchase-license.component';

const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: SchoolPermissionsComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/classes', component: SchoolClassesComponent, canActivate: [InstituteRoutingGuard]},
      { path: ':name/license', component: LicenseComponent, canActivate: [LicenseGuard] },
      { path: ':name/license/purchase', component: PurchaseLicenseComponent, canActivate: [PurchaseLicenseGuard]},
      { path: ':name/license/review', component: LicenseReviewComponent, canActivate: [PurchaseLicenseGuard]},
      { path: ':name/license/checkout', component: LicenseCheckoutComponent, canActivate: [PurchaseLicenseGuard] }
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
  SchoolProfileComponent,
  SchoolPermissionsComponent,
  SchoolClassesComponent
];
