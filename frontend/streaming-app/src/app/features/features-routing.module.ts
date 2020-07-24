import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { FeaturesComponent } from './features.component';

const routes: Routes = [
  {
    path: '',
    component: FeaturesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FeaturesRoutingModule {}

export const featuresRouteComponents = [
  FeaturesComponent
];
