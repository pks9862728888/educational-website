import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SitemapComponent } from './sitemap.component';

const routes: Routes = [
  {
    path: '',
    component: SitemapComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SitemapRoutingModule {}

export const sitemapRoutingComponents = [
  SitemapComponent
];
