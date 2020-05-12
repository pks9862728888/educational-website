import { NgModule } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDividerModule } from '@angular/material/divider';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';


@NgModule({
    imports: [
        MatSidenavModule,
        MatListModule,
        MatIconModule,
        MatToolbarModule,
        MatDividerModule,
        MatTabsModule,
        MatCardModule,
        MatGridListModule,
    ],
    exports: [
        MatSidenavModule,
        MatListModule,
        MatIconModule,
        MatToolbarModule,
        MatDividerModule,
        MatTabsModule,
        MatCardModule,
        MatGridListModule,
    ]
})
export class TeacherMaterialWorkspaceModule { }
