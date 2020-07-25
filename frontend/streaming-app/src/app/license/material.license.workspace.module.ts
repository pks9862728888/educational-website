import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';


@NgModule({
    imports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
        MatProgressSpinnerModule
    ],
    exports: [
        MatButtonModule,
        MatIconModule,
        MatCardModule,
        MatProgressSpinnerModule
    ]
})
export class LicenseMaterialWorkspaceModule { }
