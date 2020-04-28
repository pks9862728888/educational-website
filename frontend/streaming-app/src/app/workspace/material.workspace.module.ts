import { NgModule } from '@angular/core';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

@NgModule({
    imports: [
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatToolbarModule
    ],
    exports: [
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatToolbarModule
    ]
})
export class MaterialWorkspaceModule { }
