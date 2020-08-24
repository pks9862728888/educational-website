import { Routes, RouterModule } from '@angular/router';
import { PreviewCourseComponent } from './preview-course/preview-course.component';
import { AnnouncementsComponent } from './announcements/announcements.component';
import { JoinGroupsComponent } from './join-groups/join-groups.component';
import { ViewPeersComponent } from './view-peers/view-peers.component';
import { PreviewCourseWorkspaceComponent } from './preview-course-workspace.component';
import { NgModule } from '@angular/core';

const routes: Routes = [
  {
    path: '',
    component: PreviewCourseWorkspaceComponent,
    children: [
      {path: ':name/preview', component: PreviewCourseComponent},
      {path: ':name/view-peers', component: ViewPeersComponent},
      {path: ':name/join-groups', component: JoinGroupsComponent},
      {path: ':name/announcements', component: AnnouncementsComponent}
    ]
  }
]

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PreviewCourseRoutingModule {}

export const previewCourseRoutingComponents = [
  PreviewCourseWorkspaceComponent,
  PreviewCourseComponent,
  ViewPeersComponent,
  JoinGroupsComponent,
  AnnouncementsComponent
];
