import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';
import { LicenseComponent } from './license.component';

const routes: Routes = [
  {
    path: '',
    component: LicenseComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LicenseRoutingModule {}
