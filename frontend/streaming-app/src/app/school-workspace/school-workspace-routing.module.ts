import { LicenseReviewGuard } from './../route.guard';
import { RouterModule, Routes } from '@angular/router';
import { SchoolWorkspaceComponent } from './school-workspace.component';
import { SchoolProfileComponent } from './school-profile/school-profile.component';
import { SchoolPermissionsComponent } from './school-permissions/school-permissions.component';
import { SchoolClassesComponent } from './school-classes/school-classes.component';
import { NgModule } from '@angular/core';
import { LicenseComponent } from '../license/license.component';
import { LicenseCheckoutComponent } from '../license/license-checkout/license-checkout.component';
import { LicenseReviewComponent } from './../license/license-review/license-review.component';


const routes: Routes = [
  {
    path: '',
    component: SchoolWorkspaceComponent,
    children: [
      { path: ':name/profile', component: SchoolProfileComponent },
      { path: ':name/permissions', component: SchoolPermissionsComponent },
      { path: ':name/classes', component: SchoolClassesComponent },
      { path: ':name/license', component: LicenseComponent },
      { path: ':name/license/review', component: LicenseReviewComponent, canActivate: [LicenseReviewGuard]},
      { path: ':name/license/checkout', component: LicenseCheckoutComponent }
    ],
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [LicenseReviewGuard]
})
export class SchoolWorkspaceRoutingModule {}

export const schoolWorkspaceRoutingComponents = [
  SchoolWorkspaceComponent,
  SchoolProfileComponent,
  SchoolPermissionsComponent,
  SchoolClassesComponent
];
