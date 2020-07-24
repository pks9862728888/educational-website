import { AuthModule } from './auth/auth.module';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SignUpLoginGuard,StudentWorkspaceGuard, TeacherWorkspaceGuard,
         StaffWorkspaceGuard, SchoolWorkspaceGuard, CollegeWorkspaceGuard,
         CoachingWorkspaceGuard } from './auth/auth.guard';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  {
    path: 'auth',
    loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule),
    canLoad: [SignUpLoginGuard]
  },
  { path: 'teacher-workspace',
    loadChildren: () => import('./teacher-workspace/teacher-workspace.module').then(m => m.TeacherWorkspaceModule),
    canLoad: [TeacherWorkspaceGuard]
  },
  {
    path: 'student-workspace',
    loadChildren: () => import('./student-workspace/student-workspace.module').then(m => m.StudentWorkspaceModule),
    canLoad: [StudentWorkspaceGuard]
  },
  {
    path: 'staff-workspace',
    loadChildren: () => import('./staff-workspace/staff-workspace.module').then(m => m.StaffWorkspaceModule),
    canLoad: [StaffWorkspaceGuard]
  },
  {
    path: 'school-workspace',
    loadChildren: () => import('./school-workspace/school-workspace.module').then(m => m.SchoolWorkspaceModule),
    canLoad: [SchoolWorkspaceGuard]
  },
  {
    path: 'college-workspace',
    loadChildren: () => import('./college-workspace/college-workspace.module').then(m => m.CollegeWorkspaceModule),
    canLoad: [CollegeWorkspaceGuard]
  },
  {
    path: 'coaching-workspace',
    loadChildren: () => import('./coaching-workspace/coaching-workspace.module').then(m => m.CoachingWorkspaceModule),
    canLoad: [CoachingWorkspaceGuard]
  },
  {
    path: 'features',
    loadChildren: () => import('./features/features.module').then(m => m.FeaturesModule)
  },
  {
    path: 'pricing',
    loadChildren: () => import('./pricing/pricing.module').then(m => m.PricingModule)
  },
  {
    path: 'about',
    loadChildren: () => import('./about/about.module').then(m => m.AboutModule)
  },
  {
    path: 'help',
    loadChildren: () => import('./help/help.module').then(m => m.HelpModule)
  },
  {
    path: 'sitemap',
    loadChildren: () => import('./sitemap/sitemap.module').then(m => m.SitemapModule)
  },
  {
    path: '**',
    loadChildren: () => import('./page-not-found/page-not-found.module').then(m => m.PageNotFoundModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [
    SignUpLoginGuard,
    TeacherWorkspaceGuard,
    StudentWorkspaceGuard,
    StaffWorkspaceGuard,
    SchoolWorkspaceGuard,
    CollegeWorkspaceGuard,
    CoachingWorkspaceGuard
  ]
})
export class AppRoutingModule { }

export const routingComponents = [];
