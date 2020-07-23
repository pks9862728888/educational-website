import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';


@NgModule({
    imports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
    ],
    exports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
    ]
})
export class LicenseMaterialWorkspaceModule { }
